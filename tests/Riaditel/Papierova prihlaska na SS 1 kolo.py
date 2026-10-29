import os
import re
import pytest
import utils.data_helper as Data
from utils.helpers import Helper
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.papierova_prihlaska_SS_page import PapierovaPrihlaskaSS


username = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


def _expect_text(locator, text: str, message: str):
    expect(locator, message).to_contain_text(text)


def _expect_visible(locator, message: str):
    expect(locator, message).to_be_visible()


def _expect_summary_ss_1_kolo(page: Page, data, helper: Helper, den: str, mesiac: str, rok: str) -> None:
    _expect_text(page.locator("#ziadostIdentifikator"), "-", "V súhrne chýba identifikátor prihlášky pred odoslaním.")
    _expect_text(page.locator("#ziadostSkolskyRok"), "2027/2028", "V súhrne chýba školský rok.")
    _expect_text(page.locator("#ziadostDatumPodania"), f"{den}.{mesiac}.{rok}", "V súhrne chýba dátum podania.")
    _expect_text(page.locator("#ziadostSposobPodania"), "-", "V súhrne chýba spôsob podania pred odoslaním.")
    _expect_text(page.locator("#poznamkaSkoly"), "*-*", "V súhrne chýba poznámka školy.")
    _expect_text(page.locator("#koloPrijimaciehoKonania"), "1. kolo", "V súhrne chýba informácia o 1. kole.")

    _expect_text(page.locator("#dietaMenoSuhrn"), data.meno, "V súhrne chýba meno žiaka.")
    _expect_text(page.locator("#dietaPriezviskoSuhrn"), data.priezvisko, "V súhrne chýba priezvisko žiaka.")
    _expect_text(page.locator("#dietaRodnePriezviskoSuhrn"), data.priezvisko, "V súhrne chýba rodné priezvisko žiaka.")
    _expect_text(page.locator("#dietaRodneCisloSuhrn"), data.rodne_cislo, "V súhrne chýba rodné číslo žiaka.")
    _expect_text(
        page.locator("#dietaDatumNarodeniaSuhrn"),
        helper.rc_to_datum_narodenia(data.rodne_cislo),
        "V súhrne chýba dátum narodenia žiaka."
    )
    _expect_text(
        page.locator("#dietaPohlavieSuhrn"),
        helper.get_pohlavie(data.rodne_cislo),
        "V súhrne chýba pohlavie žiaka."
    )
    _expect_text(page.locator("#dietaMiestonarodeniaSuhrn"), "Slovensko", "V súhrne chýba miesto narodenia žiaka.")
    _expect_text(page.locator("#dietaNarodnostSuhrn"), "slovenská", "V súhrne chýba národnosť žiaka.")
    _expect_text(page.locator("#dietaStatnaPrislusnostSuhrn"), "Slovenská republika", "V súhrne chýba štátna príslušnosť žiaka.")
    _expect_text(page.locator("#dietaMaterinskyJazykSuhrn"), "slovenský", "V súhrne chýba materinský jazyk žiaka.")
    _expect_text(page.locator("#dietaInyMaterinskyJazykSuhrn"), "-", "V súhrne chýba údaj o inom materinskom jazyku.")
    _expect_text(
        page.locator("#dietaAdresaTrvalehoPobytuSuhrn"),
        "Prvej SNR 33/23, 90701, Myjava, Slovenská republika",
        "V súhrne chýba adresa trvalého pobytu žiaka."
    )

    _expect_text(page.locator("#dpZmenenaPracovnaSchopnost"), "Nie", "V súhrne chýba údaj o zmene pracovnej schopnosti.")
    _expect_text(page.locator("#dpSVVP"), "Nie", "V súhrne chýba údaj o ŠVVP.")
    _expect_text(page.locator("#dpMentalnePostihnutie"), "Nie", "V súhrne chýba údaj o mentálnom postihnutí.")
    _expect_text(page.locator("#dpPoznamka"), "-_-", "V súhrne chýba poznámka k doplňujúcim údajom.")


def _expect_school_section_ss(page: Page) -> None:
    _expect_text(page.locator("#skoly"), "910021624", "V sekcii školy chýba EDUID školy.")
    _expect_text(page.locator("#skoly"), "Stredná škola pre AT", "V sekcii školy chýba názov školy.")
    _expect_text(page.locator("#skoly"), "zlievač", "V sekcii školy chýba názov odboru.")
    _expect_text(page.locator("#skoly"), "Netalentový", "V sekcii školy chýba typ odboru.")
    _expect_text(page.locator("#skoly"), "1. termín", "V sekcii školy chýba termín prijímacej skúšky.")
    _expect_text(page.locator("#skoly"), "slovenský", "V sekcii školy chýba vyučovací jazyk.")
    _expect_text(page.locator("#skoly"), "Nie", "V sekcii školy chýba jedna z očakávaných odpovedí 'Nie'.")
    _expect_text(page.locator("#skoly"), "1 Stredná škola č. 1", "V sekcii školy chýba poradie školy.")


def _expect_guardian_section_ss(page: Page) -> None:
    _expect_text(page.locator("#zastupcovia"), "Osobné údaje zákonného zástupcu č. 1", "Chýba hlavička zákonného zástupcu č. 1.")
    _expect_text(page.locator("#zakonnyZastupcaMeno"), "Demeter", "Chýba meno zákonného zástupcu.")
    _expect_text(page.locator("#zakonnyZastupcaPriezvisko"), "Varga", "Chýba priezvisko zákonného zástupcu.")
    _expect_text(page.locator("#zakonnyZastupcaRodnePriezvisko"), "Varga", "Chýba rodné priezvisko zákonného zástupcu.")
    _expect_text(page.locator("#zakonnyZastupcaRodneCislo"), "840303/7269", "Chýba rodné číslo zákonného zástupcu.")
    _expect_text(page.locator("#zastupcovia"), "-", "Chýba očakávaný znak '-' v sekcii zástupcov.")
    _expect_text(page.locator("#zakonnyZastupcaDatumNarodenia"), "03.03.1984", "Chýba dátum narodenia zákonného zástupcu.")
    _expect_text(
        page.locator("#zakonnyZastupcaAdresaBydliska"),
        "Prvej SNR 33/23, 90701, Myjava, Slovenská republika",
        "Chýba adresa zákonného zástupcu."
    )
    _expect_text(page.locator("#zakonnyZastupcaEmail"), "katalontest987@gmail.com", "Chýba e-mail zákonného zástupcu.")
    _expect_text(page.locator("#zakonnyZastupcaTelefon"), "+421963258741", "Chýba telefón zákonného zástupcu.")
    _expect_text(page.locator("#zastupcovia"), "Osobné údaje zákonného zástupcu č. 2", "Chýba hlavička zákonného zástupcu č. 2.")
    _expect_text(page.locator("#zastupcovia"), "Druhý zákonný zástupca nie je známy.", "Chýba informácia o druhom zákonnom zástupcovi.")


def _expect_zs_section_ss(page: Page) -> None:
    _expect_text(page.locator("#prichodZiakaSuhrnZiadost"), "Zo ZŠ na Slovensku", "Chýba informácia o pôvode žiaka zo ZŠ.")
    _expect_text(page.locator("#eduidZSSuhrnZiadost"), "910021625", "Chýba EDUID základnej školy.")
    _expect_text(page.locator("#nazovZSSuhrnZiadost"), "Základná škola pre AT", "Chýba názov základnej školy.")
    _expect_text(page.locator("#rocnikSuhrnZiadost"), "9.", "Chýba ročník žiaka.")
    _expect_text(page.locator("#triedaSuhrnZiadost"), "9.A", "Chýba trieda žiaka.")
    _expect_text(page.locator("#rokSkolskejDochadzkySuhrnZiadost"), "9", "Chýba rok školskej dochádzky.")
    _expect_text(page.locator("#vyucovaciJazykVZSSuhrnZiadost"), "Slovenský", "Chýba vyučovací jazyk na ZŠ.")


def _expect_results_and_competitions_ss(page: Page) -> None:
    _expect_text(
        page.locator("#vysledky-vzdelavania-suhrn"),
        "6.ročník (2. polrok) Správanie veľmi dobré 7.ročník (2. polrok) Správanie uspokojivé 8.ročník (2. polrok) Správanie menej uspokojivé 9.ročník (1. polrok) Správanie veľmi dobré",
        "V sekcii výsledkov vzdelávania chýbajú očakávané údaje o správaní."
    )

    _expect_text(page.locator("#sutaze-suhrn"), "Súťaž", "V sekcii súťaží chýba nadpis alebo typ položky.")
    _expect_text(page.locator("#sutaze-suhrn"), "Preteky v kosení", "V sekcii súťaží chýba názov súťaže.")
    _expect_text(page.locator("#sutaze-suhrn"), "2. miesto - krajská", "V sekcii súťaží chýba umiestnenie.")
    _expect_text(page.locator("#sutaze-suhrn"), "Súťaže zručnosti", "V sekcii súťaží chýba kategória súťaže.")
    _expect_text(page.locator("#sutaze-suhrn"), "Školský rok: 2024/2025", "V sekcii súťaží chýba školský rok.")


@pytest.mark.regres1kolo
def test_pridanie_papierovej_prihlasky_SS_1_kolo(page: Page) -> None:
    data = Data.generate_unique_person(min_age=15, max_age=17)
    login = LoginPage(page)
    prihlaska = PapierovaPrihlaskaSS(page)
    helper = Helper()
    den, mesiac, rok = helper.aktualny_datum()

    login.login_as_riaditel(username, password, "910021624")
    prihlaska.click_on_pridaj_prihlasku_1_kolo()
    prihlaska.step_1_osobne_udaje(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska.step_2_SVVP()
    prihlaska.step_3_vyber_skoly_1_kolo()
    prihlaska.step_4_ZZ()
    prihlaska.step_5_navsteva_ZS()
    prihlaska.step_6_znamky()
    prihlaska.step_7_sutaze()
    prihlaska.step_8_prilohy()
    prihlaska.step_9_ostatne_udaje(den, mesiac, rok)

    _expect_summary_ss_1_kolo(page, data, helper, den, mesiac, rok)
    _expect_school_section_ss(page)
    _expect_guardian_section_ss(page)
    _expect_zs_section_ss(page)
    _expect_results_and_competitions_ss(page)

    _expect_visible(page.locator(".prilohaItem"), "V súhrne sa nezobrazila príloha.")

    prihlaska.click_on_odoslat_prihlasku()

    expect(
        page,
        "Po odoslaní papierovej prihlášky sa neotvorila stránka riaditeľa."
    ).to_have_url(re.compile(r".*/Riaditel.*"), timeout=60000)

    _expect_text(
        page.locator("#riaditel-home-page"),
        "Prihlášku pre dieťa ste úspešne pridali.",
        "Po odoslaní sa nezobrazila úspešná hláška o pridaní prihlášky."
    )

    prihlaska.najdi_prihlasku_1_kolo(data.meno, data.priezvisko)

    _expect_text(
        page.locator("#sub-riaditel-prihlasky"),
        f"{data.priezvisko} {data.meno}",
        "V zozname prihlášok sa nenašlo meno a priezvisko žiaka."
    )
    _expect_text(
        page.locator("#sub-riaditel-prihlasky"),
        "V spracovaní",
        "V zozname prihlášok sa nezobrazuje stav 'V spracovaní'."
    )

    prihlaska.click_on_zobrazit_prihlasku()

    _expect_text(
        page.locator("#detail-prihlasky-riad-SS-content"),
        "Papierovo",
        "V detaile prihlášky chýba informácia, že bola podaná papierovo."
    )
    _expect_text(
        page.locator("#detail-prihlasky-riad-SS-content"),
        "1. kolo",
        "V detaile prihlášky chýba informácia o 1. kole."
    )