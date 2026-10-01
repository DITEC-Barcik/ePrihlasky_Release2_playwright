import pytest
import os
import utils.data_helper as Data
from utils.api_register import GmailAliasClient
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.registracia_page import Registracia


user_password = os.getenv("EPRIHLASKY_ZZ_PASSWORD")
mail_user = os.getenv("GMAIL_USERNAME")
mail_password = os.getenv("GMAIL_APP_PASSWORD")


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_registracia(page: Page) -> None:
    registracia = Registracia(page)
    login = LoginPage(page)
    mail_client = GmailAliasClient(mail_user, mail_password)

    email = mail_client.create_alias()
    data = Data.generate_unique_person(min_age=25, max_age=55)

    registracia.click_on_registracia()

    expect(
        page.locator("#step-1"),
        "Registračný krok 1 sa nezobrazil správne."
    ).to_contain_text("Registrácia")

    expect(
        page.locator("#step-1-panel-container"),
        "Úvodný text pri registrácii sa nezobrazil správne."
    ).to_contain_text(
        "Registráciu vytvára zákonný zástupca dieťaťaPri registrácii vyplňte údaje zákonného zástupcu (nie dieťaťa), ktorý bude prihlášku podávať."
    )

    registracia.vypln_registracny_formular(
        email,
        user_password,
        data.meno,
        data.priezvisko,
        data.rodne_cislo,
        data.text
    )

    expect(
        page.locator("#potvrdenie-registracie"),
        "Potvrdenie registrácie sa nezobrazilo."
    ).to_contain_text("Potvrdenie registrácie")

    activation_url = mail_client.wait_for_registration_link(email, timeout_seconds=180)
    page.goto(activation_url)
    page.wait_for_timeout(85000)

    login.login_po_registracii(email, user_password)