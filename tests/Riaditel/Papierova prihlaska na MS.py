import os
import re
import pytest
import utils.data_helper as Data
from utils.helpers import Helper
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.papierova_prihlaska_MS_page import PapierovaPrihlaskaMS


username = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


def _expect_text(locator, text: str, message: str):
    expect(locator, message).to_contain_text(text)


def _expect_visible(locator, message: str):
    expect(locator, message).to_be_visible()


def _expect_ms_suhrn(page: Page, data, helper: Helper, den: str, mesiac: str, rok: str) -> None:
    _expect_text(page.locator("#suhrnny-prehlad"), "Súhrnný prehľad", "Chýba nadpis Súhrnný prehľad.")
    _expect_text(page.locator("#ziadostSkolskyRok"), "2026 / 2027", "Chýba školský rok.")
    _expect_text(page.locator("#ziadostDatumPodania"), f"{den}.{mesiac}.{rok}", "Chýba dátum podania.")
    _expect_text(page.locator("#poznamkaSkoly"), ":)", "Chýba poznámka školy.")
    _expect_text(page.locator("#ziadostIdentifikator"), "-", "Chýba identifikátor prihlášky.")
    _expect_text(page.locator("#ziadostSposobPodania"), "-", "Chýba spôsob podania.")

    _expect_text(page.locator("#dietaMenoSuhrn"), data.meno, "Chýba meno dieťaťa.")
    _expect_text(page.locator("#dietaPriezviskoSuhrn"), data.priezvisko, "Chýba priezvisko dieťaťa.")
    _expect_text(page.locator("#dietaRodnePriezviskoSuhrn"), data.priezvisko, "Chýba rodné priezvisko dieťaťa.")
    _expect_text(page.locator("#dietaRodneCisloSuhrn"), data.rodne_cislo, "Chýba rodné číslo dieťaťa.")
    _expect_text(
        page.locator("#dietaDatumNarodeniaSuhrn"),
        helper.rc_to_datum_narodenia(data.rodne_cislo),
        "Chýba dátum narodenia dieťaťa."
    )
    _expect_text(
        page.locator("#dietaPohlavieSuhrn"),
        helper.get_pohlavie(data.rodne_cislo),
        "Chýba pohlavie dieťaťa."
    )
    _expect_text(page.locator("#dietaMiestonarodeniaSuhrn"), "Slovensko", "Chýba miesto narodenia.")
    _expect_text(page.locator("#dietaNarodnostSuhrn"), "slovenská", "Chýba národnosť.")
    _expect_text(page.locator("#dietaStatnaPrislusnostSuhrn"), "Slovenská republika", "Chýba štátna príslušnosť.")
    _expect_text(page.locator("#dietaMaterinskyJazykSuhrn"), "slovenský", "Chýba materinský jazyk.")
    _expect_text(page.locator("#dietaInyMaterinskyJazykSuhrn"), "-", "Chýba iný materinský jazyk.")
    _expect_text(
        page.locator("#dietaAdresaTrvalehoPobytuSuhrn"),
        "Miksáthova 8/635, 02845, Kordíky, Slovenská republika",
        "Chýba trvalý pobyt dieťaťa."
    )
    _expect_text(
        page.locator("#dietaAdresaObvyklehoPobytuSuhrn"),
        "Miksáthova 8/635, 02845, Kordíky, Slovenská republika",
        "Chýba obvyklý pobyt dieťaťa."
    )
    _expect_text(page.locator("#dpDietataMsCelodennaVychova"), "Celodennú výchovu a vzdelávanie", "Chýba typ výchovy.")
    _expect_text(page.locator("#dpDietataSVVPotreby"), "Nie", "Chýba údaj o ŠVVP.")
    _expect_text(page.locator("#dpDietataSVVPotrebySNadanim"), "Nie", "Chýba údaj o nadaní.")
    _expect_text(page.locator("#dpPozadovanyDatumPrijatia"), "01.09.2026", "Chýba požadovaný dátum prijatia.")
    _expect_text(page.locator("#dpDietataPoznamka"), "-", "Chýba poznámka dieťaťa.")


def _expect_ms_skoly(page: Page) -> None:
    _expect_text(page.locator("#skoly"), "1 Materská škola č. 1", "Chýba poradie školy.")
    _expect_text(page.locator("#skoly"), "Materská škola pre AT", "Chýba názov školy.")
    _expect_text(page.locator("#skoly"), "Balková 98/8, 36578 Banská Bystrica", "Chýba adresa školy.")
    _expect_text(page.locator("#skoly"), "slovenský", "Chýba vyučovací jazyk.")


def _expect_ms_zastupcovia(page: Page) -> None:
    _expect_text(page.locator("#zastupcovia"), "Osobné údaje zákonného zástupcu č. 1", "Chýba hlavička zástupcu č. 1.")
    _expect_text(page.locator("#zakonnyZastupcaMeno"), "Peter", "Chýba meno zákonného zástupcu.")
    _expect_text(page.locator("#zakonnyZastupcaPriezvisko"), "Fodrok", "Chýba priezvisko zákonného zástupcu.")
    _expect_text(page.locator("#zakonnyZastupcaRodnePriezvisko"), "-", "Chýba rodné priezvisko zákonného zástupcu.")
    _expect_text(page.locator("#zakonnyZastupcaRodneCislo"), "860201/7842", "Chýba rodné číslo zákonného zástupcu.")
    _expect_text(page.locator("#zastupcovia"), "-", "Chýba údaj v sekcii zástupcov.")
    _expect_text(page.locator("#zakonnyZastupcaDatumNarodenia"), "01.02.1986", "Chýba dátum narodenia zákonného zástupcu.")
    _expect_text(
        page.locator("#zakonnyZastupcaAdresaBydliska"),
        "Miksáthova 8/635, 02845, Kordíky, Slovenská republika",
        "Chýba adresa zákonného zástupcu."
    )
    _expect_text(page.locator("#zakonnyZastupcaEmail"), "katalontest987@gmail.com", "Chýba e-mail zákonného zástupcu.")
    _expect_text(page.locator("#zakonnyZastupcaTelefon"), "+421905866541", "Chýba telefón zákonného zástupcu.")
    _expect_text(page.locator("#zastupcovia"), "Osobné údaje zákonného zástupcu č. 2", "Chýba hlavička zástupcu č. 2.")
    _expect_text(page.locator("#zastupcovia"), "Druhý zákonný zástupca nie je známy.", "Chýba informácia o druhom zástupcovi.")


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_pridanie_papierovej_prihlasky_MS(page: Page) -> None:
    data = Data.generate_unique_person(min_age=4, max_age=5)
    login = LoginPage(page)
    prihlaska = PapierovaPrihlaskaMS(page)
    helper = Helper()
    den, mesiac, rok = helper.aktualny_datum()

    login.login_as_riaditel(username, password, "910021626")
    prihlaska.click_on_pridaj_prihlasku()
    prihlaska.step_1_osobne_udaje(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska.step_2_SVVP()
    prihlaska.step_3_vyber_skoly()
    prihlaska.step_4_ZZ()
    prihlaska.step_5_prilohy()
    prihlaska.step_6_ostatne_udaje(den, mesiac, rok)

    _expect_ms_suhrn(page, data, helper, den, mesiac, rok)
    _expect_ms_skoly(page)
    _expect_ms_zastupcovia(page)

    _expect_text(page.locator("#prilohyHederText"), "Prílohy", "Chýba sekcia príloh.")
    _expect_visible(page.locator(".prilohaItem"), "Chýba aspoň jedna príloha.")

    prihlaska.click_on_odoslat_prihlasku()
    expect(page, "Po odoslaní sa neotvorila stránka riaditeľa.").to_have_url(re.compile(r".*/Riaditel.*"), timeout=60000)
    _expect_text(page.locator("#riaditel-home-page"), "Prihlášku pre dieťa ste úspešne pridali.", "Chýba potvrdenie o pridaní prihlášky.")

    prihlaska.najdi_prihlasku(data.meno, data.priezvisko)
    _expect_visible(page.get_by_text("P-2026-"), "Nenašiel sa identifikátor prihlášky.")
    # stav zavisi od konfiguracie prostredia
    _expect_visible(page.get_by_text(re.compile(r"Podaná|V spracovaní")).first, "Nenašiel sa stav Podaná ani V spracovaní.")
    _expect_visible(page.get_by_text("Papierovo"), "Nenašiel sa spôsob podania Papierovo.")