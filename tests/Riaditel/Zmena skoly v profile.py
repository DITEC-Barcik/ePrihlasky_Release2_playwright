import os
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.profil_page import ProfilPage



username = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


def _expect_text(locator, text: str, message: str) -> None:
    expect(locator, message).to_contain_text(text)


def _change_school(profil: ProfilPage, school_name: str) -> None:
    profil.change_school(school_name)


def _expect_profile_school(page: Page, school_name: str) -> None:
    _expect_text(
        page.locator("#profil-riaditel-skola"),
        school_name,
        f"V profile riaditeľa sa nezobrazila škola '{school_name}'."
    )


def _expect_banner_school(page: Page, school_name: str, eduid: str) -> None:
    _expect_text(
        page.get_by_role("banner"),
        f"{school_name} — EDUID {eduid}",
        f"V banneri sa nezobrazila škola '{school_name}' s EDUID {eduid}."
    )


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_zmena_skoly_profil_riaditela(page: Page) -> None:
    login = LoginPage(page)
    profil = ProfilPage(page)

    login.login_as_riaditel(username, password, "910021626")
    profil.click_on_profil()

    _expect_profile_school(page, "Materská škola pre AT")

    _change_school(profil, "Stredná škola pre AT")
    _expect_profile_school(page, "Stredná škola pre AT")
    _expect_banner_school(page, "Stredná škola pre AT", "910021624")

    _change_school(profil, "Základná škola pre AT")
    _expect_profile_school(page, "Základná škola pre AT")
    _expect_banner_school(page, "Základná škola pre AT", "910021625")