import pytest

import os

import re

import utils.data_helper as Data

from utils.helpers import Helper

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage

from pages.logout_page import LogoutPage

from pages.papierova_prihlaska_ZSSS_page import PapierovaPrihlaskaZSSS

from pages.papierova_prihlaska_SS_page import PapierovaPrihlaskaSS



username=os.getenv("EPRIHLASKY_RIADITEL_USERNAME")

password=os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")



@pytest.mark.regres2kolo

def test_pridanie_papierovej_prihlasky_SS_riaditelom_ZS_2_kolo(page: Page) -> None:

    data = Data.generate_unique_person(min_age=15, max_age=17)

    login = LoginPage(page)

    logout = LogoutPage(page)

    prihlaska = PapierovaPrihlaskaZSSS(page)

    prihlaska1 = PapierovaPrihlaskaSS(page)

    helper = Helper()

    den, mesiac, rok = helper.aktualny_datum()

    login.login_as_riaditel(username,password,"910021625")

    prihlaska.click_on_pridaj_prihlasku("2")

    prihlaska.step_1_osobne_udaje(data.meno, data.priezvisko, data.rodne_cislo)

    prihlaska.step_2_SVVP()

    prihlaska.step_3_vyber_skoly()

    prihlaska.step_4_ZZ()

    prihlaska.step_5_navsteva_ZS()

    prihlaska.step_6_znamky()

    prihlaska.step_7_sutaze()

    prihlaska.step_8_prilohy()

    prihlaska.step_9_ostatne_udaje(den, mesiac, rok)

    #step10 Súhrnný prehľad

    expect(page.locator("#ziadostIdentifikator")).to_contain_text("-")

    expect(page.locator("#ziadostSkolskyRok")).to_contain_text("2026 / 2027")

    expect(page.locator("#ziadostDatumPodania")).to_contain_text(den+"."+mesiac+"."+rok)

    expect(page.locator("#ziadostSposobPodania")).to_contain_text("-")

    expect(page.locator("#poznamkaSkoly")).to_contain_text("(-_-)")

    expect(page.locator("#koloPrijimaciehoKonania")).to_contain_text("2. kolo")

    expect(page.locator("#dietaMenoSuhrn")).to_contain_text(data.meno)

    expect(page.locator("#dietaPriezviskoSuhrn")).to_contain_text(data.priezvisko)

    expect(page.locator("#dietaRodnePriezviskoSuhrn")).to_contain_text(data.priezvisko)

    expect(page.locator("#dietaRodneCisloSuhrn")).to_contain_text(data.rodne_cislo)

    expect(page.locator("#dietaDatumNarodeniaSuhrn")).to_contain_text(helper.rc_to_datum_narodenia(data.rodne_cislo))

    expect(page.locator("#dietaPohlavieSuhrn")).to_contain_text(helper.get_pohlavie(data.rodne_cislo))

    expect(page.locator("#dietaMiestonarodeniaSuhrn")).to_contain_text("Slovensko")

    expect(page.locator("#dietaNarodnostSuhrn")).to_contain_text("slovenská")

    expect(page.locator("#dietaStatnaPrislusnostSuhrn")).to_contain_text("Slovenská republika")

    expect(page.locator("#dietaMaterinskyJazykSuhrn")).to_contain_text("slovenský")

    expect(page.locator("#dietaInyMaterinskyJazykSuhrn")).to_contain_text("-")

    expect(page.locator("#dietaAdresaTrvalehoPobytuSuhrn")).to_contain_text("Súčovská 3/9, 65874, Debraď, Slovenská republika")

    expect(page.locator("#dpZmenenaPracovnaSchopnost")).to_contain_text("Nie")

    expect(page.locator("#dpSVVP")).to_contain_text("Nie")

    expect(page.locator("#dpMentalnePostihnutie")).to_contain_text("Nie")

    expect(page.locator("#dpPoznamka")).to_contain_text("ŠVVP")

    expect(page.locator("#skoly")).to_contain_text("910021624")

    expect(page.locator("#skoly")).to_contain_text("1 Stredná škola č. 1")

    expect(page.locator("#skoly")).to_contain_text("Stredná škola pre AT")

    expect(page.locator("#skoly")).to_contain_text("2285H00")

    expect(page.locator("#skoly")).to_contain_text("zlievač -3 ročné")

    expect(page.locator("#skoly")).to_contain_text("Netalentový")

    expect(page.locator("#skoly")).to_contain_text("1. termín")

    expect(page.locator("#skoly")).to_contain_text("slovenský")

    expect(page.locator("#skoly")).to_contain_text("Nie")

    expect(page.locator("#skoly")).to_contain_text("Nie")

    expect(page.locator("#zastupcovia")).to_contain_text("Osobné údaje zákonného zástupcu č. 1")

    expect(page.locator("#zakonnyZastupcaMeno")).to_contain_text("Rudolf")

    expect(page.locator("#zakonnyZastupcaPriezvisko")).to_contain_text("Brezinoha")

    expect(page.locator("#zakonnyZastupcaRodnePriezvisko")).to_contain_text("-")

    expect(page.locator("#zakonnyZastupcaRodneCislo")).to_contain_text("760225/6013")

    expect(page.locator("#zastupcovia")).to_contain_text("-")

    expect(page.locator("#zakonnyZastupcaDatumNarodenia")).to_contain_text("25.02.1976")

    expect(page.locator("#zakonnyZastupcaAdresaBydliska")).to_contain_text("Súčovská 3/9, 65874, Debraď, Slovenská republika")

    expect(page.locator("#zakonnyZastupcaEmail")).to_contain_text("katalontest987@gmail.com")

    expect(page.locator("#zakonnyZastupcaTelefon")).to_contain_text("+421987654321")

    expect(page.locator("#zakonnyZastupcaVyhradnaKomunikacia")).to_contain_text("Áno")

    expect(page.locator("#zastupcovia")).to_contain_text("Osobné údaje zákonného zástupcu č. 2")

    expect(page.locator("#zakonnyZastupca2Meno")).to_contain_text("Tereza")

    expect(page.locator("#zakonnyZastupca2Priezvisko")).to_contain_text("Brezinohová")

    expect(page.locator("#zakonnyZastupca2RodnePriezvisko")).to_contain_text("-")

    expect(page.locator("#zakonnyZastupca2RodneCislo")).to_contain_text("765413/0341")

    expect(page.locator("#zastupcovia")).to_contain_text("-")

    expect(page.locator("#zakonnyZastupca2DatumNarodenia")).to_contain_text("13.04.1976")

    expect(page.locator("#zakonnyZastupca2AdresaBydliska")).to_contain_text("Súčovská 3/9, 65874, Debraď, Slovenská republika")

    expect(page.locator("#zakonnyZastupca2Email")).to_contain_text("katalontest789@gmail.com")

    expect(page.locator("#zakonnyZastupca2Telefon")).to_contain_text("+421357951486")

    expect(page.locator("#suhlasDruhehoZZ")).to_contain_text("Áno")

    expect(page.locator("#prichodZiakaSuhrnZiadost")).to_contain_text("Zo ZŠ na Slovensku")

    expect(page.locator("#eduidZSSuhrnZiadost")).to_contain_text("910021625")

    expect(page.locator("#nazovZSSuhrnZiadost")).to_contain_text("Základná škola pre AT")

    expect(page.locator("#rocnikSuhrnZiadost")).to_contain_text("9.")

    expect(page.locator("#triedaSuhrnZiadost")).to_contain_text("9.A")

    expect(page.locator("#rokSkolskejDochadzkySuhrnZiadost")).to_contain_text("9")

    expect(page.locator("#vyucovaciJazykVZSSuhrnZiadost")).to_contain_text("Slovenský")

    expect(page.locator("#vysledky-vzdelavania-suhrn")).to_be_visible()

    expect(page.locator("#sutaze-suhrn")).to_contain_text("Súťaž Ferova dvanástka Bez umiestnenia - Okresná úroveň Iné Školský rok: 2021/2022")

    expect(page.locator(".panel-content-prilohy")).to_be_visible()

    prihlaska.click_on_odoslat_prihlasku()

    expect(page).to_have_url(re.compile(r".*/Riaditel.*"), timeout=60000)

    prihlaska.najdi_prihlasku(data.meno, data.priezvisko)

    expect(page.locator("#riaditel-prihlasky-na-strednu-skolu")).to_contain_text("Pripravená")

    expect(page.locator("#riaditel-prihlasky-na-strednu-skolu")).to_contain_text(data.priezvisko +" "+ data.meno)

    prihlaska.click_on_zobrazit_prihlasku()

    prihlaska.click_on_skontrolovana()

    expect(page.locator("#message-box")).to_contain_text("Stav kontroly bol aktualizovaný na skontrolovaná.")

    expect(page.locator("#detail-prihlasky-riad-SS-content")).to_contain_text("Papierovo ZŠ")

    prihlaska.click_on_odoslat_na_SS()

    expect(page.locator("#info-panel-blue-prihlaska-bola-podana-priamo-na-strednu-skolu")).to_contain_text("Prihláška bola podaná priamo na strednú školu. Prihlášku pridal do systému riaditeľ školy Jalmová 266/19, 06534, Prešov")

    logout.logout()

    login.login_as_riaditel(username,password,"910021624")

    page.get_by_label("Kolo").select_option("2")

    prihlaska1.najdi_prihlasku(data.meno, data.priezvisko)

    expect(page.locator("#sub-riaditel-prihlasky")).to_contain_text("Papierovo ZŠ")

    expect(page.locator("#sub-riaditel-prihlasky")).to_contain_text("Prijatá od ZŠ")

    prihlaska1.click_on_zobrazit_prihlasku()



@pytest.mark.regres1kolo

def test_pridanie_papierovej_prihlasky_SS_riaditelom_ZS_1_kolo(page: Page) -> None:

    data = Data.generate_unique_person(min_age=15, max_age=17)

    login = LoginPage(page)

    logout = LogoutPage(page)

    prihlaska = PapierovaPrihlaskaZSSS(page)

    prihlaska1 = PapierovaPrihlaskaSS(page)

    helper = Helper()

    den, mesiac, rok = helper.aktualny_datum()

    login.login_as_riaditel(username,password,"910021625")

    prihlaska.click_on_pridaj_prihlasku("1")

    prihlaska.step_1_osobne_udaje(data.meno, data.priezvisko, data.rodne_cislo)

    prihlaska.step_2_SVVP()

    prihlaska.step_3_vyber_skoly()

    prihlaska.step_4_ZZ()

    prihlaska.step_5_navsteva_ZS()

    prihlaska.step_6_znamky()

    prihlaska.step_7_sutaze()

    prihlaska.step_8_prilohy()

    prihlaska.step_9_ostatne_udaje(den, mesiac, rok)

    #step10 Súhrnný prehľad

    expect(page.locator("#ziadostIdentifikator")).to_contain_text("-")

    expect(page.locator("#ziadostSkolskyRok")).to_contain_text("2026 / 2027")

    expect(page.locator("#ziadostDatumPodania")).to_contain_text(den+"."+mesiac+"."+rok)

    expect(page.locator("#ziadostSposobPodania")).to_contain_text("-")

    expect(page.locator("#poznamkaSkoly")).to_contain_text("(-_-)")

    expect(page.locator("#koloPrijimaciehoKonania")).to_contain_text("1. kolo")

    expect(page.locator("#dietaMenoSuhrn")).to_contain_text(data.meno)

    expect(page.locator("#dietaPriezviskoSuhrn")).to_contain_text(data.priezvisko)

    expect(page.locator("#dietaRodnePriezviskoSuhrn")).to_contain_text(data.priezvisko)

    expect(page.locator("#dietaRodneCisloSuhrn")).to_contain_text(data.rodne_cislo)

    expect(page.locator("#dietaDatumNarodeniaSuhrn")).to_contain_text(helper.rc_to_datum_narodenia(data.rodne_cislo))

    expect(page.locator("#dietaPohlavieSuhrn")).to_contain_text(helper.get_pohlavie(data.rodne_cislo))

    expect(page.locator("#dietaMiestonarodeniaSuhrn")).to_contain_text("Slovensko")

    expect(page.locator("#dietaNarodnostSuhrn")).to_contain_text("slovenská")

    expect(page.locator("#dietaStatnaPrislusnostSuhrn")).to_contain_text("Slovenská republika")

    expect(page.locator("#dietaMaterinskyJazykSuhrn")).to_contain_text("slovenský")

    expect(page.locator("#dietaInyMaterinskyJazykSuhrn")).to_contain_text("-")

    expect(page.locator("#dietaAdresaTrvalehoPobytuSuhrn")).to_contain_text("Súčovská 3/9, 65874, Debraď, Slovenská republika")

    expect(page.locator("#dpZmenenaPracovnaSchopnost")).to_contain_text("Nie")

    expect(page.locator("#dpSVVP")).to_contain_text("Nie")

    expect(page.locator("#dpMentalnePostihnutie")).to_contain_text("Nie")

    expect(page.locator("#dpPoznamka")).to_contain_text("ŠVVP")

    expect(page.locator("#skoly")).to_contain_text("910021624")

    expect(page.locator("#skoly")).to_contain_text("1 Stredná škola č. 1")

    expect(page.locator("#skoly")).to_contain_text("Stredná škola pre AT")

    expect(page.locator("#skoly")).to_contain_text("2285H00")

    expect(page.locator("#skoly")).to_contain_text("zlievač -3 ročné")

    expect(page.locator("#skoly")).to_contain_text("Netalentový")

    expect(page.locator("#skoly")).to_contain_text("1. termín")

    expect(page.locator("#skoly")).to_contain_text("slovenský")

    expect(page.locator("#skoly")).to_contain_text("Nie")

    expect(page.locator("#skoly")).to_contain_text("Nie")

    expect(page.locator("#zastupcovia")).to_contain_text("Osobné údaje zákonného zástupcu č. 1")

    expect(page.locator("#zakonnyZastupcaMeno")).to_contain_text("Rudolf")

    expect(page.locator("#zakonnyZastupcaPriezvisko")).to_contain_text("Brezinoha")

    expect(page.locator("#zakonnyZastupcaRodnePriezvisko")).to_contain_text("-")

    expect(page.locator("#zakonnyZastupcaRodneCislo")).to_contain_text("760225/6013")

    expect(page.locator("#zastupcovia")).to_contain_text("-")

    expect(page.locator("#zakonnyZastupcaDatumNarodenia")).to_contain_text("25.02.1976")

    expect(page.locator("#zakonnyZastupcaAdresaBydliska")).to_contain_text("Súčovská 3/9, 65874, Debraď, Slovenská republika")

    expect(page.locator("#zakonnyZastupcaEmail")).to_contain_text("katalontest987@gmail.com")

    expect(page.locator("#zakonnyZastupcaTelefon")).to_contain_text("+421987654321")

    expect(page.locator("#zakonnyZastupcaVyhradnaKomunikacia")).to_contain_text("Áno")

    expect(page.locator("#zastupcovia")).to_contain_text("Osobné údaje zákonného zástupcu č. 2")

    expect(page.locator("#zakonnyZastupca2Meno")).to_contain_text("Tereza")

    expect(page.locator("#zakonnyZastupca2Priezvisko")).to_contain_text("Brezinohová")

    expect(page.locator("#zakonnyZastupca2RodnePriezvisko")).to_contain_text("-")

    expect(page.locator("#zakonnyZastupca2RodneCislo")).to_contain_text("765413/0341")

    expect(page.locator("#zastupcovia")).to_contain_text("-")

    expect(page.locator("#zakonnyZastupca2DatumNarodenia")).to_contain_text("13.04.1976")

    expect(page.locator("#zakonnyZastupca2AdresaBydliska")).to_contain_text("Súčovská 3/9, 65874, Debraď, Slovenská republika")

    expect(page.locator("#zakonnyZastupca2Email")).to_contain_text("katalontest789@gmail.com")

    expect(page.locator("#zakonnyZastupca2Telefon")).to_contain_text("+421357951486")

    expect(page.locator("#suhlasDruhehoZZ")).to_contain_text("Áno")

    expect(page.locator("#prichodZiakaSuhrnZiadost")).to_contain_text("Zo ZŠ na Slovensku")

    expect(page.locator("#eduidZSSuhrnZiadost")).to_contain_text("910021625")

    expect(page.locator("#nazovZSSuhrnZiadost")).to_contain_text("Základná škola pre AT")

    expect(page.locator("#rocnikSuhrnZiadost")).to_contain_text("9.")

    expect(page.locator("#triedaSuhrnZiadost")).to_contain_text("9.A")

    expect(page.locator("#rokSkolskejDochadzkySuhrnZiadost")).to_contain_text("9")

    expect(page.locator("#vyucovaciJazykVZSSuhrnZiadost")).to_contain_text("Slovenský")

    expect(page.locator("#vysledky-vzdelavania-suhrn")).to_be_visible()

    expect(page.locator("#sutaze-suhrn")).to_contain_text("Súťaž Ferova dvanástka Bez umiestnenia - Okresná úroveň Iné Školský rok: 2021/2022")

    expect(page.locator(".panel-content-prilohy")).to_be_visible()

    prihlaska.click_on_odoslat_prihlasku()

    expect(page).to_have_url(re.compile(r".*/Riaditel.*"), timeout=60000)

    prihlaska.najdi_prihlasku(data.meno, data.priezvisko)

    expect(page.locator("#riaditel-prihlasky-na-strednu-skolu")).to_contain_text("Pripravená")

    expect(page.locator("#riaditel-prihlasky-na-strednu-skolu")).to_contain_text(data.priezvisko +" "+ data.meno)

    prihlaska.click_on_zobrazit_prihlasku()

    prihlaska.click_on_skontrolovana()

    expect(page.locator("#message-box")).to_contain_text("Stav kontroly bol aktualizovaný na skontrolovaná.")

    expect(page.locator("#detail-prihlasky-riad-SS-content")).to_contain_text("Papierovo ZŠ")

    prihlaska.click_on_odoslat_na_SS()

    expect(page.locator("#info-panel-blue-prihlaska-bola-podana-priamo-na-strednu-skolu")).to_contain_text("Prihláška bola podaná priamo na strednú školu. Prihlášku pridal do systému riaditeľ školy Jalmová 266/19, 06534, Prešov")

    logout.logout()

    login.login_as_riaditel(username,password,"910021624")

    page.get_by_label("Kolo").select_option("1")

    prihlaska1.najdi_prihlasku_1_kolo(data.meno, data.priezvisko)

    expect(page.locator("#sub-riaditel-prihlasky")).to_contain_text("Papierovo ZŠ")

    expect(page.locator("#sub-riaditel-prihlasky")).to_contain_text("Prijatá od ZŠ")

    prihlaska1.click_on_zobrazit_prihlasku()

