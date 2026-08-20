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


def _expect_visible(locator, message: str) -> None:
    expect(locator, message).to_be_visible()


def _update_zs_school_profile_first_version(
    page: Page,
    login_page: LoginPage,
    sprava_skoly: SpravaSkoly,
) -> None:
    login_page.login_as_riaditel(username, password, "910021625")
    sprava_skoly.click_on_menu_sprava_skoly()

    page.get_by_text("Prístupné poschodia, toalety").click()
    page.get_by_text("Bez telocvične").click()
    page.get_by_text("Multifunkčné vonkajšie ihrisko").click()
    page.get_by_text("Úroveň 2: Digitálna komuniká").click()
    page.locator("#radioGroup-ZS_WiFi").get_by_text("Nie").click()
    page.get_by_role("textbox", name="Krátky popis školy *").fill("testovací popis 1")

    sprava_skoly.click_on_ulozit_zmeny()

    _expect_text(
        page.locator("#sprava-skoly-content"),
        "Údaje profilu školy boli úspešne uložené",
        "Po uložení 1. verzie profilu ZŠ sa nezobrazila úspešná hláška."
    )


def _update_zs_school_profile_second_version(
    page: Page,
    login_page: LoginPage,
    sprava_skoly: SpravaSkoly,
) -> None:
    login_page.login_as_riaditel(username, password, "910021625")
    sprava_skoly.click_on_menu_sprava_skoly()

    page.get_by_role("radio", name="Škola neprístupná pre osoby").check()
    page.get_by_role("radio", name="Viac telocviční").check()
    page.get_by_role("radio", name="Bez vonkajšieho ihriska").check()
    page.get_by_role("radio", name="Úroveň 5: Riešenie digitá").check()
    page.get_by_role("radio", name="Áno").check()
    page.get_by_role("textbox", name="Krátky popis školy *").fill("testovací popis 2")

    sprava_skoly.click_on_ulozit_zmeny()

    _expect_text(
        page.locator("#sprava-skoly-content"),
        "Údaje profilu školy boli úspešne uložené",
        "Po uložení 2. verzie profilu ZŠ sa nezobrazila úspešná hláška."
    )


def _open_public_zs_profile(verejna_zona: VerejnaZona) -> None:
    verejna_zona.vyhladaj_skolu("Základná škola pre AT", "910021625", "Základné školy")
    verejna_zona.click_on_profil_skoly()


def _expect_zs_public_profile_first_version(page: Page) -> None:
    locator = page.locator("#najst-skolu-content")

    _expect_text(locator, "Základná škola pre AT, Jalmová 19", "Vo verejnom profile chýba názov ZŠ.")
    _expect_text(locator, "Jalmová 19, 065 34 Prešov", "Vo verejnom profile chýba adresa ZŠ.")
    _expect_text(locator, "testovací popis 1", "Vo verejnom profile chýba prvý testovací popis.")
    _expect_text(locator, "Prístupné poschodia, toalety a jedáleň", "Vo verejnom profile chýba prvý údaj o prístupnosti.")
    _expect_text(locator, "Bez telocvične", "Vo verejnom profile chýba prvý údaj o telocvični.")
    _expect_text(locator, "Multifunkčné vonkajšie ihrisko", "Vo verejnom profile chýba prvý údaj o ihrisku.")
    _expect_text(locator, "Nie", "Vo verejnom profile chýba hodnota Wi‑Fi 'Nie'.")

    _expect_visible(
        page.get_by_text("check").first,
        "Vo verejnom profile sa nezobrazuje prvá ikonka 'check'."
    )
    _expect_visible(
        page.get_by_text("check").nth(1),
        "Vo verejnom profile sa nezobrazuje druhá ikonka 'check'."
    )
    _expect_visible(
        page.locator(".subcategories > div:nth-child(4) > .material-icons"),
        "Vo verejnom profile sa nezobrazuje ikonka digitálnej úrovne."
    )
    _expect_visible(
        page.locator("div:nth-child(5) > .material-icons"),
        "Vo verejnom profile sa nezobrazuje 5. ikonka kategórie."
    )
    _expect_visible(
        page.locator("div:nth-child(6) > .material-icons"),
        "Vo verejnom profile sa nezobrazuje 6. ikonka kategórie."
    )


def _expect_zs_public_profile_second_version(page: Page) -> None:
    locator = page.locator("#najst-skolu-content")

    _expect_text(locator, "Základná škola pre AT, Jalmová 19", "Vo verejnom profile chýba názov ZŠ po druhej úprave.")
    _expect_text(locator, "testovací popis 2", "Vo verejnom profile chýba druhý testovací popis.")
    _expect_text(locator, "Škola neprístupná pre osoby so zníženou mobilitou", "Vo verejnom profile chýba druhý údaj o prístupnosti.")
    _expect_text(locator, "Viac telocviční", "Vo verejnom profile chýba druhý údaj o telocvični.")
    _expect_text(locator, "Bez vonkajšieho ihriska", "Vo verejnom profile chýba druhý údaj o ihrisku.")
    _expect_text(locator, "Áno", "Vo verejnom profile chýba hodnota Wi‑Fi 'Áno'.")

    _expect_visible(
        page.get_by_text("check").first,
        "Vo verejnom profile sa nezobrazuje prvá ikonka 'check' po druhej úprave."
    )
    _expect_visible(
        page.get_by_text("check").nth(1),
        "Vo verejnom profile sa nezobrazuje druhá ikonka 'check' po druhej úprave."
    )
    _expect_visible(
        page.get_by_text("check").nth(2),
        "Vo verejnom profile sa nezobrazuje tretia ikonka 'check' po druhej úprave."
    )
    _expect_visible(
        page.get_by_text("check").nth(3),
        "Vo verejnom profile sa nezobrazuje štvrtá ikonka 'check' po druhej úprave."
    )
    _expect_visible(
        page.get_by_text("check").nth(4),
        "Vo verejnom profile sa nezobrazuje piata ikonka 'check' po druhej úprave."
    )


@pytest.mark.spravaSkoly
@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_profil_skoly_ZS(page: Page) -> None:
    login_page = LoginPage(page)
    logout_page = LogoutPage(page)
    verejna_zona = VerejnaZona(page)
    sprava_skoly = SpravaSkoly(page)

    _update_zs_school_profile_first_version(page, login_page, sprava_skoly)
    logout_page.logout()

    _open_public_zs_profile(verejna_zona)
    _expect_zs_public_profile_first_version(page)

    page.locator("button").filter(has_text="Zavrieť").last.click()

    _update_zs_school_profile_second_version(page, login_page, sprava_skoly)
    logout_page.logout()

    _open_public_zs_profile(verejna_zona)
    _expect_zs_public_profile_second_version(page)