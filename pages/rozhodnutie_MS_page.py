import re
import os
from playwright.sync_api import Page, expect
from pages.base_page import BasePage

SUBOR_PRILOHA = "./data/Dokument.pdf"
PODAVATEL_ODVOLANIA_ID = "6abc23b2-9039-45f3-b421-9d95dc93e9e2"


class RozhodnutieMS(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def navigate_to_rozhodnutia(self):
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.get_by_role("link", name="Rozhodnutia"),
            "Rozhodnutia"
        )
        self.page.wait_for_load_state("networkidle")

    def search(self, meno: str):
        search_box = self.page.get_by_role("textbox", name="Vyhľadávanie v meno,")
        expect(search_box).to_be_visible()
        self.page.wait_for_timeout(2000)
        search_box.fill(meno)
        expect(search_box).to_have_value(meno)
        self._safe_click(
            self.page.get_by_role("button", name="Hľadať"),
            "Hľadať"
        )
        self.page.wait_for_load_state("networkidle")

    def select_first(self):
        self._safe_click(
            self.page.get_by_role("button", name="Vybrať").first,
            "Vybrať"
        )

    def click_upravit_rozhodnutie(self):
        self._safe_click(
            self.page.get_by_role("link", name="Upraviť rozhodnutie"),
            "Upraviť rozhodnutie"
        )

    def click_prejst_na_podpis(self):
        self._safe_click(
            self.page.get_by_role("button", name="Prejsť na podpis"),
            "Prejsť na podpis"
        )

    def autorizovat_a_vygenerovat(self, login: str = None, heslo: str = None):
        if login is None:
            login = os.getenv("EPRIHLASKY_RIADITEL_USERNAME", "")
        if heslo is None:
            heslo = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD", "")
        self._safe_click(
            self.page.get_by_role("button", name="Autorizovať a vygenerovať (1)"),
            "Autorizovať a vygenerovať"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Prihlasovacie meno *"),
            login,
            "Prihlasovacie meno"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Heslo *"),
            heslo,
            "Heslo"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Prihlásiť sa"),
            "Prihlásiť sa"
        )

    def click_spat_na_rozhodnutia(self):
        self._safe_click(
            self.page.get_by_role("button", name="Späť na rozhodnutia"),
            "Späť na rozhodnutia"
        )

    def wait_for_generation_complete(self, meno: str, max_retries: int = 15, interval_ms: int = 20000):
        self.search(meno)
        expect(self.page.locator("#sub-riaditel-rozhodnutia")).to_contain_text("Prebieha generovanie rozhodnutia.")
        for _ in range(max_retries):
            self.page.wait_for_timeout(interval_ms)
            self._safe_click(
                self.page.get_by_role("button", name="Hľadať"),
                "Hľadať - čakanie na generovanie"
            )
            self.page.wait_for_load_state("networkidle")
            if not self.page.locator("#sub-riaditel-rozhodnutia").filter(
                has_text="Prebieha generovanie rozhodnutia."
            ).is_visible():
                break

    def click_zaevidovat_odvolanie(self):
        self._safe_click(
            self.page.get_by_role("link", name="Zaevidovať odvolanie"),
            "Zaevidovať odvolanie"
        )

    def fill_odvolanie_form(self, den: str, mesiac: str, rok: str):
        self._safe_fill(
            self.page.get_by_role("group", name="Dátum doručenia odvolania *").get_by_placeholder("DD"),
            den, "Dátum doručenia odvolania - deň"
        )
        self._safe_fill(
            self.page.get_by_role("group", name="Dátum doručenia odvolania *").get_by_placeholder("MM"),
            mesiac, "Dátum doručenia odvolania - mesiac"
        )
        self._safe_fill(
            self.page.get_by_role("group", name="Dátum doručenia odvolania *").get_by_placeholder("YYYY"),
            rok, "Dátum doručenia odvolania - rok"
        )
        self._safe_fill(
            self.page.get_by_role("group", name="Dátum doručenia rozhodnutia *").get_by_placeholder("DD"),
            den, "Dátum doručenia rozhodnutia - deň"
        )
        self._safe_fill(
            self.page.get_by_role("group", name="Dátum doručenia rozhodnutia *").get_by_placeholder("MM"),
            mesiac, "Dátum doručenia rozhodnutia - mesiac"
        )
        self._safe_fill(
            self.page.get_by_role("group", name="Dátum doručenia rozhodnutia *").get_by_placeholder("YYYY"),
            rok, "Dátum doručenia rozhodnutia - rok"
        )
        self._safe_click(
            self.page.get_by_text("Podávateľ odvolania (nepovinné) Mária BartošováFero Bartoš warning warning"),
            "Podávateľ odvolania - rozbalit"
        )
        self._safe_select(
            self.page.get_by_label("Podávateľ odvolania"),
            PODAVATEL_ODVOLANIA_ID,
            "Podávateľ odvolania"
        )
        with self.page.expect_file_chooser() as fc_info:
            self._safe_click(
                self.page.get_by_role("button", name="Vybrať súbor"),
                "Vybrať súbor"
            )
            fc_info.value.set_files(SUBOR_PRILOHA)
        self._safe_fill(
            self.page.get_by_role("textbox", name="Odôvodnenie"),
            "Dôvod odvolania",
            "Odôvodnenie"
        )

    def submit_odvolanie(self):
        self._safe_click(
            self.page.get_by_role("button", name="Zaevidovať odvolanie"),
            "Zaevidovať odvolanie - potvrdiť"
        )

    def click_spatvzatie_odvolania(self):
        self._safe_click(
            self.page.get_by_role("link", name="Späťvzatie odvolania"),
            "Späťvzatie odvolania"
        )

    def confirm_spatvzatie(self):
        self._safe_click(
            self.page.locator("button").filter(has_text=re.compile(r"^Áno$")),
            "Potvrdiť späťvzatie"
        )
