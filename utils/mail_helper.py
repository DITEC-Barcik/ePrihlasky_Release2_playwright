import imaplib
import email
import re
import time
from datetime import datetime, timedelta, timezone
from email.message import Message
from email.utils import parsedate_to_datetime


MAX_WAIT_SECONDS = 180
POLLING_INTERVAL_SECONDS = 15
ARRIVAL_CLOCK_TOLERANCE_SECONDS = 1
RECENT_MESSAGES_TO_CHECK = 20


class Mail:
    _returned_uids: set[bytes] = set()

    @staticmethod
    def extract_text(message: Message) -> str | None:
        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                if "attachment" in content_disposition:
                    continue

                if content_type == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode("utf-8", errors="replace").strip()

            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                if "attachment" in content_disposition:
                    continue

                if content_type == "text/html":
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode("utf-8", errors="replace").strip()
        else:
            payload = message.get_payload(decode=True)
            if payload:
                return payload.decode("utf-8", errors="replace").strip()

        return None

    @staticmethod
    def get_last_email_text(
    host: str,
    user: str,
    password: str,
    mailbox: str = "INBOX",
    max_wait_seconds: int = MAX_WAIT_SECONDS,
    polling_interval_seconds: int = POLLING_INTERVAL_SECONDS,) -> str | None:
        function_start_time = time.time()
        end_time = function_start_time + max_wait_seconds
        # Arrival time instead of message count: a slow IMAP login must not hide a mail that arrived meanwhile
        min_arrival_time = function_start_time - ARRIVAL_CLOCK_TOLERANCE_SECONDS

        poll_attempt = 0

        print("[MAIL] get_last_email_text started")
        print(f"[MAIL] function_start_time = {function_start_time}")
        print(f"[MAIL] max_wait_seconds = {max_wait_seconds}")
        print(f"[MAIL] polling_interval_seconds = {polling_interval_seconds}")
        print(f"[MAIL] end_time = {end_time}")

        while time.time() < end_time:
            poll_attempt += 1
            now = time.time()

            print("--------------------------------------------------")
            print(f"[MAIL] Poll attempt #{poll_attempt}")
            print(f"[MAIL] Current time = {now}")
            print(f"[MAIL] Remaining wait seconds = {int(end_time - now)}")

            mail = None

            try:
                print("[MAIL] Connecting to store...")
                mail = imaplib.IMAP4_SSL(host, 993)
                mail.login(user, password)
                print(f"[MAIL] Connected successfully in {time.time() - now:.1f} s")

                status, _ = mail.select(mailbox)
                if status != "OK":
                    print(f"[MAIL] Failed to open mailbox: {mailbox}")
                    continue

                status, messages = mail.uid("search", None, "ALL")
                if status != "OK":
                    print("[MAIL] Failed to search messages")
                    continue

                recent_uids = messages[0].split()[-RECENT_MESSAGES_TO_CHECK:]

                for uid in reversed(recent_uids):
                    if uid in Mail._returned_uids:
                        continue

                    status, date_data = mail.uid("fetch", uid, "(INTERNALDATE)")
                    if status != "OK" or not date_data or date_data[0] is None:
                        continue

                    arrival = imaplib.Internaldate2tuple(date_data[0])
                    if arrival is None:
                        continue

                    arrival_time = time.mktime(arrival)
                    if arrival_time < min_arrival_time:
                        # UIDs are ascending, older messages follow
                        break

                    print(f"[MAIL] Checking message uid = {uid.decode()}, arrived {arrival_time - function_start_time:+.1f} s from start")

                    status, msg_data = mail.uid("fetch", uid, "(RFC822)")
                    if status != "OK":
                        print("[MAIL] Failed to fetch message")
                        continue

                    raw_email = msg_data[0][1]
                    message = email.message_from_bytes(raw_email)

                    try:
                        subject = message.get("Subject", "<no subject>")
                    except Exception:
                        subject = "<unable to read subject>"

                    print(f"[MAIL] Subject = {subject}")

                    email_text = Mail.extract_text(message)

                    if email_text is None:
                        print("[MAIL] extract_text returned None")
                        continue

                    if not email_text.strip():
                        print("[MAIL] extract_text returned empty text")
                        continue

                    Mail._returned_uids.add(uid)
                    print("[MAIL] Email text extracted successfully")
                    print("[MAIL] Returning email text")
                    return email_text.strip()

                print("[MAIL] No new messages since function start")

            except Exception as e:
                print(f"[MAIL] Exception while reading email: {e}")

            finally:
                if mail is not None:
                    try:
                        print("[MAIL] Closing store")
                        mail.logout()
                    except Exception as e:
                        print(f"[MAIL] Failed to close store: {e}")

            if time.time() < end_time:
                print(f"[MAIL] No matching email yet, sleeping for {polling_interval_seconds} seconds...")
                time.sleep(polling_interval_seconds)

        print("[MAIL] Timeout reached, no matching email found")
        return None
    
    @staticmethod
    def find_six_digit_number(text: str | None) -> str | None:
        if not text:
            return None

        match = re.search(r"\b\d{6}\b", text)
        return match.group(0) if match else None

    @staticmethod
    def get_message_datetime(message: Message) -> tuple[datetime | None, str]:
        received_headers = message.get_all("Received", [])
        if received_headers:
            try:
                top_received = received_headers[0]
                received_date_part = top_received.split(";")[-1].strip()
                received_dt = parsedate_to_datetime(received_date_part)
                if received_dt is not None:
                    if received_dt.tzinfo is None:
                        received_dt = received_dt.replace(tzinfo=timezone.utc)
                    return received_dt, "Received"
            except Exception:
                pass

        try:
            sent_header = message.get("Date")
            if sent_header:
                sent_dt = parsedate_to_datetime(sent_header)
                if sent_dt is not None:
                    if sent_dt.tzinfo is None:
                        sent_dt = sent_dt.replace(tzinfo=timezone.utc)
                    return sent_dt, "Sent (fallback)"
        except Exception:
            pass

        return None, "N/A"

    @staticmethod
    def get_six_digit_number_from_last_email(
        host: str,
        user: str,
        password: str,
        mailbox: str = "INBOX",
        max_wait_seconds: int = MAX_WAIT_SECONDS,
        polling_interval_seconds: int = POLLING_INTERVAL_SECONDS,
    ) -> str | None:
        start_time = datetime.now(timezone.utc) - timedelta(seconds=2)
        end_time = time.time() + max_wait_seconds

        print(f"[MAIL] Starting to poll for a new email received AFTER: {start_time.isoformat()}")

        while time.time() < end_time:
            mail = None

            try:
                mail = imaplib.IMAP4_SSL(host, 993)
                mail.login(user, password)

                status, _ = mail.select(mailbox)
                if status != "OK":
                    print(f"[MAIL] Failed to open mailbox: {mailbox}")
                    continue

                status, messages = mail.search(None, "ALL")
                if status != "OK":
                    print("[MAIL] Failed to search messages")
                    continue

                email_ids = messages[0].split()
                print(f"[MAIL] Polling... Total messages in inbox: {len(email_ids)}")

                if email_ids:
                    last_email_id = email_ids[-1]
                    status, msg_data = mail.fetch(last_email_id, "(RFC822)")
                    if status != "OK":
                        print("[MAIL] Failed to fetch last message")
                        continue

                    raw_email = msg_data[0][1]
                    message = email.message_from_bytes(raw_email)

                    message_dt, date_type = Mail.get_message_datetime(message)
                    formatted_time = message_dt.strftime("%H:%M:%S") if message_dt else "N/A"

                    print(f"[MAIL] Last Message {date_type} Date/Time: {formatted_time}")

                    if message_dt is not None and message_dt > start_time:
                        print(f"[MAIL] Found a new email ({date_type} date after start time). Processing...")

                        email_text = Mail.extract_text(message)
                        preview = email_text[:200] + "..." if email_text and len(email_text) > 200 else email_text
                        print(f"[MAIL] Extracted Email Text (first 200 chars):\n{preview}")

                        six_digit_number = Mail.find_six_digit_number(email_text)

                        if six_digit_number is not None:
                            print(f"[MAIL] Successfully found 6-digit number: {six_digit_number}")
                            return six_digit_number
                        else:
                            print("[MAIL] New email found, but no 6-digit number extracted from it. Continuing to poll...")
                    else:
                        print("[MAIL] Last email is not new enough (or no valid date found). Waiting for a new email...")
                else:
                    print("[MAIL] No emails found in the inbox. Waiting for a new email...")

            except Exception as e:
                print(f"[MAIL] Error while checking email: {e}")

            finally:
                if mail is not None:
                    try:
                        mail.logout()
                    except Exception:
                        pass

            if time.time() < end_time:
                print(f"[MAIL] Next check in {polling_interval_seconds} seconds...")
                time.sleep(polling_interval_seconds)

        print(f"[MAIL] Timed out after {max_wait_seconds} seconds without finding a new email with a 6-digit number.")
        return None