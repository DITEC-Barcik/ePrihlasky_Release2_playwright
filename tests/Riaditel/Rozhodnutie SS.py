import os
import re
import pytest

from pages.logout_page import LogoutPage
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from utils.helpers import Helper as helper
from utils.mail_helper import Mail
from pages.rozhodnutie_SS_page import RozhodnutieSS

mailuser = os.getenv("GMAIL_USERNAME")
mailpw = os.getenv("GMAIL_APP_PASSWORD")

username_riad = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password_riad = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


def test_rozhodnutie_SS(page: Page) -> None:
    login = LoginPage(page)
    rozhodnutie = RozhodnutieSS(page)
    den, mesiac, rok = helper.aktualny_datum()

    login.login_as_riaditel(username_riad, password_riad, "910021624")
    rozhodnutie.navigate_to_rozhodnutia()
    rozhodnutie.search("Baráthová")
    rozhodnutie.select_first()
    rozhodnutie.click_upravit_rozhodnutie()

    expect(page.locator("#doplnenie-udajov")).to_contain_text("Doplnenie údajov")
    expect(page.locator("#doplnenie-udajov-description")).to_contain_text("Doplňte dátum, dôvody prijatia/neprijatia a číslo rozhodnutia.")
    expect(page.locator("#doplnenie-udajov-grid-content")).to_contain_text("Baráthová Valéria")

    rozhodnutie.click_prejst_na_podpis()

    expect(page.locator("#podpis-rozhodnuti")).to_contain_text("Podpis rozhodnutí")
    expect(page.locator("#podpis-rozhodnuti")).to_contain_text("Skontrolujte všetky rozhodnutia a pristúpte k ich podpisu.")
    expect(page.locator("#aktualny-nahlad-container")).to_contain_text("Stredná škola pre AT")
    expect(page.locator("#aktualny-nahlad-container")).to_contain_text("Číslo spisu: R-26-910021624-00001")
    expect(page.locator("#aktualny-nahlad-container")).to_contain_text("Dátum:")
    expect(page.locator("#aktualny-nahlad-container")).to_contain_text("ROZHODNUTIE")
    expect(page.locator("#aktualny-nahlad-container")).to_contain_text("Valéria Baráthová")
    expect(page.locator("#aktualny-nahlad-container")).to_contain_text("21.01.2010")
    expect(page.locator("#aktualny-nahlad-container")).to_contain_text("Juríčková 896/2, 03657, Košariská")
    expect(page.get_by_role("rowgroup")).to_contain_text("meno a priezvisko:")
    expect(page.get_by_role("rowgroup")).to_contain_text("Valéria Baráthová")
    expect(page.get_by_role("rowgroup")).to_contain_text("dátum narodenia:")
    expect(page.get_by_role("rowgroup")).to_contain_text("21.01.2010")
    expect(page.get_by_role("rowgroup")).to_contain_text("trvalý pobyt:")
    expect(page.get_by_role("rowgroup")).to_contain_text("Juríčková 896/2, 03657, Košariská")
    expect(page.locator("#aktualny-nahlad-container")).to_contain_text("Odôvodnenie:")
    expect(page.locator("#aktualny-nahlad-container")).to_contain_text("Poučenie:")
    expect(page.locator("#aktualny-nahlad-container")).to_contain_text("Stredná škola pre AT")
    expect(page.locator("#aktualny-nahlad-container")).to_contain_text("riaditeľ")
    expect(page.locator("#aktualny-nahlad-container")).to_contain_text("Rozhodnutie sa doručuje:")
    expect(page.locator("#aktualny-nahlad-container")).to_contain_text("Tomáš Lukáč, Ražná 58/232, 01508, Košariská")

    rozhodnutie.autorizovat_a_vygenerovat()

    expect(page.locator("#podpis-success-title")).to_contain_text("Generovanie 1 rozhodnutia bolo spustené.")
    expect(page.locator("#podpis-success-desc")).to_contain_text("Tento proces môže v závislosti od počtu vybraných rozhodnutí trvať niekoľko minút až hodín.")
    expect(page.locator("#podpis-success-dolozka")).to_contain_text("Rozhodnutia budú mať po dokončení automaticky vygenerované doložky o autorizácii.")

    rozhodnutie.click_spat_na_rozhodnutia()
    rozhodnutie.wait_for_generation_complete("Baráthová")

    expect(page.locator("#sub-riaditel-rozhodnutia")).not_to_contain_text("Prebieha generovanie rozhodnutia.")
    expect(page.locator("#sub-riaditel-rozhodnutia")).to_contain_text("Pre rozhodnutie nebolo žiadané doručenie poštou ani do eDesk.")
    expect(page.locator("#sub-riaditel-rozhodnutia")).to_contain_text("Rozhodnuté o prijatí")


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_odvolanie_SS(page: Page) -> None:
    login = LoginPage(page)
    rozhodnutie = RozhodnutieSS(page)
    mail = Mail()
    den, mesiac, rok = helper.aktualny_datum()

    login.login_as_riaditel(username_riad, password_riad, "910021624")
    rozhodnutie.navigate_to_rozhodnutia()
    rozhodnutie.search("Baráthová")
    rozhodnutie.select_first()
    rozhodnutie.click_zaevidovat_odvolanie()

    expect(page.locator("#zaevidovat-odvolanie-title")).to_contain_text("Zaevidovať odvolanie proti rozhodnutiu o prijatí")
    expect(page.locator("#zaevidovat-odvolanie-meno")).to_contain_text("Baráthová Valéria")

    rozhodnutie.fill_odvolanie_form(den, mesiac, rok)
    rozhodnutie.submit_odvolanie()

    expect(page.locator("#sub-riaditel-rozhodnutia")).to_contain_text("Odvolanie")
    expect(page.locator("#sub-riaditel-rozhodnutia")).to_contain_text("Dôvod odvolania")
    expect(page.locator("#sub-riaditel-rozhodnutia")).to_contain_text(re.compile(r"Zostávajú \d+ dn"))

    mail_odvolanie = helper.cleanup_email_text(mail.get_last_email_text("imap.gmail.com", mailuser, mailpw))
    expected_mail_odvolanie = (
        "Vážený/á pán/pani Tomáš Lukáč, riaditeľ školy Stredná škola pre AT zaevidoval v systéme odvolanie voči "
        "rozhodnutiu o prijímacom konaní, ktoré ste podali k prihláške P-2026-21988.01 pre Valéria Baráthová 21.01.2010. "
        "O ďalšom postupe Vás bude škola informovať po vyhodnotení odvolania. S pozdravom Tím elektronických prihlášok "
        "MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe "
        "Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň.\""
    )
    assert mail_odvolanie == expected_mail_odvolanie, (
        f"Obsah e-mailu po zaevidovaní odvolania nezodpovedá očakávaniu.\n\n=== EXPECTED ===\n{expected_mail_odvolanie}\n\n=== ACTUAL ===\n{mail_odvolanie}"
    )

    rozhodnutie.select_first()
    rozhodnutie.click_spatvzatie_odvolania()

    expect(page.locator("body")).to_contain_text("Späťvzatie odvolania")
    expect(page.locator("body")).to_contain_text("Riaditeľ má možnosť opakovane vziať odvolanie späť a vytvoriť nové. Túto funkcionalitu je možné využiť na opravu už podaného odvolania. Naozaj chcete potvrdiť späťvzatie odvolania?")

    rozhodnutie.confirm_spatvzatie()

    expect(page.locator("#riaditel-home-page")).to_contain_text("Späťvzatie odvolania proti rozhodnutiu o prijatí/neprijatí uchádzača bolo úspešne zaevidované.")
    expect(page.locator("#sub-riaditel-rozhodnutia")).to_contain_text("-")

    mail_spatvzatie = helper.cleanup_email_text(mail.get_last_email_text("imap.gmail.com", mailuser, mailpw))
    expected_mail_spatvzatie = (
        "Vážený/á pán/pani Tomáš Lukáč, Odvolanie k prihláške P-2026-21988.01 pre Valéria Baráthová 21.01.2010 bolo "
        "vzaté späť riaditeľom školy Stredná škola pre AT. Odvolacie konanie bolo zastavené. S pozdravom Tím "
        "elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky "
        "do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň.\""
    )
    assert mail_spatvzatie == expected_mail_spatvzatie, (
        f"Obsah e-mailu po späťvzatí odvolania nezodpovedá očakávaniu.\n\n=== EXPECTED ===\n{expected_mail_spatvzatie}\n\n=== ACTUAL ===\n{mail_spatvzatie}"
    )
