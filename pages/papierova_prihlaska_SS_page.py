from playwright.sync_api import Page
from pages.base_page import BasePage


class PapierovaPrihlaskaSS(BasePage):
    KOLO_2 = "2"
    ODBOR_2_KOLO = "2b3813df-fbe6-41ce-be28-0efc6dfaca83"
    ODBOR_1_KOLO = "fa97e1ee-cf77-4880-853a-5972261cdb4c"

    KRAJINA = "slovenska rep"
    KRAJINA_LABEL = "Slovenská republika"
    OBEC = "pali"
    OBEC_LABEL = "Palín (Michalovce)"
    ULICA = "korce"
    ULICA_LABEL = "Korčekova"
    SUPISNE_CISLO = "12"
    ORIENTACNE_CISLO = "45"
    PSC = "89516"

    SVVP_POZNAMKA = "-_-"

    ZZ_MENO = "Demeter"
    ZZ_PRIEZVISKO = "Varga"
    ZZ_RC = "840303/7269"
    ZZ_EMAIL = "katalontest987@gmail.com"
    ZZ_TELEFON = "+421963258741"

    EDUID_ZS = "910021625"
    TRIEDA = "9.A"
    ROCNIK = "9"
    ROK_SKOLSKEJ_DOCHADZKY = "9"

    SUTAZ_NAZOV = "Preteky v kosení"
    SUTAZ_DRUH = "3"
    SUTAZ_UROVEN = "3"
    SUTAZ_SKOLSKY_ROK = "2024/2025"

    SUBOR_PRILOHA = "./data/Dokument.pdf"
    POZNAMKA_SKOLY = "*-*"

    def __init__(self, page: Page):
        super().__init__(page)

    def _click_dalej(self, nazov_kroku: str):
        self._safe_click(
            self.page.get_by_role("button", name="Ďalej"),
            nazov_kroku
        )

    def _odstran_predmety(self, pocet: int, nazov_prvku: str):
        for _ in range(pocet):
            self._safe_click(
                self.page.get_by_role("button", name="Odstrániť").nth(1),
                nazov_prvku
            )

    def _potvrd_existujucu_prihlasku_ak_treba(self):
        hlaska = self.page.get_by_text("Pre tohto žiaka už existuje prihláška.", exact=True)
        if hlaska.is_visible():
            self._safe_click(
                self.page.locator("button.btn-confirm.govuk-button.govuk-button__large.last-focusable"),
                "Potvrdiť existujúcu prihlášku"
            )

            pridat_btn = self.page.locator("button").filter(has_text="Pridať prihlášku").last
            if pridat_btn.is_visible():
                self._safe_click(
                    pridat_btn,
                    "Pridať prihlášku po potvrdení"
                )

    def click_on_pridaj_prihlasku(self):
        self.page.wait_for_load_state("networkidle")
        self._safe_select(
            self.page.get_by_label("Kolo"),
            self.KOLO_2,
            "Kolo"
        )
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.locator("#btn-vytvorit-prihlasku"),
            "Vytvoriť prihlášku"
        )

    def click_on_pridaj_prihlasku_1_kolo(self):
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.locator("#btn-vytvorit-prihlasku"),
            "Vytvoriť prihlášku - 1. kolo"
        )

    def step_1_osobne_udaje(self, meno: str, priezvisko: str, rc: str):
        self._safe_check(
            self.page.locator("#maDietaRCRadio_option_0"),
            "Dieťa má rodné číslo"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Rodné číslo *"),
            rc,
            "Rodné číslo"
        )
        self._click_dalej("Ďalej - rodné číslo")

        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

        self._potvrd_existujucu_prihlasku_ak_treba()

        self._safe_fill(
            self.page.get_by_role("textbox", name="Meno *"),
            meno,
            "Meno"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Priezvisko *"),
            priezvisko,
            "Priezvisko"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Rodné priezvisko"),
            priezvisko,
            "Rodné priezvisko"
        )
        self._safe_fill(
            self.page.locator("#input-miestoNarodenia"),
            "Slovensko",
            "Miesto narodenia"
        )

        self._safe_fill(
            self.page.locator("#adresaTPKrajina input.autocomplete-input"),
            self.KRAJINA,
            "Krajina"
        )
        self._safe_click(
            self.page.locator("#adresaTPKrajina").get_by_text(self.KRAJINA_LABEL, exact=True),
            "Slovenská republika"
        )

        self._safe_fill(
            self.page.locator("#adresaTPObec input.autocomplete-input"),
            self.OBEC,
            "Obec"
        )
        self._safe_click(
            self.page.locator("#adresaTPObec").get_by_text(self.OBEC_LABEL, exact=True),
            "Palín (Michalovce)"
        )

        self._safe_fill(
            self.page.locator("#adresaTPUlica input.autocomplete-input"),
            self.ULICA,
            "Ulica"
        )
        self._safe_click(
            self.page.locator("#adresaTPUlica").get_by_text(self.ULICA_LABEL, exact=True),
            "Korčekova"
        )

        self._safe_fill(
            self.page.get_by_role("textbox", name="Súpisné číslo"),
            self.SUPISNE_CISLO,
            "Súpisné číslo"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Orientačné číslo *"),
            self.ORIENTACNE_CISLO,
            "Orientačné číslo"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="PSČ *"),
            self.PSC,
            "PSČ"
        )

        self._click_dalej("Ďalej - osobné údaje")
        self._click_dalej("Ďalej - pokračovanie po osobných údajoch")

    def step_2_SVVP(self):
        self._safe_check(
            self.page.locator("#zmenenaPracovnaSchopnostRadio_option_1"),
            "Zmenená pracovná schopnosť - Nie"
        )
        self._safe_check(
            self.page.locator("#specialneVVP_option_1"),
            "Špeciálne VVP - Nie"
        )
        self._safe_check(
            self.page.locator("#mentalnePostihnutie_option_1"),
            "Mentálne postihnutie - Nie"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Poznámka:"),
            self.SVVP_POZNAMKA,
            "Poznámka"
        )
        self._click_dalej("Ďalej - SVVP")

    def step_3_vyber_skoly(self):
        self._safe_click(
            self.page.get_by_role("link", name="Pridať odbor mojej školy"),
            "Pridať odbor mojej školy"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať do prihlášky").first,
            "Pridať do prihlášky"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať odbory a odísť"),
            "Pridať odbory a odísť"
        )
        self._click_dalej("Ďalej - výber školy 1")
        self._click_dalej("Ďalej - výber školy 2")

    def step_3_vyber_skoly_1_kolo(self):
        self._safe_click(
            self.page.get_by_role("link", name="Pridať odbor mojej školy"),
            "Pridať odbor mojej školy - 1. kolo"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať do prihlášky").nth(1),
            "Pridať do prihlášky - 1. kolo"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať odbory a odísť"),
            "Pridať odbory a odísť"
        )
        self._click_dalej("Ďalej - výber školy 1. kolo 1")
        self._click_dalej("Ďalej - výber školy 1. kolo 2")

    def step_4_ZZ(self):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Meno *"),
            self.ZZ_MENO,
            "Meno zákonného zástupcu"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Priezvisko *"),
            self.ZZ_PRIEZVISKO,
            "Priezvisko zákonného zástupcu"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Rodné číslo *"),
            self.ZZ_RC,
            "Rodné číslo zákonného zástupcu"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="E-mail"),
            self.ZZ_EMAIL,
            "E-mail zákonného zástupcu"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Telefónne číslo *"),
            self.ZZ_TELEFON,
            "Telefónne číslo zákonného zástupcu"
        )
        self._safe_check(
            self.page.get_by_role("radio", name="Druhý zákonný zástupca nie je"),
            "Druhý zákonný zástupca nie je"
        )

        self.page.wait_for_timeout(1000)

        self._click_dalej("Ďalej - zákonný zástupca")
        if self.page.get_by_role("radio", name="Druhý zákonný zástupca nie je").is_visible():
            self._click_dalej("Ďalej - zákonný zástupca opakovanie")

    def step_5_navsteva_ZS(self):
        self._safe_fill(
            self.page.get_by_role("textbox", name="EDUID základnej školy *"),
            self.EDUID_ZS,
            "EDUID základnej školy"
        )
        self._safe_click(
            self.page.get_by_text("Informácie o základnej škole Vyplňte dodatočné informácie o základnej škole."),
            "Informácie o základnej škole"
        )
        self._safe_select(
            self.page.locator("#select-rocnikSKSelect"),
            self.ROCNIK,
            "Ročník"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Trieda *"),
            self.TRIEDA,
            "Trieda"
        )
        self._safe_select(
            self.page.locator("#select-rokSkolskejDochadzkySKSelect"),
            self.ROK_SKOLSKEJ_DOCHADZKY,
            "Rok školskej dochádzky"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Názov základnej školy *", exact=True),
            "slovenský",
            "Názov základnej školy"
        )
        self._safe_click(
            self.page.locator("#vyucovaciJazykVZakladnejSkoleSKAutocomplete").get_by_text("slovenský", exact=True),
            "slovenský"
        )

        self.page.wait_for_timeout(1000)

        self._click_dalej("Ďalej - návšteva ZŠ")

    def step_6_znamky(self):
        self._safe_select(
            self.page.locator("#select-hodnotenie-1-1"),
            "29",
            "Hodnotenie 6. ročník"
        )
        self._odstran_predmety(18, "Odstrániť predmet zo 6. ročníka")

        self._safe_click(
            self.page.get_by_text("7. ročník"),
            "7. ročník"
        )
        self._safe_select(
            self.page.locator("#select-hodnotenie-2-1"),
            "30",
            "Hodnotenie 7. ročník"
        )
        self._odstran_predmety(18, "Odstrániť predmet zo 7. ročníka")

        self._safe_click(
            self.page.get_by_text("8. ročník"),
            "8. ročník"
        )
        self._safe_select(
            self.page.locator("#select-hodnotenie-3-1"),
            "31",
            "Hodnotenie 8. ročník"
        )
        self._odstran_predmety(18, "Odstrániť predmet z 8. ročníka")

        self._safe_click(
            self.page.get_by_text("9. ročník"),
            "9. ročník"
        )
        self._safe_select(
            self.page.locator("#select-hodnotenie-4-1"),
            "29",
            "Hodnotenie 9. ročník"
        )
        self._odstran_predmety(18, "Odstrániť predmet z 9. ročníka")

        self._click_dalej("Ďalej - známky")

    def step_7_sutaze(self):
        self._safe_click(
            self.page.get_by_role("button", name="Pridať súťaž"),
            "Pridať súťaž"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Názov súťaže *"),
            self.SUTAZ_NAZOV,
            "Názov súťaže"
        )
        self._safe_select(
            self.page.get_by_label("Druh súťaže"),
            self.SUTAZ_DRUH,
            "Druh súťaže"
        )
        self._safe_select(
            self.page.get_by_label("Úroveň súťaže"),
            self.SUTAZ_UROVEN,
            "Úroveň súťaže"
        )
        self._safe_check(
            self.page.get_by_role("radio", name="2. miesto"),
            "2. miesto"
        )
        self._safe_select(
            self.page.get_by_label("Školský rok"),
            self.SUTAZ_SKOLSKY_ROK,
            "Školský rok"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať", exact=True),
            "Pridať súťaž"
        )
        self._click_dalej("Ďalej - súťaže")

    def step_8_prilohy(self):
        self._safe_click(
            self.page.get_by_text("Olympiáda / súťaž: Preteky v kosení Nenahrané Nenahrané Nahrané"),
            "Príloha k súťaži"
        )
        with self.page.expect_file_chooser() as fc_info:
            self._safe_click(
                self.page.get_by_role("link", name="Vybrať súbor"),
                "Vybrať súbor"
            )

        file_chooser = fc_info.value
        file_chooser.set_files(self.SUBOR_PRILOHA)

        self._click_dalej("Ďalej - prílohy")

    def step_9_ostatne_udaje(self, den: str, mesiac: str, rok: str):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Deň"),
            den,
            "Deň"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Mesiac"),
            mesiac,
            "Mesiac"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Rok"),
            rok,
            "Rok"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Poznámka školy:"),
            self.POZNAMKA_SKOLY,
            "Poznámka školy"
        )
        self._click_dalej("Ďalej - ostatné údaje")

    def click_on_odoslat_prihlasku(self):
        self._safe_click(
            self.page.get_by_role("button", name="Pridať prihlášku"),
            "Pridať prihlášku"
        )
        self.page.wait_for_load_state("load", timeout=60000)

    def najdi_prihlasku_2_kolo(self, meno: str, priezvisko: str):
        self._safe_select(
            self.page.get_by_label("Odbor"),
            self.ODBOR_2_KOLO,
            "Odbor - 2. kolo"
        )
        self.page.wait_for_load_state("networkidle")
        self._safe_fill(
            self.page.get_by_role("textbox", name="Vyhľadávanie v prihláškach"),
            f"{meno} {priezvisko}",
            "Vyhľadávanie v prihláškach"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Hľadať"),
            "Hľadať"
        )

    def najdi_prihlasku_1_kolo(self, meno: str, priezvisko: str):
        self._safe_select(
            self.page.get_by_label("Odbor"),
            self.ODBOR_1_KOLO,
            "Odbor - 1. kolo"
        )
        self.page.wait_for_load_state("networkidle")
        self._safe_fill(
            self.page.get_by_role("textbox", name="Vyhľadávanie v prihláškach"),
            f"{meno} {priezvisko}",
            "Vyhľadávanie v prihláškach"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Hľadať"),
            "Hľadať"
        )
        self.page.wait_for_load_state("networkidle", timeout=60000)

    def click_on_zobrazit_prihlasku(self):
        self.page.locator("div.page-overlay").wait_for(state="hidden", timeout=60000)
        self._safe_click(
            self.page.locator("div.riaditel-prihlasky-cell.akcia-cell button:visible").nth(0),
            "Zobraziť prihlášku"
        )