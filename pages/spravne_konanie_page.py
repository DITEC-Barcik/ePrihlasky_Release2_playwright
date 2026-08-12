import os
from playwright.sync_api import Page, expect
from pages.base_page import BasePage

SUBOR_PRILOHA = "./data/Dokument.pdf"


class SpravneKonanie(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def navigate_to_spravne_konanie(self):
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.get_by_role("link", name="Správne konanie"),
            "Správne konanie"
        )
        self.page.wait_for_load_state("networkidle")

    def search(self, meno: str):
        search_box = self.page.get_by_role("textbox", name="Vyhľadávanie v meno,")
        expect(search_box).to_be_visible()
        search_box.fill(meno)
        expect(search_box).to_have_value(meno)
        self._safe_click(
            self.page.get_by_role("button", name="Hľadať"),
            "Hľadať"
        )

    def click_spatvzatie_konania(self):
        self._safe_click(
            self.page.get_by_role("button", name="Späťvzatie konania"),
            "Späťvzatie konania"
        )

    def select_ucastnik(self, meno: str, meno_display: str):
        textbox = self.page.get_by_role("textbox")
        textbox.dblclick()
        textbox.fill(meno)
        self._safe_click(
            self.page.get_by_text(meno_display),
            meno_display
        )

    def upload_dokument(self, subor: str = SUBOR_PRILOHA):
        with self.page.expect_file_chooser() as fc_info:
            self._safe_click(
                self.page.get_by_role("link", name="Vybrať súbor"),
                "Vybrať súbor"
            )
            fc_info.value.set_files(subor)

    def click_pokracovat(self):
        self._safe_click(
            self.page.get_by_role("button", name="Pokračovať"),
            "Pokračovať"
        )

    def click_prejst_na_podpis(self):
        self._safe_click(
            self.page.get_by_role("button", name="Prejsť na podpis"),
            "Prejsť na podpis"
        )

    def click_vygenerovat(self):
        self._safe_click(
            self.page.get_by_role("button", name="Vygenerovať (1)"),
            "Vygenerovať (1)"
        )

    def click_spat_na_spravne_konanie(self):
        self._safe_click(
            self.page.get_by_role("button", name="Späť na správne konanie"),
            "Späť na správne konanie"
        )
        self.page.wait_for_load_state("networkidle")

    def cakaj_na_stav(self, meno: str, ocakavany_text: str, max_pokusov: int = 20):
        """Opakovane kliká na Hľadať každých 10s kým sa neobjaví očakávaný stav."""
        self.page.wait_for_timeout(2000)
        self.search(meno)
        for _ in range(max_pokusov):
            try:
                expect(self.page.locator("div.meno-wrapper:visible")).to_contain_text(
                    ocakavany_text, timeout=1000)
                return
            except AssertionError:
                self.page.wait_for_timeout(10000)
                self._safe_click(
                    self.page.get_by_role("button", name="Hľadať"),
                    "Hľadať"
                )
        expect(self.page.locator("div.meno-wrapper:visible")).to_contain_text(ocakavany_text)

    def click_vybrat_first(self):
        self._safe_click(
            self.page.locator(".govuk-button.govuk-button--sec.btn-vybrat.mb-0").first,
            "Vybrať"
        )

    def click_odoslat_rozhodnutie_zastavenia(self):
        self._safe_click(
            self.page.get_by_role("link", name="Odoslať rozhodnutie zastavenia konania"),
            "Odoslať rozhodnutie zastavenia konania"
        )

    def click_oznacit_ako_odoslane(self):
        self._safe_click(
            self.page.get_by_role("button", name="Označiť ako odoslané"),
            "Označiť ako odoslané"
        )
        self.page.wait_for_load_state("networkidle")
