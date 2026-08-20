from playwright.sync_api import Page
from pages.base_page import BasePage


class PapierovaPrihlaskaMS(BasePage):
    KRAJINA = "slovenská rep"
    KRAJINA_LABEL = "Slovenská republika"
    OBEC = "Kord"
    OBEC_LABEL = "Kordíky (Banská Bystrica)"
    ULICA = "Miksa"
    ULICA_LABEL = "Miksáthova"
    SUPISNE_CISLO = "8"
    ORIENTACNE_CISLO = "635"
    PSC = "02845"

    DATUM_NASTUP_DEN = "1"
    DATUM_NASTUP_MESIAC = "9"
    DATUM_NASTUP_ROK = "2026"

    ZZ_MENO = "Peter"
    ZZ_PRIEZVISKO = "Fodrok"
    ZZ_RC = "860201/7842"
    ZZ_EMAIL = "katalontest987@gmail.com"
    ZZ_TELEFON = "+421905866541"

    SUBOR_PRILOHA = "./data/Dokument.pdf"
    POZNAMKA_SKOLY = ":)"

    def __init__(self, page: Page):
        super().__init__(page)

    def _click_dalej(self, nazov_kroku: str):
        self._safe_click(
            self.page.get_by_role("button", name="Ďalej"),
            nazov_kroku
        )

    def _potvrd_existujucu_prihlasku_ak_treba(self):
        hlaska = self.page.get_by_text("Pre toto dieťa už existuje prihláška.", exact=True)
        self.page.wait_for_timeout(2000)
        hlaska1 = self.page.get_by_text("Prihláška už existuje", exact=True)
        if hlaska.is_visible() or hlaska1.is_visible():
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
        self._safe_click(
            self.page.get_by_role("button", name="Pridať prihlášku"),
            "Pridať prihlášku"
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

        self._potvrd_existujucu_prihlasku_ak_treba()

        self.page.wait_for_load_state("networkidle")

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
            "Kordíky (Banská Bystrica)"
        )

        self._safe_fill(
            self.page.locator("#adresaTPUlica input.autocomplete-input"),
            self.ULICA,
            "Ulica"
        )
        self._safe_click(
            self.page.locator("#adresaTPUlica").get_by_text(self.ULICA_LABEL, exact=True),
            "Miksáthova"
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
            self.page.get_by_role("radio", name="celodennú výchovu a vzdelá"),
            "Celodennú výchovu a vzdelávanie"
        )
        self._safe_check(
            self.page.locator("#DPDSVVPRadio_option_1"),
            "ŠVVP - Nie"
        )
        self._safe_check(
            self.page.locator("#DPDDietaSNadanimRadio_option_1"),
            "Dieťa s nadaním - Nie"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Deň"),
            self.DATUM_NASTUP_DEN,
            "Deň nástupu"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Mesiac"),
            self.DATUM_NASTUP_MESIAC,
            "Mesiac nástupu"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Rok"),
            self.DATUM_NASTUP_ROK,
            "Rok nástupu"
        )
        self._click_dalej("Ďalej - SVVP")

    def step_3_vyber_skoly(self):
        self._click_dalej("Ďalej - výber školy 1")
        self._click_dalej("Ďalej - výber školy 2")
        self._click_dalej("Ďalej - výber školy 3")

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

        self.page.wait_for_timeout(1000)

        self._click_dalej("Ďalej - zákonný zástupca")
        if self.page.get_by_role("textbox", name="Telefónne číslo *").is_visible():
            self._click_dalej("Ďalej - zákonný zástupca opakovanie")

    def step_5_prilohy(self):
        self._safe_click(
            self.page.get_by_text("Potvrdenie o zdravotnej spôsobilosti (materská škola) Nenahrané Nenahrané"),
            "Potvrdenie o zdravotnej spôsobilosti"
        )

        with self.page.expect_file_chooser() as fc_info:
            self._safe_click(
                self.page.get_by_role("link", name="Vybrať súbor"),
                "Vybrať súbor"
            )

        file_chooser = fc_info.value
        file_chooser.set_files(self.SUBOR_PRILOHA)

        self._click_dalej("Ďalej - prílohy")

    def step_6_ostatne_udaje(self, den: str, mesiac: str, rok: str):
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

    def najdi_prihlasku(self, meno: str, priezvisko: str):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Vyhľadávanie v meno,"),
            f"{meno} {priezvisko}",
            "Vyhľadávanie prihlášky"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Hľadať"),
            "Hľadať"
        )
        self._safe_click(
            self.page.locator("button").filter(has_text="Zobraziť").first,
            "Zobraziť prihlášku"
        )