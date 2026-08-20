import os
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from pages.verejna_zona_page import VerejnaZona
from pages.sprava_skoly_page import SpravaSkoly


username = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


def _expect_text(locator, text: str, message: str) -> None:
    expect(locator, message).to_contain_text(text)


def _click_profile_option(page: Page, visible_text: str, message: str) -> None:
    page.get_by_text(visible_text).click()
    # Alternatíva do budúcna: presunúť do page objectu SpravaSkoly.


def _update_school_profile(
    page: Page,
    login_page: LoginPage,
    sprava_skoly: SpravaSkoly,
    school_code: str,
    accessibility_text: str,
    gym_text: str,
    playground_text: str,
    short_description: str,
) -> None:
    login_page.login_as_riaditel(username, password, school_code)
    sprava_skoly.click_on_menu_sprava_skoly()

    _click_profile_option(
        page,
        accessibility_text,
        "Nepodarilo sa vybrať možnosť prístupnosti školy."
    )
    _click_profile_option(
        page,
        gym_text,
        "Nepodarilo sa vybrať možnosť telocvične."
    )
    _click_profile_option(
        page,
        playground_text,
        "Nepodarilo sa vybrať možnosť vonkajšieho ihriska."
    )

    page.get_by_role("textbox", name="Krátky popis školy *").fill(short_description)
    sprava_skoly.click_on_ulozit_zmeny()

    _expect_text(
        page.locator("#sprava-skoly-content"),
        "Údaje profilu školy boli úspešne uložené",
        "Po uložení sa nezobrazila úspešná hláška o uložení profilu školy."
    )


def _open_public_school_profile(
    verejna_zona: VerejnaZona,
    school_name: str,
    school_code: str,
    school_type: str,
) -> None:
    verejna_zona.vyhladaj_skolu(school_name, school_code, school_type)
    verejna_zona.click_on_profil_skoly()


def _expect_public_profile_ms_version_1(page: Page) -> None:
    locator = page.locator("#najst-skolu-content")

    _expect_text(locator, "Materská škola pre AT, Balková 8", "Vo verejnom profile chýba názov alebo adresa školy.")
    _expect_text(locator, "testovací popis 1", "Vo verejnom profile chýba prvý testovací popis.")
    _expect_text(locator, "Škola neprístupná pre osoby so zníženou mobilitou", "Vo verejnom profile chýba prvá informácia o prístupnosti.")
    _expect_text(locator, "Telocvičňa do 400 m2", "Vo verejnom profile chýba prvá informácia o telocvični.")
    _expect_text(locator, "Základné vonkajšie ihrisko", "Vo verejnom profile chýba prvá informácia o ihrisku.")


def _expect_public_profile_ms_version_2(page: Page) -> None:
    locator = page.locator("#najst-skolu-content")

    _expect_text(locator, "testovací popis 2", "Vo verejnom profile chýba druhý testovací popis.")
    _expect_text(locator, "Prístupné poschodia, toalety a jedáleň", "Vo verejnom profile chýba druhá informácia o prístupnosti.")
    _expect_text(locator, "Viac telocviční", "Vo verejnom profile chýba druhá informácia o telocvični.")
    _expect_text(locator, "Viaceré multifunkčné vonkajšie ihriská", "Vo verejnom profile chýba druhá informácia o ihrisku.")


@pytest.mark.spravaSkoly
@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_profil_skoly_MS(page: Page) -> None:
    login_page = LoginPage(page)
    logout_page = LogoutPage(page)
    verejna_zona = VerejnaZona(page)
    sprava_skoly = SpravaSkoly(page)

    _update_school_profile(
        page=page,
        login_page=login_page,
        sprava_skoly=sprava_skoly,
        school_code="910021626",
        accessibility_text="Škola neprístupná pre osoby",
        gym_text="Telocvičňa do 400 m2",
        playground_text="Základné vonkajšie ihrisko",
        short_description="testovací popis 1",
    )

    logout_page.logout()

    _open_public_school_profile(
        verejna_zona,
        "Materská škola pre AT",
        "910021626",
        "Materské školy",
    )
    _expect_public_profile_ms_version_1(page)

    page.locator("button").filter(has_text="Zavrieť").last.click()

    _update_school_profile(
        page=page,
        login_page=login_page,
        sprava_skoly=sprava_skoly,
        school_code="910021626",
        accessibility_text="Prístupné poschodia, toalety",
        gym_text="Viac telocviční",
        playground_text="Viaceré multifunkčné vonkajš",
        short_description="testovací popis 2",
    )

    logout_page.logout()

    _open_public_school_profile(
        verejna_zona,
        "Materská škola pre AT",
        "910021626",
        "Materské školy",
    )
    _expect_public_profile_ms_version_2(page)