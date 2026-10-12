import os
import re
import pytest
import utils.data_helper as Data

from utils.helpers import Helper
from utils.mail_helper import Mail
from pages.logout_page import LogoutPage
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.prihlaska_SS_page import PrihlaskaSS
from pages.papierova_prihlaska_SS_page import PapierovaPrihlaskaSS
from pages.konflikt_SS_page import KofliktSS


username = os.getenv("EPRIHLASKY_ZZ_USERNAME")
password = os.getenv("EPRIHLASKY_ZZ_PASSWORD")
username_riad = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password_riad = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")
mailuser = os.getenv("GMAIL_USERNAME")
mailpw = os.getenv("GMAIL_APP_PASSWORD")


@pytest.fixture(scope="module")
def person_data():
    return Data.generate_unique_person(min_age=15, max_age=17)


def _expect_text(locator, text, message: str) -> None:
    expect(locator, message).to_contain_text(text)


def _expect_visible(locator, message: str) -> None:
    expect(locator, message).to_be_visible()


def _expect_url(page: Page, pattern: str, message: str, timeout: int = 60000) -> None:
    expect(page, message).to_have_url(re.compile(pattern), timeout=timeout)


def _assert_in_options(actual: str, expected_options: list[str], message: str) -> None:
    assert actual in expected_options, (
        f"{message}\n\n=== ACTUAL ===\n{actual}\n\n=== EXPECTED OPTIONS ===\n"
        + "\n--- OR ---\n".join(expected_options)
    )


@pytest.mark.regres2kolo
def test_vytvorenie_konfliktu_2_kolo(page: Page, person_data) -> None:
    data = person_data
    helper = Helper()
    login = LoginPage(page)
    logout = LogoutPage(page)
    prihlaska = PrihlaskaSS(page)
    prihlaska_riad = PapierovaPrihlaskaSS(page)

    login.login_as_zakonny_zastupca(username, password)

    prihlaska.click_on_vytvorit_prihlasku()
    prihlaska.pridat_dieta(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska.step_1_vyber_ziaka()
    prihlaska.step_2_SVVP()
    prihlaska.step_3_vyber_skoly("pre AT")
    prihlaska.step_4_ZZ()
    prihlaska.step_5_ziak_navsteva_skoly()
    prihlaska.step_6_znamky()
    prihlaska.step_7_sutaze()
    prihlaska.step_8_prilohy()
    prihlaska.click_on_odoslat_prihlasku()
    prihlaska.click_on_potvrdit_odoslanie()

    _expect_url(
        page,
        r".*/Prihlaska-odoslana.*",
        "Po odoslaní elektronickej prihlášky sa neotvorila stránka 'Prihláška odoslaná'."
    )

    prihlaska.click_on_prejst_na_prihlasky()

    _expect_url(
        page,
        r".*/Prihlasky.*",
        "Po kliknutí na prechod na prihlášky sa neotvorila stránka so zoznamom prihlášok."
    )

    logout.logout()

    login.login_as_riaditel(username_riad, password_riad, "910021624")

    den, mesiac, rok = helper.aktualny_datum()

    prihlaska_riad.click_on_pridaj_prihlasku()
    prihlaska_riad.step_1_osobne_udaje(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska_riad.step_2_SVVP()
    prihlaska_riad.step_3_vyber_skoly()
    prihlaska_riad.step_4_ZZ()
    prihlaska_riad.step_5_navsteva_ZS()
    prihlaska_riad.step_6_znamky()
    prihlaska_riad.step_7_sutaze()
    prihlaska_riad.step_8_prilohy()
    prihlaska_riad.step_9_ostatne_udaje(den, mesiac, rok)
    prihlaska_riad.click_on_odoslat_prihlasku()

    _expect_url(
        page,
        r".*/Riaditel.*",
        "Po odoslaní papierovej prihlášky sa používateľ nevrátil na stránku riaditeľa."
    )


@pytest.mark.regres2kolo
def test_vyriesenie_konfliktu_2_kolo(page: Page) -> None:
    login = LoginPage(page)
    mail = Mail()
    helper = Helper()
    konflikt = KofliktSS(page)

    login.login_as_riaditel(username_riad, password_riad, "910021624")
    konflikt.najdi_prihlasku_v_konflikte()

    konflikt_info = page.locator("#info-panel-red-prihlaska-v-konflikte-riad-ss")
    _expect_text(
        konflikt_info,
        "Táto prihláška je v stave - V konflikte.",
        "Na detaile prihlášky sa nezobrazuje červený info panel o konflikte."
    )
    _expect_text(
        konflikt_info,
        "Pre toto dieťa existuje v systéme viacero prihlášok.",
        "V červenom info paneli chýba informácia o existencii viacerých prihlášok."
    )
    _expect_text(
        konflikt_info,
        "Vyzvite zákonného zástupcu na výber jednej verzie.",
        "V červenom info paneli chýba výzva na kontaktovanie zákonného zástupcu."
    )
    _expect_text(
        konflikt_info,
        "Bez vyriešenia konfliktu nie je možné prihlášku ďalej spracovávať.",
        "V červenom info paneli chýba upozornenie, že prihlášku nemožno ďalej spracovať."
    )

    detail = page.locator("#detail-prihlasky-riad-SS-content")
    _expect_text(detail, "Elektronicky", "V detaile konfliktnej prihlášky chýba spôsob podania 'Elektronicky'.")
    _expect_text(detail, "V konflikte", "V detaile konfliktnej prihlášky chýba stav 'V konflikte'.")

    meno = page.locator("#dietaMeno").text_content()
    priezvisko = page.locator("#dietaPriezvisko").text_content()
    identifikator = page.locator(".prihlaskaIdentifikator").text_content()
    datum_narodenia = page.locator("#dietaDatumNarodenia").text_content()

    konflikt.click_on_vyzva_na_vyriesenie_konfliktu()

    _expect_text(
        page.locator("body"),
        "Pre dieťa existuje viac ako jedna prihláška.",
        "Po otvorení výzvy na vyriešenie konfliktu chýba úvodná informácia o duplicite prihlášok."
    )
    _expect_text(
        page.locator("body"),
        "Mária Bartošová",
        "V dialógu výzvy na vyriešenie konfliktu chýba zákonný zástupca Mária Bartošová."
    )
    _expect_text(
        page.locator("body"),
        "Demeter Varga",
        "V dialógu výzvy na vyriešenie konfliktu chýba zákonný zástupca Demeter Varga."
    )

    konflikt.click_on_odoslat_vyzvu("Výzva na vyriešenie konfliktu.")

    vyzva_konflikt = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyzva_konflikt = helper.cleanup_email_text(vyzva_konflikt)

    expected_demeter = (
        f"Vážený/á pán/pani Demeter Varga, v systéme bolo zistené, že pre žiaka {meno} {priezvisko} nar. {datum_narodenia} "
        f"boli podané viaceré prihlášky. Riaditeľ školy Stredná škola pre AT Vás týmto vyzýva, aby ste ho bezodkladne "
        f"kontaktovali a informovali, ktorú prihlášku si želáte ponechať ako platnú. Sprievodná správa od riaditeľa: "
        f"Výzva na vyriešenie konfliktu. Bez vyriešenia tohto konfliktu nebudú prihlášky ďalej spracované. "
        f"S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom "
        f"Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže "
        f"Slovenskej republiky. Neodpovedajte naň."
    )
    expected_maria = (
        f"Vážený/á pán/pani Mária Bartošová, v systéme bolo zistené, že pre žiaka {meno} {priezvisko} nar. {datum_narodenia} "
        f"boli podané viaceré prihlášky. Riaditeľ školy Stredná škola pre AT Vás týmto vyzýva, aby ste ho bezodkladne "
        f"kontaktovali a informovali, ktorú prihlášku si želáte ponechať ako platnú. Sprievodná správa od riaditeľa: "
        f"Výzva na vyriešenie konfliktu. Bez vyriešenia tohto konfliktu nebudú prihlášky ďalej spracované. "
        f"S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom "
        f"Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže "
        f"Slovenskej republiky. Neodpovedajte naň."
    )
    _assert_in_options(
        vyzva_konflikt,
        [expected_demeter, expected_maria],
        "Obsah e-mailu s výzvou na vyriešenie konfliktu nezodpovedá očakávaniu."
    )

    _expect_text(
        page.locator("#duplicitne-prihlasky"),
        "Riaditeľ školy Stredná škola pre AT zaslal výzvu na riešenie konfliktu prihlášok.",
        "Po odoslaní výzvy sa v sekcii duplicitných prihlášok nezobrazila informácia o odoslanej výzve."
    )
    _expect_text(
        detail,
        "V konflikte",
        "Po odoslaní výzvy sa stav prihlášky neočakávane zmenil z 'V konflikte'."
    )

    konflikt.click_on_vyriesit_konflikt()

    _expect_text(
        page.locator("#vyriesit-konflikt-title"),
        "Vyriešiť konflikt",
        "Po otvorení formulára na riešenie konfliktu chýba správny nadpis."
    )
    _expect_text(
        page.locator("body"),
        "Po označení prihlášky ako aktívnej sa automaticky zneaktivnia všetky duplicitné prihlášky pre toto dieťa na všetkých školách.",
        "V dialógu riešenia konfliktu chýba upozornenie o zneaktívnení duplicitných prihlášok."
    )

    konflikt.click_on_odoslat_konfikt("Vyriešiť konflikt.")

    vyriesenie_konflikt = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyriesenie_konflikt = helper.cleanup_email_text(vyriesenie_konflikt)

    identifikator1 = helper.inkrementuj_identifikator(identifikator)

    expected_vyriesenie_maria = (
        f"Vážený/á pán/pani Mária Bartošová, Prihláška {identifikator} bola v konflikte s prihláškou/prihláškami "
        f"{identifikator}, {identifikator1}. Konflikt bol vyriešený . V systéme bude ďalej evidovaná len prihláška "
        f"{identifikator}. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky "
        f"portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže "
        f"Slovenskej republiky. Neodpovedajte naň."
    )
    expected_vyriesenie_demeter = (
        f"Vážený/á pán/pani Demeter Varga, riaditeľ školy Stredná škola pre AT vyriešil konflikt viacerých prihlášok "
        f"podaných pre žiaka {meno} {priezvisko} nar. {datum_narodenia}. Ako aktívna bola označená prihláška s "
        f"identifikátorom {identifikator}, ktorú podal/podala Mária Bartošová. Ostatné prihlášky boli označené ako "
        f"“Konflikt - neaktívna” a nebudú ďalej spracované. Stav prihlášky si môžete overiť po prihlásení do portálu "
        f"Elektronické prihlášky: Link na prihlásenie S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email "
        f"bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, "
        f"výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
    )
    _assert_in_options(
        vyriesenie_konflikt,
        [expected_vyriesenie_maria, expected_vyriesenie_demeter],
        "Obsah e-mailu o vyriešení konfliktu nezodpovedá očakávaniu."
    )

    _expect_text(
        page.get_by_role("strong"),
        "Duplicita prihlášok úspešne vyriešená",
        "Po vyriešení konfliktu sa nezobrazila úspešná hláška o duplicite prihlášok."
    )

    aktivna_info = page.locator("#info-panel-blue-prihlaska-aktivna")
    _expect_text(
        aktivna_info,
        "Prihláška bola označená ako aktívna riaditeľom školy 910021624 Stredná škola pre AT",
        "V modrom info paneli chýba informácia o aktívnej prihláške."
    )
    _expect_text(
        aktivna_info,
        "Ak je potrebné označiť inú prihlášku ako aktívnu, kontaktujte riaditeľa uvedenej školy.",
        "V modrom info paneli chýba informácia o ďalšom postupe pri zmene aktívnej prihlášky."
    )

    _expect_text(
        page.locator("#duplicitne-prihlasky"),
        f"Pre žiaka {meno} {priezvisko} bol vyriešený konflikt.",
        "V sekcii duplicitných prihlášok chýba potvrdenie o vyriešení konfliktu."
    )
    _expect_text(
        page.locator(".stavPrihlasky"),
        "V spracovaní",
        "Po vyriešení konfliktu nemá prihláška očakávaný stav 'V spracovaní'."
    )