from playwright.sync_api import Page
from pages.base_page import BasePage


class PrilohyZS(BasePage):
    TYP_PRILOHY = "3"
    SUBOR = "./data/Dokument.pdf"

    def __init__(self, page: Page):
        super().__init__(page)

    def vyziadat_prilohu(self, dovod: str):
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
            dovod,
            "Dôvod vyžiadania prílohy"
        )

        self._safe_click(
            self.page.get_by_role("button", name="Odoslať"),
            "Odoslať žiadosť o prílohu"
        )

    def odvolat_ziadost(self):
        self.page.wait_for_timeout(5000)

        self._safe_click(
            self.page.get_by_role("button", name="Odvolať žiadosť"),
            "Odvolať žiadosť"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Áno, odvolať"),
            "Potvrdiť odvolanie žiadosti"
        )

    def pridat_prilohu(self):
        self._safe_click(
            self.page.get_by_role("link", name="Pridať prílohy").first,
            "Pridať prílohy"
        )

        self._safe_click(
            self.page.get_by_text("Čestné vyhlásenie zákonného zástupcu Nenahrané Nenahrané Nahrané"),
            "Vybrať typ prílohy - Čestné vyhlásenie zákonného zástupcu"
        )

        with self.page.expect_file_chooser() as fc_info:
            self._safe_click(
                self.page.get_by_role("link", name="Vybrať súbor"),
                "Vybrať súbor"
            )

        file_chooser = fc_info.value
        file_chooser.set_files(self.SUBOR)

        self._safe_click(
            self.page.get_by_role("button", name="Odoslať"),
            "Odoslať prílohu"
        )

    def click_on_prejst_na_prihlasky(self):
        self._safe_click(
            self.page.get_by_role("link", name="Prejsť na prihlášky"),
            "Prejsť na prihlášky"
        )