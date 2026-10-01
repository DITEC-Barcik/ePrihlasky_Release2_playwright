import email as email_lib
import imaplib
import random
import re
import string
import time
from playwright.sync_api import Playwright

from utils.mail_helper import Mail


class GmailAliasClient:
    """Jednorazove adresy cez Gmail plus-aliasy - vsetko chodi do jednej schranky."""

    IMAP_HOST = "imap.gmail.com"
    POLL_SECONDS = 10
    SCAN_LAST_MESSAGES = 20

    def __init__(self, address: str, password: str):
        self.address = address
        self.password = password

    @staticmethod
    def _random_string(length: int = 8) -> str:
        chars = string.ascii_lowercase + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    def create_alias(self) -> str:
        local, domain = self.address.split("@")
        return f"{local}+{self._random_string()}@{domain}"

    def wait_for_registration_link(self, alias: str, timeout_seconds: int = 180) -> str:
        deadline = time.time() + timeout_seconds

        while time.time() < deadline:
            text = self._find_message_text(alias)
            if text:
                # Portal posiela HTML aj v textovej casti, URL preto konci na < > " '
                match = re.search(r"https?://[^\s\"'<>]+", text)
                if match:
                    return match.group(0).rstrip("].,")
            time.sleep(self.POLL_SECONDS)

        raise AssertionError(
            f"Registracny e-mail pre {alias} neprisiel do {timeout_seconds} s."
        )

    def _find_message_text(self, alias: str) -> str | None:
        # Hlavicky kontrolujeme sami - Gmail IMAP search s plus-aliasmi nie je spolahlivy.
        mail = imaplib.IMAP4_SSL(self.IMAP_HOST, 993)
        try:
            mail.login(self.address, self.password)
            if mail.select("INBOX")[0] != "OK":
                return None

            status, data = mail.search(None, "ALL")
            if status != "OK" or not data[0]:
                return None

            for message_id in reversed(data[0].split()[-self.SCAN_LAST_MESSAGES:]):
                status, fetched = mail.fetch(message_id, "(RFC822)")
                if status != "OK" or not fetched or not isinstance(fetched[0], tuple):
                    continue

                message = email_lib.message_from_bytes(fetched[0][1])
                recipients = " ".join(
                    str(message.get(header, "")) for header in ("To", "Delivered-To", "X-Original-To")
                )
                if alias.lower() in recipients.lower():
                    return Mail.extract_text(message)

            return None
        finally:
            try:
                mail.logout()
            except Exception:
                pass


class MailTmClient:
    BASE_URL = "https://api.mail.tm"

    def __init__(self, playwright: Playwright):
        self.api = playwright.request.new_context(
            base_url=self.BASE_URL,
            extra_http_headers={"Content-Type": "application/json"}
        )

    def _random_string(self, length: int = 10) -> str:
        chars = string.ascii_lowercase + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    def create_temp_mailbox(self) -> tuple[str, str]:
        domains_response = self.api.get("/domains")
        assert domains_response.ok, f"Domains call failed: {domains_response.status}"
        domains_json = domains_response.json()
        domain = domains_json["hydra:member"][0]["domain"]

        email = f"{self._random_string()}@{domain}".lower()
        password = f"Pw{self._random_string(10)}1!"

        create_response = self.api.post(
            "/accounts",
            data={"address": email, "password": password}
        )
        assert create_response.status == 201, create_response.text()

        token_response = self.api.post(
            "/token",
            data={"address": email, "password": password}
        )
        assert token_response.status == 200, token_response.text()

        token = token_response.json()["token"]
        return email, token

    def wait_for_registration_link(self, token: str, timeout_seconds: int = 60) -> str:
        deadline = time.time() + timeout_seconds
        auth_api = self.api

        while time.time() < deadline:
            messages_response = auth_api.get(
                "/messages",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert messages_response.status == 200, messages_response.text()
            messages_json = messages_response.json()
            messages = messages_json.get("hydra:member", [])

            if messages:
                message_id = messages[0]["id"]
                message_response = auth_api.get(
                    f"/messages/{message_id}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                assert message_response.status == 200, message_response.text()
                message_json = message_response.json()

                text = message_json.get("text", "") or ""
                match = re.search(r"https?://\S+", text)
                if match:
                    return match.group(0).rstrip("].,>)")

            time.sleep(5)

        raise AssertionError("Registration email did not arrive in time")

    def dispose(self):
        self.api.dispose()