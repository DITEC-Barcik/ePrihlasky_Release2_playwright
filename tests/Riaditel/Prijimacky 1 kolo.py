import os
import re
import pytest
import utils.data_helper as Data

from utils.mail_helper import Mail
from utils.helpers import Helper
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.prijimacky_page import Prijimacky
from pages.prihlaska_SS_page import PrihlaskaSS
from utils.pdf_helper import compare_pdf_visual, compare_pdf_text


mailuser = os.getenv("GMAIL_USERNAME")
mailpw = os.getenv("GMAIL_APP_PASSWORD")
username = os.getenv("EPRIHLASKY_ZZ_USERNAME")
password = os.getenv("EPRIHLASKY_ZZ_PASSWORD")
username_riad = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password_riad = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


@pytest.fixture(scope="module")
def person_data():
    return Data.generate_unique_person(min_age=15, max_age=17)


def _expect_text(locator, text: str, message: str) -> None:
    expect(locator, message).to_contain_text(text)


def _expect_visible(locator, message: str) -> None:
    expect(locator, message).to_be_visible()


def _normalize_mail_text(mail_text: str, helper: Helper) -> str:
    cleaned = helper.cleanup_email_text(mail_text)
    return helper.normalize_pozvankaBody(cleaned)


def _assert_mail_equals(actual: str, expected: str, message: str) -> None:
    assert actual == expected, (
        f"{message}\n\n"
        f"=== EXPECTED ===\n{expected}\n\n"
        f"=== ACTUAL ===\n{actual}"
    )


def _build_expected_pozvanka(data, helper: Helper) -> str:
    expected = (
        f"Vážený/á pán/pani Mária Bartošová týmto pozývame žiaka {data.meno} {data.priezvisko} "
        f"{helper.rc_to_datum_narodenia(data.rodne_cislo)} "
        f"na prijímaciu skúšku 1. termín (1.kolo) do odboru vzdelávania 2285H00-zlievač , "
        f"v škole Stredná škola pre AT, ktorá sa uskutoční dňa 12.10.2026 o 11:30 hod. "
        f"Miesto: Stredná škola pre AT, 3.E Odporúčame si ho bezpečne uložiť. "
        f"Predmety prijímacej skúšky Matematika, Slovenský jazyk a literatúra. "
        f"Dostavte sa na čas a prineste si kružítko. S pozdravom Tím elektronických prihlášok MŠVVaM SR "
        f"Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, "
        f"ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. "
        f"Neodpovedajte naň."
    )
    return helper.normalize_pozvankaBody(expected)


def _build_expected_plny_pocet(data, helper: Helper) -> str:
    expected = (
        f"Vážený/á pán/pani Mária Bartošová žiak {data.meno} {data.priezvisko} "
        f"{helper.rc_to_datum_narodenia(data.rodne_cislo)} "
        f"splnil podmienky na dosiahnutie plného počtu bodov z prijímacích skúšok "
        f"do odboru vzdelávania 2285H00-zlievač , v škole Stredná škola pre AT, "
        f"ktoré mu boli udelené v systéme. Výsledky prijímacieho konania si môžete pozrieť, "
        f"keď budú dostupné pod číselným prístupovým kódom, ktorý bol žiakovi pridelený. "
        f"Odporúčame si ho bezpečne uložiť. Prosím, zapíšte si ho. "
        f"S pozdravom Tím elektronických prihlášok MŠVVaM SR "
        f"Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, "
        f"ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. "
        f"Neodpovedajte naň."
    )
    return helper.normalize_pozvankaBody(expected)


@pytest.mark.regres1kolo
def test_prihlaska_na_SS_1_kolo_prijimacky(page: Page, person_data) -> None:
    data = person_data
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

    _expect_text(
        page.locator("body"),
        "Chystáte sa odoslať prihlášku na stredné školy, ktoré ste uviedli v prihláške.",
        "Pred potvrdením odoslania sa nezobrazilo upozornenie o odoslaní prihlášky."
    )
    _expect_text(
        page.locator("body"),
        "Po odoslaní prihlášky už nebude možné upravovať údaje ani prílohy",
        "V upozornení pred odoslaním chýba informácia o uzamknutí údajov a príloh."
    )

    prihlaska.click_on_potvrdit_odoslanie()

    expect(
        page,
        "Po potvrdení odoslania sa neotvorila stránka Prihláška odoslaná."
    ).to_have_url(re.compile(r".*/Prihlaska-odoslana.*"), timeout=60000)

    _expect_text(
        page.locator("h1"),
        "Prihláška bola úspešne odoslaná!",
        "Po odoslaní sa nezobrazil nadpis o úspešnom odoslaní prihlášky."
    )


@pytest.mark.regres1kolo
def test_prijimacky_odoslanie_sprav(page: Page, person_data) -> None:
    data = person_data
    login = LoginPage(page)
    prijimacky = Prijimacky(page)
    mail = Mail()
    helper = Helper()

    login.login_as_riaditel(username_riad, password_riad, "910021624")
    prijimacky.zmen_odbor_1_kolo()
    prijimacky.click_on_menu_sprava_prihlasok()
    prijimacky.click_on_menu_prijimacky()
    prijimacky.zorad_prihlasky()
    prijimacky.click_on_uprava_prihlasky()

    _expect_text(
        page.locator("#prij_edit_meno"),
        f"{data.priezvisko} {data.meno}",
        "V detaile prihlášky sa nezobrazilo meno žiaka."
    )
    # Pôvodne "O4" - po prekonfigurovaní odborov má odbor iné poradové číslo.
    _expect_text(
        page.locator("#prij_edit_detaily"),
        "O7 - zlievač • slovenský • 2285H00",
        "V detaile prihlášky sa nezobrazili očakávané detaily odboru."
    )

    prijimacky.nastavenie_terminu_prijimaciek()
    prijimacky.click_on_akcia_odoslat_pozvanky()

    _expect_text(
        page.locator("body"),
        "Vygenerovať pozvánky",
        "Po kliknutí na odoslanie pozvánok sa nezobrazil dialóg na generovanie pozvánok."
    )

    prijimacky.odoslat_pozvanky()

    pozvanka = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    pozvanka = _normalize_mail_text(pozvanka, helper)
    expected_pozvanka = _build_expected_pozvanka(data, helper)

    _assert_mail_equals(
        pozvanka,
        expected_pozvanka,
        "Obsah e-mailu s pozvánkou nezodpovedá očakávanému textu."
    )

    _expect_text(
        page.locator("#prijimacky-generovanie-spustene"),
        "Generovanie 1 pozvánok bolo spustené.",
        "Po odoslaní pozvánok sa nezobrazila informácia o spustení generovania."
    )
    _expect_text(
        page.locator("#prijimacky-generovanie-spustene"),
        "Tento proces môže v závislosti od počtu vybraných pozvánok trvať niekoľko minút až hodín.",
        "Po odoslaní pozvánok chýba doplňujúca informácia o trvaní generovania."
    )

    prijimacky.click_on_spat_na_prijimacky()
    prijimacky.zmen_odbor_1_kolo()
    prijimacky.zorad_prihlasky()

    _expect_visible(
        page.locator("div.riaditel-prijimacky-cell.komunikacia-cell").locator("div").nth(2),
        "V zozname prijímačiek sa nezobrazuje indikátor odoslanej komunikácie."
    )

    prijimacky.click_on_akcia_plny_pocet_bodov()

    _expect_text(
        page.locator("body"),
        "Vygenerovať správu o plnom počte bodov",
        "Po kliknutí na správu o plnom počte bodov sa nezobrazil potvrdzovací dialóg."
    )

    prijimacky.odoslat_plny_pocet_bodov()

    plny_pocet = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    plny_pocet = _normalize_mail_text(plny_pocet, helper)
    expected_plny_pocet = _build_expected_plny_pocet(data, helper)

    _assert_mail_equals(
        plny_pocet,
        expected_plny_pocet,
        "Obsah e-mailu o plnom počte bodov nezodpovedá očakávanému textu."
    )

    _expect_text(
        page.locator("#riaditel-home-page"),
        "Správa bola úspešne odoslaná",
        "Po odoslaní správy o plnom počte bodov sa nezobrazila úspešná hláška."
    )

    prijimacky.click_on_menu_sprava_prihlasok()
    prijimacky.zmen_odbor_1_kolo()
    prijimacky.click_on_menu_prijimacky()
    prijimacky.zorad_prihlasky()

    prijimacky.stiahni_pozvanku()
    prijimacky.stiahni_body()


@pytest.mark.regres1kolo
def test_porovnaj_body_pdf_vizualne():
    compare_pdf_visual(
        actual_pdf="data/downloads/bodyDownloaded.pdf",
        expected_pdf="data/BodyPredloha.pdf",
        # Dĺžka mena žiaka mení počet riadkov odseku a tým posúva všetok text
        # pod ním, preto je zamaskovaná celá dynamická časť strany.
        # Obsah kontroluje test_porovnaj_body_pdf_textovo.
        masks={
            0: [
                (105, 300, 1085, 740),
            ],
        },
        threshold=0.05,
        max_diff_pixels=500,
        name_prefix="body_pdf",
        zoom=2.0,
    )


@pytest.mark.regres1kolo
def test_porovnaj_body_pdf_textovo():
    compare_pdf_text(
        actual_pdf="data/downloads/bodyDownloaded.pdf",
        expected_pdf="data/BodyPredloha.pdf",
        name_prefix="body_text",
        flatten_to_single_line=True,
        ignore_patterns=[
            r"(?<=žiak\s)[^\d]+?(?=\d{2}\.\d{2}\.\d{4})",
            r"Mária Bartošová",
            r"(?<!\d)\d{2}\.\d{2}\.\d{4}(?!\d)",
            r"(?<=Váš prístupový kód:\s)[A-Za-z0-9]+",
        ],
    )


@pytest.mark.regres1kolo
def test_porovnaj_pozvanka_pdf_vizualne():
    compare_pdf_visual(
        actual_pdf="data/downloads/pozvankaDownloaded.pdf",
        expected_pdf="data/PozvánkaPredloha.pdf",
        # To isté ako pri bodoch - obsah kontroluje test_porovnaj_pozvanka_pdf_textovo.
        masks={
            0: [
                (105, 300, 1085, 790),
            ],
        },
        threshold=0.05,
        max_diff_pixels=500,
        name_prefix="pozvanka_pdf",
        zoom=2.0,
    )


@pytest.mark.regres1kolo
def test_porovnaj_pozvanka_pdf_textovo():
    compare_pdf_text(
        actual_pdf="data/downloads/pozvankaDownloaded.pdf",
        expected_pdf="data/PozvánkaPredloha.pdf",
        name_prefix="pozvanka_text",
        flatten_to_single_line=True,
        ignore_patterns=[
            r"(?<=žiaka\s)[^\d]+?(?=\d{2}\.\d{2}\.\d{4})",
            r"Mária Bartošová",
            r"(?<!\d)\d{2}\.\d{2}\.\d{4}(?!\d)",
            r"(?<=Váš prístupový kód:\s)[A-Za-z0-9]+",
        ],
    )