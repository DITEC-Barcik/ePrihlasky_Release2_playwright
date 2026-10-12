import os
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from pages.sprava_pouzivatelov_page import SpravaPouzivatelov


NO_ROLE_MESSAGE = (
    "Ľutujeme, ale nemáte priradenú rolu. Ak sa ako zamestnanec školy prihlasujete do portálu, "
    "je potrebné aby vám riaditeľ školy v portáli ePrihlášky priradil rolu v rámci správy školy "
    "(správa používateľov) - bez priradenej role nie je možné spracovávať prihlášky."
)

SKOLA = "910021624"


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        pytest.skip(f"Missing environment variable: {name}")
    return value


@pytest.fixture
def credentials():
    return {
        "riad_username": _require_env("EPRIHLASKY_RIADITEL_USERNAME"),
        "riad_password": _require_env("EPRIHLASKY_RIADITEL_PASSWORD"),
        "admin_username": _require_env("EPRIHLASKY_ADMIN_USERNAME"),
        "admin_password": _require_env("EPRIHLASKY_ADMIN_PASSWORD"),
        "spracovatel_username": _require_env("EPRIHLASKY_SPRACOVATEL_USERNAME"),
        "spracovatel_password": _require_env("EPRIHLASKY_SPRACOVATEL_PASSWORD"),
    }


def _expect_user_management_intro(page: Page) -> None:
    expect(
        page.locator("#sprava-pouzivatelov"),
        "Na stránke správy používateľov sa nezobrazil formulár na pridanie používateľa."
    ).to_contain_text("Pridať používateľa")

    expect(
        page.locator("#sprava-pouzivatelov"),
        "Na stránke správy používateľov chýba pomocný text o zapojení odborníkov do kontroly prihlášok."
    ).to_contain_text(
        "Vyhľadajte a zapojte odborníkov z vašej školy do procesu kontroly prihlášok."
    )


def _expect_user_added_success(page: Page, role_name: str) -> None:
    expect(
        page.locator("#sprava-skoly-content"),
        f"Po pridaní roly '{role_name}' sa nezobrazila úspešná hláška."
    ).to_contain_text("Používateľa ste úspešne pridali.")

    expect(
        page.locator("#sprava-pouzivatelov"),
        "Po pridaní používateľa sa nezobrazil nadpis stránky Správa používateľov."
    ).to_contain_text("Správa používateľov")

    expect(
        page.get_by_role("paragraph"),
        "Po pridaní používateľa chýba popis správy používateľov."
    ).to_contain_text("Spravujte používateľov a priraďte im rolu.")


def _expect_profile(page: Page, full_name: str, role_name: str) -> None:
    expect(
        page.locator("#meno-osoby"),
        f"V profile používateľa sa nezobrazilo meno '{full_name}'."
    ).to_contain_text(full_name)

    expect(
        page.locator("#profil-riaditel-typ"),
        f"V profile používateľa sa nezobrazila rola '{role_name}'."
    ).to_contain_text(role_name)


def _expect_remove_dialog(page: Page) -> None:
    expect(
        page.locator("body"),
        "Po kliknutí na odstránenie sa nezobrazil dialóg Odstránenie údajov."
    ).to_contain_text("Odstránenie údajov")


def _expect_user_removed_success(page: Page) -> None:
    expect(
        page.locator("#sprava-skoly-content"),
        "Po odstránení používateľa sa nezobrazila úspešná hláška."
    ).to_contain_text("Používateľa ste úspešne odstránili.")


def _expect_login_without_role(page: Page, username_label: str) -> None:
    expect(
        page.locator("#error-summary-title-login"),
        f"Po prihlásení používateľa '{username_label}' sa nezobrazil nadpis o neúspešnom prihlásení."
    ).to_contain_text("Neúspešné prihlásenie do systému")

    expect(
        page.locator("#error-message-login"),
        f"Po prihlásení používateľa '{username_label}' sa nezobrazila očakávaná chyba o nepriradenej role."
    ).to_contain_text(NO_ROLE_MESSAGE)


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_pridaj_rolu(page: Page, credentials) -> None:
    login = LoginPage(page)
    logout = LogoutPage(page)
    role = SpravaPouzivatelov(page)

    login.login_as_riaditel(
        credentials["riad_username"],
        credentials["riad_password"],
        SKOLA
    )

    role.otvor_spravu_pouzivatelov()
    role.click_on_pridat_pouzivatela()
    _expect_user_management_intro(page)

    role.pridaj_rolu("930593021", "spracovatel")
    _expect_user_added_success(page, "spracovatel")

    role.click_on_pridat_pouzivatela()
    role.pridaj_rolu("930593019", "admin")
    _expect_user_added_success(page, "admin")

    logout.logout()

    login.login_as_rola(
        credentials["spracovatel_username"],
        credentials["spracovatel_password"]
    )
    role.otvor_profil()
    _expect_profile(page, "Klaudia Kelmová", "Spracovateľ")

    logout.logout()

    login.login_as_rola(
        credentials["admin_username"],
        credentials["admin_password"]
    )
    role.otvor_profil()
    _expect_profile(page, "Dušan Lemo", "Administrátor")


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_odstran_rolu(page: Page, credentials) -> None:
    login = LoginPage(page)
    logout = LogoutPage(page)
    role = SpravaPouzivatelov(page)

    login.login_as_riaditel(
        credentials["riad_username"],
        credentials["riad_password"],
        SKOLA
    )

    role.otvor_spravu_pouzivatelov()

    role.click_on_odstranit()
    _expect_remove_dialog(page)
    role.click_on_potvrdit_odstranenie()
    _expect_user_removed_success(page)

    role.click_on_odstranit()
    _expect_remove_dialog(page)
    role.click_on_potvrdit_odstranenie()
    _expect_user_removed_success(page)

    logout.logout()

    login.login_as_rola(
        credentials["admin_username"],
        credentials["admin_password"]
    )
    _expect_login_without_role(page, "admin")

    login.login_as_rola(
        credentials["spracovatel_username"],
        credentials["spracovatel_password"]
    )
    _expect_login_without_role(page, "spracovateľ")