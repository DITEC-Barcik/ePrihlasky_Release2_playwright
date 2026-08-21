import os
import pytest

from pages.logout_page import LogoutPage
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.vyveska_page import VyveskaMS

username = "ljxikynq7v@dollicons.com"
password = os.getenv("EPRIHLASKY_ZZ_PASSWORD")

@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_vyveska_SS(page: Page) -> None:
    login = LoginPage(page)
    logout = LogoutPage(page)
    vyveska = VyveskaMS(page)

    login.login_as_zakonny_zastupca(username, password)
    vyveska.navigate_to_vyveska()
    vyveska.verify_page_header()
    vyveska.verify_page_text_logged_in()
    vyveska.fill_pristupovy_kod("EzViLyfJsBgP")
    vyveska.click_zobrazit_vysledky()
    vyveska.verify_kod_already_shown("EzViLyfJsBgP")
    vyveska.click_expand_result(kod="EzViLyfJsBgP")
    vyveska.verify_prijaty_in_table()
    vyveska.verify_neprijaty_in_table()
    logout.logout()
    vyveska.navigate_to_vyveska()
    vyveska.verify_page_header()
    vyveska.verify_page_text_logged_out()
    vyveska.fill_pristupovy_kod("EzViLyfJsBgP")
    vyveska.click_zobrazit_vysledky()
    vyveska.verify_vysledky_vyhladavania("EzViLyfJsBgP")
    vyveska.click_expand_result()
    vyveska.verify_prijaty_in_table()
    vyveska.fill_pristupovy_kod("aP6SUbmwv3Hc")
    vyveska.click_zobrazit_vysledky()
    vyveska.verify_vysledky_vyhladavania("aP6SUbmwv3Hc")
    vyveska.click_expand_result()
    vyveska.verify_neprijaty_in_table()
