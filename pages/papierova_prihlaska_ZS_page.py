from playwright.sync_api import Page
from pages.base_page import BasePage


class PapierovaPrihlaskaZS(BasePage):
    KRAJINA_TRVALEHO_POBYTU = "Indi"
    KRAJINA_TRVALEHO_POBYTU_LABEL = "Indická republika"
    ADRESA_TRVALEHO_POBYTU = "New Dhili, 879/71"
    MATERINSKY_JAZYK = "an"
    MATERINSKY_JAZYK_LABEL = "anglický"

    KRAJINA_KORESPONDENCNEJ_ADRESY = "slovenska re"
    KRAJINA_KORESPONDENCNEJ_ADRESY_LABEL = "Slovenská republika"
    ADRESA_KORESPONDENCNA = "Prvej SNR 33/23"
    ADRESA_KORESPONDENCNA_LABEL = "Prvej SNR 33/23, 90701, Myjava, Myjava"

    ZZ_MENO = "Patrik"
    ZZ_PRIEZVISKO = "Kvarga"
    ZZ_RC = "650204/9367"
    ZZ_TELEFON = "+421966332557"

    POZNAMKA = "ŠVVP"
    POZNAMKA_SKOLY = "Poznámka školy."

    def __init__(self, page: Page):
        super().__init__(page)

    def _click_dalej(self, nazov_kroku: str):
        self._safe_click(
            self.page.get_by_role("button", name="Ďalej"),
            nazov_kroku
        )

    def click_on_pridaj_prihlasku(self):
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.locator("#btn-vytvorit-prihlasku:visible"),
            "Pridať prihlášku"
        )

    def step_1_osobne_udaje(self, meno: str, priezvisko: str, rc: str):
        self.page.wait_for_load_state("networkidle")

        self._safe_check(
            self.page.locator("#maDietaRCRadio_option_0"),
            "Dieťa má rodné číslo"
        )
        self._safe_fill(
            self.page.locator("#input-rodneCislo"),
            rc,
            "Rodné číslo"
        )
        self._click_dalej("Ďalej - rodné číslo")

        self._safe_fill(
            self.page.locator("#input-krstneMeno"),
            meno,
            "Meno"
        )
        self._safe_fill(
            self.page.locator("#input-priezvisko"),
            priezvisko,
            "Priezvisko"
        )
        self._safe_fill(
            self.page.locator("#input-rodnePriezvisko"),
            priezvisko,
            "Rodné priezvisko"
        )
        self._safe_fill(
            self.page.locator("#input-miestoNarodenia"),
            "Slovensko",
            "Miesto narodenia"
        )

        self._safe_fill(
            self.page.locator("#adresaTPKrajina > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input"),
            self.KRAJINA_TRVALEHO_POBYTU,
            "Krajina trvalého pobytu"
        )
        self._safe_click(
            self.page.get_by_text(self.KRAJINA_TRVALEHO_POBYTU_LABEL),
            "Indická republika"
        )

        self._safe_fill(
            self.page.locator("#input-adresaTPAdresa"),
            self.ADRESA_TRVALEHO_POBYTU,
            "Adresa"
        )

        self._safe_fill(
            self.page.locator("#inyMaterinskyJazyk input.autocomplete-input"),
            self.MATERINSKY_JAZYK,
            "Materinský jazyk"
        )
        self._safe_click(
            self.page.locator("#inyMaterinskyJazyk").get_by_text(self.MATERINSKY_JAZYK_LABEL, exact=True),
            "anglický"
        )

        self._safe_check(
            self.page.locator("#zvycajnaAdresaradio_option_1"),
            "Iná adresa"
        )

        self._safe_fill(
            self.page.locator("#adresaZAKrajina > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input"),
            self.KRAJINA_KORESPONDENCNEJ_ADRESY,
            "Krajina korešpondenčnej adresy"
        )
        self._safe_click(
            self.page.locator("#adresaZAKrajina").get_by_text(self.KRAJINA_KORESPONDENCNEJ_ADRESY_LABEL, exact=True),
            "Slovenská republika - korešpondenčná adresa"
        )

        self._safe_fill(
            self.page.locator("#adresaZAAdresaRA input.autocomplete-input"),
            self.ADRESA_KORESPONDENCNA,
            "Adresa obvyklého pobytu"
        )
        self._safe_click(
            self.page.locator("#adresaZAAdresaRA").get_by_text(self.ADRESA_KORESPONDENCNA_LABEL, exact=True),
            self.ADRESA_KORESPONDENCNA_LABEL
        )

        self._click_dalej("Ďalej - osobné údaje")
        self._click_dalej("Ďalej - pokračovanie po osobných údajoch")

    def step_2_SVVP(self):
        self._safe_check(
            self.page.get_by_role("radio", name="Etická"),
            "Výchova - Etická"
        )
        self._safe_check(
            self.page.locator("#zsDPDStravovanieRadio_option_0"),
            "Stravovanie - Áno"
        )
        self._safe_check(
            self.page.locator("#zsDPDSkolskyKlubRadio_option_1"),
            "Školský klub - Nie"
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
            self.page.get_by_role("textbox", name="Poznámka:"),
            self.POZNAMKA,
            "Poznámka"
        )

        self._click_dalej("Ďalej - SVVP 1")
        self._click_dalej("Ďalej - SVVP 2")
        self._click_dalej("Ďalej - SVVP 3")

    def step_3_vyber_skoly(self):
        pass

    def step_4_ZZ(self):
        self._safe_fill(
            self.page.locator("#input-zastupca1Meno"),
            self.ZZ_MENO,
            "Meno zákonného zástupcu"
        )
        self._safe_fill(
            self.page.locator("#input-zastupca1Priezvisko"),
            self.ZZ_PRIEZVISKO,
            "Priezvisko zákonného zástupcu"
        )
        self._safe_fill(
            self.page.locator("#input-zastupca1RodneCislo"),
            self.ZZ_RC,
            "Rodné číslo zákonného zástupcu"
        )
        self._safe_fill(
            self.page.locator("#input-zastupca1Telefon"),
            self.ZZ_TELEFON,
            "Telefónne číslo zákonného zástupcu"
        )

        self._click_dalej("Ďalej - ZZ 1")

        self.page.wait_for_timeout(1000)
        self.page.wait_for_load_state("networkidle")

        self._click_dalej("Ďalej - ZZ 2")

        telefon = self.page.locator("#input-zastupca1Telefon")
        if telefon.is_visible():
            self._click_dalej("Ďalej - ZZ opakovanie po zobrazení telefónu")

        self.page.wait_for_timeout(1000)

        self._click_dalej("Ďalej - ZZ finálne")

    def step_5_navsteva_ZS(self):
        pass

    def step_6_znamky(self):
        pass

    def step_7_sutaze(self):
        pass

    def step_8_prilohy(self):
        pass

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
            "Odoslať papierovú prihlášku"
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
            "Hľadať prihlášku"
        )

    def click_on_zobrazit_prihlasku(self):
        self._safe_click(
            self.page.locator("div.riaditel-prihlasky-cell.akcia-cell").locator("button").nth(0),
            "Zobraziť prihlášku"
        )

    def click_on_skontrolovana(self):
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.get_by_role("button", name="Označiť ako skontrolovaná"),
            "Označiť ako skontrolovaná"
        )

    def click_on_odoslat_na_SS(self):
        self._safe_click(
            self.page.get_by_role("button", name="Odoslať na stredné školy"),
            "Odoslať na stredné školy"
        )