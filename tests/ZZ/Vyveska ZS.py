import os
import pytest

from pages.logout_page import LogoutPage
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.vyveska_page import VyveskaMS

username = os.getenv("EPRIHLASKY_ZZ_USERNAME")
password = os.getenv("EPRIHLASKY_ZZ_PASSWORD")

@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_example(page: Page) -> None:
    login = LoginPage(page)
    logout = LogoutPage(page)
    vyveska = VyveskaMS(page)

    login.login_as_zakonny_zastupca(username, password)
    vyveska.navigate_to_vyveska()
    vyveska.verify_page_header()
    vyveska.verify_page_text_logged_in()
    vyveska.fill_pristupovy_kod("T6PU43fCAPN1")
    vyveska.click_zobrazit_vysledky()
    vyveska.verify_kod_already_shown("T6PU43fCAPN1")
    vyveska.click_expand_result(nth_child="103")
    vyveska.verify_prijaty_in_table()
    vyveska.verify_neprijaty_in_table()
    logout.logout()
    vyveska.navigate_to_vyveska()
    vyveska.verify_page_header()
    vyveska.verify_page_text_logged_out()
    vyveska.fill_pristupovy_kod("T6PU43fCAPN1")
    vyveska.click_zobrazit_vysledky()
    vyveska.verify_vysledky_vyhladavania("T6PU43fCAPN1")
    vyveska.click_expand_result()
    vyveska.verify_prijaty_in_table()
    vyveska.fill_pristupovy_kod("YlxVg6wVJDik")
    vyveska.click_zobrazit_vysledky()
    vyveska.verify_vysledky_vyhladavania("YlxVg6wVJDik")
    vyveska.click_expand_result()
    vyveska.verify_neprijaty_in_table()
    
