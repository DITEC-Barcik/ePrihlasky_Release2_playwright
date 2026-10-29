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
    expect(locator, message).to_contain_text(text, timeout=60000)


def _expect_url(page: Page, pattern: str, message: str, timeout: int = 60000) -> None:
    expect(page, message).to_have_url(re.compile(pattern), timeout=timeout)


def _assert_in_options(actual: str, options: list[str], message: str) -> None:
    assert actual in options, (
        f"{message}\n\n=== ACTUAL ===\n{actual}\n\n=== EXPECTED OPTIONS ===\n"
        + "\n---\n".join(options)
    )


def _create_electronic_ss_application_round_1(page: Page, data) -> None:
    logout = LogoutPage(page)
    login = LoginPage(page)
    prihlaska = PrihlaskaSS(page)

    login.login_as_zakonny_zastupca(username, password)
    prihlaska.click_on_vytvorit_prihlasku_1_kolo()
    prihlaska.pridat_dieta(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska.step_1_vyber_ziaka()
    prihlaska.step_2_SVVP()
    prihlaska.step_3_vyber_skoly_1_kolo("škola pre AT")
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
        "Po odoslaní elektronickej SS prihlášky sa neotvorila stránka Prihláška odoslaná."
    )

    logout.logout()


def _create_paper_ss_application_round_1(page: Page, data, helper: Helper) -> None:
    login = LoginPage(page)
    prihlaska_riad = PapierovaPrihlaskaSS(page)
    den, mesiac, rok = helper.aktualny_datum()

    login.login_as_riaditel(username_riad, password_riad, "910021624")
    prihlaska_riad.click_on_pridaj_prihlasku_1_kolo()
    prihlaska_riad.step_1_osobne_udaje(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska_riad.step_2_SVVP()
    prihlaska_riad.step_3_vyber_skoly_1_kolo()
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
        "Po odoslaní papierovej SS prihlášky sa nevrátila stránka riaditeľa."
    )


def _build_conflict_notice_options(meno: str, priezvisko: str, datum_narodenia: str) -> list[str]:
    return [
        (
            f"Vážený/á pán/pani Demeter Varga, v systéme bolo zistené, že pre žiaka {meno} {priezvisko} "
            f"nar. {datum_narodenia} boli podané viaceré prihlášky. Riaditeľ školy Stredná škola pre AT "
            f"Vás týmto vyzýva, aby ste ho bezodkladne kontaktovali a informovali, ktorú prihlášku si želáte "
            f"ponechať ako platnú. Sprievodná správa od riaditeľa: Výzva na vyriešenie konfliktu. Bez vyriešenia "
            f"tohto konfliktu nebudú prihlášky ďalej spracované. S pozdravom Tím elektronických prihlášok "
            f"MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, "
            f"ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. "
            f"Neodpovedajte naň."
        ),
        (
            f"Vážený/á pán/pani Mária Bartošová, v systéme bolo zistené, že pre žiaka {meno} {priezvisko} "
            f"nar. {datum_narodenia} boli podané viaceré prihlášky. Riaditeľ školy Stredná škola pre AT "
            f"Vás týmto vyzýva, aby ste ho bezodkladne kontaktovali a informovali, ktorú prihlášku si želáte "
            f"ponechať ako platnú. Sprievodná správa od riaditeľa: Výzva na vyriešenie konfliktu. Bez vyriešenia "
            f"tohto konfliktu nebudú prihlášky ďalej spracované. S pozdravom Tím elektronických prihlášok "
            f"MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, "
            f"ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. "
            f"Neodpovedajte naň."
        ),
    ]


def _build_resolution_options(
    identifikator: str,
    identifikator1: str,
    meno: str,
    priezvisko: str,
    datum_narodenia: str,
) -> list[str]:
    return [
        (
            f"Vážený/á pán/pani Mária Bartošová, Prihláška {identifikator} bola v konflikte "
            f"s prihláškou/prihláškami {identifikator}, {identifikator1}. Konflikt bol vyriešený . "
            f"V systéme bude ďalej evidovaná len prihláška {identifikator}. S pozdravom Tím elektronických "
            f"prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky "
            f"do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. "
            f"Neodpovedajte naň."
        ),
        (
            f"Vážený/á pán/pani Demeter Varga, riaditeľ školy Stredná škola pre AT vyriešil konflikt "
            f"viacerých prihlášok podaných pre žiaka {meno} {priezvisko} nar. {datum_narodenia}. "
            f"Ako aktívna bola označená prihláška s identifikátorom {identifikator}, ktorú podal/podala "
            f"Mária Bartošová. Ostatné prihlášky boli označené ako “Konflikt - neaktívna” a nebudú ďalej "
            f"spracované. Stav prihlášky si môžete overiť po prihlásení do portálu Elektronické prihlášky: "
            f"Link na prihlásenie S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol "
            f"generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva "
            f"školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
        ),
    ]


@pytest.mark.regres1kolo
def test_vytvorenie_konfliktu_na_SS_1_kolo(page: Page, person_data) -> None:
    helper = Helper()
    data = person_data

    _create_electronic_ss_application_round_1(page, data)
    _create_paper_ss_application_round_1(page, data, helper)


@pytest.mark.regres1kolo
def test_vyriesenie_konfliktu_1_kolo(page: Page, person_data) -> None:
    login = LoginPage(page)
    mail = Mail()
    helper = Helper()
    konflikt = KofliktSS(page)

    login.login_as_riaditel(username_riad, password_riad, "910021624")
    konflikt.najdi_prihlasku_v_konflikte_1_kolo(person_data.meno, person_data.priezvisko)

    conflict_panel = page.locator("#info-panel-red-prihlaska-v-konflikte-riad-ss")
    _expect_text(
        conflict_panel,
        "Táto prihláška je v stave - V konflikte.",
        "Chýba informácia, že SS prihláška je v konflikte."
    )
    _expect_text(
        conflict_panel,
        "Pre toto dieťa existuje v systéme viacero prihlášok.",
        "V červenom paneli chýba informácia o viacerých prihláškach."
    )
    _expect_text(
        conflict_panel,
        "Vyzvite zákonného zástupcu na výber jednej verzie.",
        "V červenom paneli chýba pokyn na výzvu zákonnému zástupcovi."
    )
    _expect_text(
        conflict_panel,
        "Následne vyriešte konflikt označením jednej prihlášky ako aktívnej.",
        "V červenom paneli chýba pokyn na vyriešenie konfliktu."
    )
    _expect_text(
        conflict_panel,
        "Bez vyriešenia konfliktu nie je možné prihlášku ďalej spracovávať.",
        "V červenom paneli chýba upozornenie na nemožnosť ďalšieho spracovania."
    )

    detail = page.locator("#detail-prihlasky-riad-SS-content")
    _expect_text(detail, "Elektronicky", "V detaile prihlášky chýba spôsob podania 'Elektronicky'.")
    _expect_text(detail, "V konflikte", "V detaile prihlášky chýba stav 'V konflikte'.")

    meno = page.locator("#dietaMeno").text_content()
    priezvisko = page.locator("#dietaPriezvisko").text_content()
    identifikator = re.search(r"Identifikátor prihlášky\s*(P-\d{4}-\d+)", detail.inner_text()).group(1)
    datum_narodenia = page.locator("#dietaDatumNarodenia").text_content()

    konflikt.click_on_vyzva_na_vyriesenie_konfliktu()

    _expect_text(
        page.locator("body"),
        "Pre dieťa existuje viac ako jedna prihláška.",
        "V dialógu výzvy chýba informácia o viacerých prihláškach."
    )
    _expect_text(
        page.locator("body"),
        "Mária Bartošová",
        "V dialógu výzvy chýba meno Mária Bartošová."
    )
    _expect_text(
        page.locator("body"),
        "Demeter Varga",
        "V dialógu výzvy chýba meno Demeter Varga."
    )

    konflikt.click_on_odoslat_vyzvu("Výzva na vyriešenie konfliktu.")

    vyzva_konflikt = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyzva_konflikt = helper.cleanup_email_text(vyzva_konflikt)

    _assert_in_options(
        vyzva_konflikt,
        _build_conflict_notice_options(meno, priezvisko, datum_narodenia),
        "Obsah e-mailu s výzvou na vyriešenie konfliktu na SS nezodpovedá očakávaniu."
    )

    _expect_text(
        page.locator("#duplicitne-prihlasky"),
        "Riaditeľ školy Stredná škola pre AT zaslal výzvu na riešenie konfliktu prihlášok.",
        "Po odoslaní výzvy sa nezobrazila informácia o zaslanej výzve."
    )
    _expect_text(
        detail,
        "V konflikte",
        "Po odoslaní výzvy sa neočakávane zmenil stav prihlášky."
    )

    konflikt.click_on_vyriesit_konflikt()

    _expect_text(
        page.locator("#vyriesit-konflikt-title"),
        "Vyriešiť konflikt",
        "Nezobrazil sa dialóg Vyriešiť konflikt."
    )
    _expect_text(
        page.locator("body"),
        "Po označení prihlášky ako aktívnej sa automaticky zneaktivnia všetky duplicitné prihlášky",
        "V dialógu riešenia konfliktu chýba popis dôsledku označenia aktívnej prihlášky."
    )

    konflikt.click_on_odoslat_konflikt("Vyriešiť konflikt.")

    vyriesenie_konflikt = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyriesenie_konflikt = helper.cleanup_email_text(vyriesenie_konflikt)

    identifikator1 = helper.inkrementuj_identifikator(identifikator)

    _assert_in_options(
        vyriesenie_konflikt,
        _build_resolution_options(
            identifikator,
            identifikator1,
            meno,
            priezvisko,
            datum_narodenia,
        ),
        "Obsah e-mailu o vyriešení konfliktu na SS nezodpovedá očakávaniu."
    )

    _expect_text(
        page.get_by_role("strong"),
        "Duplicita prihlášok úspešne vyriešená",
        "Chýba zvýraznená hláška o úspešnom vyriešení duplicity."
    )
    _expect_text(
        page.locator("#info-panel-blue-prihlaska-aktivna"),
        "Prihláška bola označená ako aktívna riaditeľom školy 910021624 Stredná škola pre AT",
        "Chýba modrý panel o označení aktívnej prihlášky."
    )
    _expect_text(
        page.locator("#info-panel-blue-prihlaska-aktivna"),
        "Ak je potrebné označiť inú prihlášku ako aktívnu, kontaktujte riaditeľa uvedenej školy.",
        "V modrom paneli chýba informácia o ďalšom postupe."
    )
    _expect_text(
        page.locator("#duplicitne-prihlasky"),
        f"Pre žiaka {meno} {priezvisko} bol vyriešený konflikt.",
        "V detaile duplicity chýba informácia o vyriešenom konflikte."
    )
    _expect_text(
        detail,
        "V spracovaní",
        "Po vyriešení konfliktu nemá aktívna prihláška stav 'V spracovaní'."
    )