import os
import pytest
from playwright.sync_api import Page, expect
from utils.helpers import Helper
from utils.mail_helper import Mail
from pages.login_page import LoginPage
from pages.profil_ZZ_page import ProfilZZ


password = os.getenv("EPRIHLASKY_ZZ_PASSWORD")


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_zmeny_udajov_ZZ_IFO(page: Page, email_account_picker) -> None:
    helper = Helper()
    mail = Mail()
    login = LoginPage(page)
    profil = ProfilZZ(page)

    login.login_as_zakonny_zastupca("roidap@quimail.site", password)
    profil.otvorit_profil()

    aktualna_adresa = (page.locator("#profil-adresa").text_content() or "").strip()
    if aktualna_adresa == "Záštepy 32/98, 06578, Trebatice, Slovenská republika":
        stat = "Slovenská re"
        mesto = "semero"
        ulica = "kuri"
        sup_cislo = ""
        or_cislo = "12"
        psc = "85476"
    else:
        stat = "Slovenská re"
        mesto = "trebatic"
        ulica = "zast"
        sup_cislo = "32"
        or_cislo = "98"
        psc = "06578"

    expect(
        page.locator("#profil-dn"),
        "Dátum narodenia zákonného zástupcu sa nezobrazuje správne."
    ).to_contain_text("17.02.1988")

    povodny_email = page.locator("#profil-mail").text_content()
    account = email_account_picker(povodny_email)
    telefon = helper.vygeneruj_tel_cislo()

    profil.zmen_tel_cislo(telefon)
    profil.click_on_ulozit_zmeny()

    expect(
        page.locator("#profil-nastavenieZZ"),
        "Po zmene telefónneho čísla sa nezobrazila úspešná hláška."
    ).to_contain_text("Zmeny sme úspešne uložili.")

    profil.zmenit_mail(account["new_email"])
    kod = mail.get_six_digit_number_from_last_email(
        "imap.gmail.com",
        account["mail_user"],
        account["mail_pw"]
    )
    profil.overit_kod_mailu(kod)

    profil.zmenit_adresu(stat, mesto, ulica, sup_cislo, or_cislo, psc)

    expect(
        page.locator("#profil-nastavenieZZ"),
        "Po zmene adresy sa nezobrazila úspešná hláška."
    ).to_contain_text("Zmeny sme úspešne uložili.")

    profil.otvorit_profil()

    if mesto == "semero":
        expect(
            page.locator("#profil-adresa"),
            "Adresa zákonného zástupcu sa po zmene na Semerovo nezobrazila správne."
        ).to_contain_text("Kúria 12, 85476, Semerovo, Slovenská republika")
    else:
        expect(
            page.locator("#profil-adresa"),
            "Adresa zákonného zástupcu sa po zmene na Trebatice nezobrazila správne."
        ).to_contain_text("Záštepy 32/98, 06578, Trebatice, Slovenská republika")

    expect(
        page.locator("#profil-rodneCislo"),
        "Rodné číslo zákonného zástupcu sa nezobrazuje správne."
    ).to_contain_text("880217/9210")

    expect(
        page.locator("#profil-dn"),
        "Dátum narodenia zákonného zástupcu sa po úpravách nezobrazuje správne."
    ).to_contain_text("17.02.1988")

    expect(
        page.locator("#profil-tel"),
        "Telefónne číslo zákonného zástupcu sa po zmene nezobrazuje správne."
    ).to_contain_text(telefon)

    expect(
        page.locator("#profil-mail"),
        "E-mail zákonného zástupcu sa po zmene nezobrazuje správne."
    ).to_contain_text(account["new_email"])

    expect(
        page.locator("#profil-meno"),
        "Prihlasovacie meno zákonného zástupcu sa nezobrazuje správne."
    ).to_contain_text("roidap@quimail.site")