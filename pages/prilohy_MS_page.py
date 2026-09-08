from playwright.sync_api import Page
from pages.base_page import BasePage


class PrilohyMS(BasePage):
    TYP_PRILOHY = "1"
    DOVOD = "Odvolanie prílohy."
    SUBOR_PRILOHA = "./data/Dokument.pdf"

    def __init__(self, page: Page):
        super().__init__(page)

    def vyziadanie_prilohy_MS(self):
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000)

        self._safe_click(
            self.page.get_by_role("button", name="Vyžiadať prílohu"),
            "Vyžiadať prílohu"
        )
        self._safe_select(
            self.page.get_by_label("Typ prílohy"),
            self.TYP_PRILOHY,
            "Typ prílohy"
        )
        self._safe_fill(
            self.page.locator("#textarea-dovodText"),
            self.DOVOD,
            "Dôvod"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Odoslať"),
            "Odoslať žiadosť o prílohu"
        )

    def odvolanie_prilohy_MS(self):
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(4000)

        self._safe_click(
            self.page.get_by_role("button", name="Odvolať žiadosť"),
            "Odvolať žiadosť"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Áno, odvolať"),
            "Áno, odvolať"
        )

    def pridat_prilohu_MS(self):
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000)

        self._safe_click(
            self.page.get_by_role("link", name="Pridať prílohy").first,
            "Pridať prílohy"
        )
        self._safe_click(
            self.page.locator("span").filter(has_text="add").first,
            "Pridať novú prílohu"
        )

        with self.page.expect_file_chooser() as fc_info:
            self._safe_click(
                self.page.get_by_role("link", name="Vybrať súbor"),
                "Vybrať súbor"
            )

        file_chooser = fc_info.value
        file_chooser.set_files(self.SUBOR_PRILOHA)

        self._safe_click(
            self.page.get_by_role("button", name="Odoslať"),
            "Odoslať prílohu"
        )