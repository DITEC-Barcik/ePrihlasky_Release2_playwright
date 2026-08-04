from playwright.sync_api import Page
from pages.base_page import BasePage


class PrihlaskaZS(BasePage):
    KRAJINA = "slovenska re"
    KRAJINA_LABEL = "Slovenská republika"
    OBEC = "Brusno"
    OBEC_LABEL = "Brusno (Banská Bystrica)"
    ULICA = "cibulk"
    ULICA_LABEL = "Cibulková"
    SUPISNE_CISLO = "8"
    ORIENTACNE_CISLO = "63"
    PSC = "03687"

    def __init__(self, page: Page):
        super().__init__(page)

    def _click_dalej(self, nazov_kroku: str):
        self._safe_click(
            self.page.get_by_role("button", name="Ďalej", exact=True),
            nazov_kroku
        )

    def pridanie_prihlasky(self):
        self.page.wait_for_load_state("networkidle")

        self._safe_click(
            self.page.get_by_text("Vytvoriť prihlášku").first,
            "Vytvoriť prihlášku"
        )
        self._safe_check(
            self.page.get_by_role("radio", name="Základná škola Prihlášku môž"),
            "Typ prihlášky - Základná škola"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať", exact=True),
            "Pridať"
        )

    def step_1_pridat_dieta(self, meno: str, priezvisko: str, rodne_cislo: str):
        self.page.wait_for_load_state("networkidle")

        self._safe_check(
            self.page.get_by_role("radio", name="Iné dieťa Pridajte dieťa"),
            "Iné dieťa"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať dieťa"),
            "Pridať dieťa"
        )

        self._safe_check(
            self.page.locator("#maDietaRCRadio_option_0"),
            "Dieťa má rodné číslo"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Rodné číslo *"),
            rodne_cislo,
            "Rodné číslo"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Krstné meno *"),
            meno,
            "Krstné meno"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Priezvisko *"),
            priezvisko,
            "Priezvisko"
        )

        self._safe_click(
            self.page.locator("#step-1").get_by_role("button", name="Ďalej"),
            "Ďalej - krok 1"
        )

        self._safe_fill(
            self.page.locator("#input-miestoNarodenia"),
            "Slovensko",
            "Miesto narodenia"
        )
        self._safe_fill(
            self.page.locator("#adresaTPKrajina").get_by_role("textbox"),
            self.KRAJINA,
            "Krajina"
        )
        self._safe_click(
            self.page.locator("#adresaTPKrajina").get_by_text(self.KRAJINA_LABEL, exact=True),
            "Slovenská republika"
        )

        self._safe_fill(
            self.page.locator("#adresaTPObec > .govuk-form-group > .input-wrapper > .govuk-input.autocomplete-input"),
            self.OBEC,
            "Obec"
        )
        self._safe_click(
            self.page.get_by_text(self.OBEC_LABEL),
            "Brusno (Banská Bystrica)"
        )

        self._safe_fill(
            self.page.get_by_role("textbox", name="Krajina *"),
            self.ULICA,
            "Ulica"
        )
        self._safe_click(
            self.page.get_by_text(self.ULICA_LABEL),
            "Cibulková"
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

        self._safe_click(
            self.page.locator("#step-2").get_by_role("button", name="Pridať dieťa"),
            "Pridať dieťa - potvrdenie"
        )
        self._click_dalej("Ďalej po pridaní dieťaťa")
        self._click_dalej("Ďalej na ďalší krok")

    def step_2_SVVP(self):
        self._safe_check(
            self.page.get_by_role("radio", name="Náboženská"),
            "Typ výchovy - Náboženská"
        )
        self._safe_check(
            self.page.get_by_role("radio", name="Rímskokatolícka"),
            "Vierovyznanie - Rímskokatolícka"
        )
        self._safe_check(
            self.page.locator("#zsDPDStravovanieRadio_option_0"),
            "Stravovanie - Áno"
        )
        self._safe_check(
            self.page.locator("#zsDPDSkolskyKlubRadio_option_0"),
            "Školský klub - Áno"
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
            "ŠVVP",
            "Poznámka"
        )
        self._click_dalej("Ďalej - krok SVVP")

    def step_3_vyber_skoly(self, nazov_skoly: str):
        self._safe_check(
            self.page.get_by_role("radio", name="Hľadať podľa názvu školy"),
            "Hľadať podľa názvu školy"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Názov školy alebo jej adresa *"),
            nazov_skoly,
            "Názov školy alebo jej adresa"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Hľadať"),
            "Hľadať"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Základná škola pre AT Pridať do prihlášky"),
            "Pridať školu do prihlášky"
        )
        self._click_dalej("Ďalej - výber školy 1")
        self._click_dalej("Ďalej - výber školy 2")
        self._click_dalej("Ďalej - výber školy 3")
        self._safe_click(
            self.page.get_by_role("button", name="Mám skontrolované"),
            "Mám skontrolované"
        )

    def step_4_ZZ(self):
        self._safe_check(
            self.page.get_by_role("radio", name="Druhý zákonný zástupca nie je"),
            "Druhý zákonný zástupca nie je známy"
        )
        self._click_dalej("Ďalej - krok zákonný zástupca")

    def step_5_prilohy(self):
        self._click_dalej("Ďalej - krok prílohy")

    def accept_terms_and_submit(self):
        self._safe_click(
            self.page.locator("#cestnePrehlasenie > .checkmark"),
            "Čestné prehlásenie"
        )
        self._safe_click(
            self.page.locator("#suhlasOsobneUdaje > .checkmark"),
            "Súhlas s osobnými údajmi"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Odoslať prihlášku"),
            "Odoslať prihlášku"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Odoslať prihlášku").nth(1),
            "Potvrdiť odoslanie prihlášky"
        )

    def click_on_prejst_na_prihlasky(self):
        self._safe_click(
            self.page.get_by_role("button", name="Prejsť na prihlášky"),
            "Prejsť na prihlášky"
        )