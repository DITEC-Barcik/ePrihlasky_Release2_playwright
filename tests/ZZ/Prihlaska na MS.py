import os
import re
import pytest
import utils.data_helper as Data

from utils.helpers import Helper
from utils.mail_helper import Mail
from pages.logout_page import LogoutPage
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.prihlaska_MS_page import PrihlaskaMS
from pages.prilohy_MS_page import PrilohyMS


mailuser = os.getenv("GMAIL_USERNAME")
mailpw = os.getenv("GMAIL_APP_PASSWORD")
username = os.getenv("EPRIHLASKY_ZZ_USERNAME")
password = os.getenv("EPRIHLASKY_ZZ_PASSWORD")
username_riad = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password_riad = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


@pytest.fixture(scope="module")
def person_data():
    return Data.generate_unique_person(min_age=4, max_age=5)


def _expect_text(locator, text, message: str) -> None:
    expect(locator, message).to_contain_text(text)


def _expect_visible(locator, message: str) -> None:
    expect(locator, message).to_be_visible()


def _expect_url(page: Page, pattern: str, message: str, timeout: int = 60000) -> None:
    expect(page, message).to_have_url(re.compile(pattern), timeout=timeout)


def _assert_equal(actual: str, expected: str, message: str) -> None:
    assert actual == expected, (
        f"{message}\n\n=== EXPECTED ===\n{expected}\n\n=== ACTUAL ===\n{actual}"
    )


def _expect_ms_summary(page: Page, data, helper: Helper) -> None:
    summary = page.locator("#suhrnny-prehlad")

    _expect_text(summary, re.compile(r"P-2026-.+"), "V súhrnnom prehľade chýba identifikátor prihlášky.")
    _expect_text(summary, "2027/2028", "V súhrnnom prehľade chýba školský rok.")
    _expect_text(summary, data.meno, "V súhrnnom prehľade chýba meno dieťaťa.")
    _expect_text(summary, data.priezvisko, "V súhrnnom prehľade chýba priezvisko dieťaťa.")
    _expect_text(summary, data.rodne_cislo, "V súhrnnom prehľade chýba rodné číslo dieťaťa.")
    _expect_text(
        summary,
        helper.rc_to_datum_narodenia(data.rodne_cislo),
        "V súhrnnom prehľade chýba dátum narodenia dieťaťa."
    )

    pohlavie = "žena" if helper.get_pohlavie(data.rodne_cislo) == "ženské" else "muž"
    _expect_text(summary, pohlavie, "V súhrnnom prehľade chýba pohlavie dieťaťa.")

    _expect_text(summary, "Slovensko", "V súhrnnom prehľade chýba miesto narodenia.")
    _expect_text(summary, "slovenská", "V súhrnnom prehľade chýba národnosť.")
    _expect_text(summary, "Slovenská republika", "V súhrnnom prehľade chýba štátna príslušnosť.")
    _expect_text(summary, "slovenský", "V súhrnnom prehľade chýba materinský jazyk.")
    # Pôvodne: "Debraďská 999/21, 54231, Bobot, ..." - po prechode na register adries
    # sa vyberá adresa z číselníka a súhrn ju zobrazuje bez obce.
    _expect_text(
        summary,
        "Prvej SNR 33/23, 90701, Slovenská republika",
        "V súhrnnom prehľade chýba adresa dieťaťa."
    )
    _expect_text(summary, "Celodennú výchovu a vzdelávanie", "V súhrnnom prehľade chýba typ výchovy.")
    _expect_text(summary, "07.09.2026", "V súhrnnom prehľade chýba požadovaný dátum prijatia.")
    _expect_text(summary, "ŠVVP", "V súhrnnom prehľade chýba poznámka ŠVVP.")


def _expect_ms_school_and_guardians(page: Page) -> None:
    _expect_text(page.locator("#skoly"), "Materská škola pre AT", "V sekcii školy chýba názov školy.")
    _expect_text(page.locator("#skoly"), "Balková 98/8, 36578 Banská Bystrica", "V sekcii školy chýba adresa školy.")
    _expect_text(page.locator("#skoly"), "slovenský", "V sekcii školy chýba vyučovací jazyk.")

    guardians = page.locator("#zastupcovia")
    _expect_text(guardians, "Mária", "V sekcii zástupcov chýba meno 1. zákonného zástupcu.")
    _expect_text(guardians, "Bartošová", "V sekcii zástupcov chýba priezvisko 1. zákonného zástupcu.")
    _expect_text(guardians, "855215/3830", "V sekcii zástupcov chýba rodné číslo 1. zákonného zástupcu.")
    _expect_text(guardians, "15.02.1985", "V sekcii zástupcov chýba dátum narodenia 1. zákonného zástupcu.")
    _expect_text(
        guardians,
        "Prvej SNR 33/23, 90701, Slovenská republika",
        "V sekcii zástupcov chýba adresa 1. zákonného zástupcu."
    )
    _expect_text(guardians, "katalontest987@gmail.com", "V sekcii zástupcov chýba e-mail 1. zákonného zástupcu.")
    _expect_text(guardians, "+421999888777", "V sekcii zástupcov chýba telefón 1. zákonného zástupcu.")
    _expect_text(guardians, "Nie", "V sekcii zástupcov chýba hodnota 'Nie'.")

    _expect_text(guardians, "Fero", "V sekcii zástupcov chýba meno 2. zákonného zástupcu.")
    _expect_text(guardians, "Bartoš", "V sekcii zástupcov chýba priezvisko 2. zákonného zástupcu.")
    _expect_text(guardians, "860224/7005", "V sekcii zástupcov chýba rodné číslo 2. zákonného zástupcu.")
    _expect_text(guardians, "24.02.1986", "V sekcii zástupcov chýba dátum narodenia 2. zákonného zástupcu.")
    _expect_text(guardians, "mail@tst.net", "V sekcii zástupcov chýba e-mail 2. zákonného zástupcu.")
    _expect_text(guardians, "+421954856321", "V sekcii zástupcov chýba telefón 2. zákonného zástupcu.")
    _expect_text(guardians, "Áno", "V sekcii zástupcov chýba hodnota 'Áno'.")


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_prihlaska_na_MS(page: Page, person_data) -> None:
    data = person_data
    helper = Helper()
    login = LoginPage(page)
    logout = LogoutPage(page)
    prihlaska = PrihlaskaMS(page)

    login.login_as_zakonny_zastupca(username, password)
    prihlaska.click_on_vytvorit_prihlasku()
    prihlaska.step_1_pridat_dieta(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska.step_2_SVVP()
    prihlaska.step_3_vyber_skoly("materská škola pre AT")
    prihlaska.step_4_ZZ()
    prihlaska.step_5_prilohy()

    _expect_ms_summary(page, data, helper)
    _expect_ms_school_and_guardians(page)
    _expect_visible(page.locator(".prilohaItem").first, "V súhrne sa nezobrazila nahraná príloha.")

    prihlaska.odoslat_prihlasku_MS()

    _expect_url(
        page,
        r".*/Prihlaska-odoslana.*",
        "Po odoslaní prihlášky na MŠ sa neotvorila stránka Prihláška odoslaná."
    )
    _expect_text(
        page.locator("h1"),
        "Prihláška bola úspešne odoslaná!",
        "Po odoslaní prihlášky sa nezobrazil úspešný nadpis."
    )

    logout.logout()

    login.login_as_riaditel(username_riad, password_riad, "910021626")
    _expect_url(
        page,
        r".*/Riaditel.*",
        "Po prihlásení riaditeľa sa neotvorila stránka riaditeľa."
    )

    prihlaska.vyhladaj_prihlasku(data.meno, data.priezvisko)

    detail = page.locator("#detail-prihlasky-riad-MS-ZS-content")
    _expect_text(detail, "Elektronicky", "V detaile prihlášky chýba spôsob podania 'Elektronicky'.")
    _expect_text(detail, "Podaná", "V detaile prihlášky chýba stav 'Podaná'.")
    _expect_text(page.locator("#dietaMeno"), data.meno, "V detaile prihlášky chýba meno dieťaťa.")
    _expect_text(page.locator("#dietaPriezvisko"), data.priezvisko, "V detaile prihlášky chýba priezvisko dieťaťa.")
    _expect_text(page.locator("#dietaRodneCislo"), data.rodne_cislo, "V detaile prihlášky chýba rodné číslo dieťaťa.")


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_doplnenie_prilohy_na_MS(page: Page, person_data) -> None:
    data = person_data
    helper = Helper()
    mail = Mail()
    login = LoginPage(page)
    logout = LogoutPage(page)
    prihlaska = PrihlaskaMS(page)
    prilohy = PrilohyMS(page)

    login.login_as_riaditel(username_riad, password_riad, "910021626")
    prihlaska.vyhladaj_prihlasku(data.meno, data.priezvisko)

    _expect_text(
        page.locator("#detail-prihlasky-riad-MS-ZS-content"),
        "Podaná",
        "Pred prácou s prílohami nemá prihláška stav 'Podaná'."
    )

    identifikator = page.locator(".prihlaskaIdentifikator").text_content()

    prilohy.vyziadanie_prilohy_MS()
    prilohy.odvolanie_prilohy_MS()

    odvolanie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    odvolanie_prilohy = helper.cleanup_email_text(odvolanie_prilohy)

    expected_cancel = (
        f"Vážený/á pán/pani Mária Bartošová, radi by sme Vás informovali, že požiadavka na doloženie "
        f"dodatočných dokumentov príloh k Vašej prihláške zaevidovanej v portáli Elektronické prihlášky do škôl "
        f"bola zrušená. Nie je teda potrebné dodatočne nahrávať žiadne ďalšie prílohy k prihláške pre: "
        f"{data.meno} {data.priezvisko} nar. {helper.rc_to_datum_narodenia(data.rodne_cislo)}. "
        f"Ak ste už zadali dokumenty na základe predchádzajúceho odkazu, upozorňujeme, že tento odkaz je už neaktívny. "
        f"V prípade akýchkoľvek otázok nás neváhajte kontaktovať. S pozdravom Tím elektronických prihlášok MŠVVaM SR "
        f"Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe "
        f"Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň.\""
    )
    _assert_equal(
        odvolanie_prilohy,
        expected_cancel,
        "Obsah e-mailu o odvolaní požiadavky na prílohu nezodpovedá očakávaniu."
    )

    _expect_text(
        page.locator("#skoly"),
        "info Výzva odvolaná",
        "Po odvolaní výzvy sa v detaile prihlášky nezobrazuje stav 'Výzva odvolaná'."
    )

    prilohy.vyziadanie_prilohy_MS()

    vyziadanie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyziadanie_prilohy = helper.cleanup_email_text(vyziadanie_prilohy)

    expected_request = (
        f"Vážený/á pán/pani Mária Bartošová, pri kontrole prihlášky {identifikator} pre školu "
        f"Materská škola pre AT pre {data.meno} {data.priezvisko} sme zistili, že je potrebné doložiť "
        f"nasledujúcu prílohu: Rozhodnutie súdu z dôvodu že \" Odvolanie prílohy. \". Prosíme Vás o doplnenie "
        f"požadovanej prílohy k prihláške. Doplnenie príloh môžete vykonať prostredníctvom portálu Elektronické "
        f"prihlášky do škôl: Link na prihlásenie Ak ešte nemáte vytvorené konto, zaregistrujte sa prostredníctvom "
        f"odkazu: Registrovať sa Po registrácii a prihlásení sa dostanete do sekcie Moje prihlášky, kde nájdete možnosť "
        f"pridať existujúcu prihlášku do svojho konta. Na pridanie prihlášky zadajte tento identifikátor prihlášky: "
        f"{identifikator} Po pridaní prihlášky do konta budete môcť sledovať jej stav, doplniť požadované prílohy "
        f"a komunikovať so školou. V prípade, že už konto v portáli máte, prihláste sa a pokračujte podľa pokynov "
        f"v portáli. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom "
        f"Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže "
        f"Slovenskej republiky. Neodpovedajte naň."
    )
    _assert_equal(
        vyziadanie_prilohy,
        expected_request,
        "Obsah e-mailu so žiadosťou o doplnenie prílohy nezodpovedá očakávaniu."
    )

    _expect_text(
        page.locator("#message-box"),
        "Žiadosť o doplnenie prílohy bola úspešne odoslaná",
        "Po vyžiadaní prílohy sa nezobrazila úspešná hláška."
    )
    _expect_text(
        page.locator("#skoly"),
        "Riaditeľ školy Materská škola pre AT požadoval ďalšie prílohy.",
        "V detaile prihlášky chýba informácia o požadovaných ďalších prílohách."
    )
    _expect_text(
        page.locator("#skoly"),
        "Neúplná",
        "Po vyžiadaní prílohy nemá prihláška stav 'Neúplná'."
    )

    logout.logout()
    login.login_as_zakonny_zastupca(username, password)

    _expect_text(
        page.locator("#moje-prihlasky"),
        "Nahrajte prílohy",
        "V zozname mojich prihlášok chýba výzva na nahratie príloh."
    )
    _expect_text(
        page.locator("#moje-prihlasky"),
        "Riaditeľ materskej školy požaduje doplnenie príloh.",
        "V zozname mojich prihlášok chýba informácia o požadovanom doplnení príloh."
    )

    prilohy.pridat_prilohu_MS()

    prijatie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    prijatie_prilohy = helper.cleanup_email_text(prijatie_prilohy)

    expected_received = (
        f"Vážený/á pán/pani/ Mária Bartošová, dovoľujeme si Vás informovať, že k Vašej prihláške "
        f"do Materská škola pre AT pre {data.meno} {data.priezvisko}, zaevidovanej v elektronickom portáli "
        f"prihlášok bola doručená príloha s názvom Rozhodnutie súdu. Doručenú prílohu si prosím starostlivo "
        f"skontrolujte prihlásením sa na portáli Elektronických prihlášok v detaile prihlášky, alebo v prílohe "
        f"tohto mailu. Prihlásením sa na portáli zároveň získate aj ďalšie informácie o stave Vašej prihlášky "
        f"a priebehu jej spracovania. Link na prihlásenie S pozdravom Tím elektronických prihlášok MŠVVaM SR "
        f"Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe "
        f"Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň.\""
    )
    _assert_equal(
        prijatie_prilohy,
        expected_received,
        "Obsah e-mailu o prijatí prílohy nezodpovedá očakávaniu."
    )

    _expect_text(
        page.locator("#pridat-prilohy"),
        "Dokumenty ste úspešne nahrali",
        "Po nahratí prílohy sa nezobrazila úspešná hláška."
    )

    logout.logout()
    login.login_as_riaditel(username_riad, password_riad, "910021626")
    prihlaska.vyhladaj_prihlasku(data.meno, data.priezvisko)

    _expect_text(
        page.locator("#detail-prihlasky-riad-MS-ZS-content"),
        "Doplnená",
        "Po doplnení príloh nemá prihláška stav 'Doplnená'."
    )
    _expect_visible(
        page.get_by_text("Priložené dokumenty: article"),
        "V detaile prihlášky sa nezobrazujú priložené dokumenty."
    )
    _expect_text(
        page.locator("#skoly"),
        "Doplnená",
        "V sekcii školy sa nezobrazuje stav 'Doplnená'."
    )