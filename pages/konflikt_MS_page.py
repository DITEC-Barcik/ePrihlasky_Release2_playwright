from playwright.sync_api import Page
from pages.base_page import BasePage


class KonfliktMS(BasePage):
    DEFAULT_VYZVA_TEXT = "Výzva na vyriešenie konfliktu."

    def __init__(self, page: Page):
        super().__init__(page)

    def click_on_vyzva_na_vyriesenie_konfliktu(self):
        self._safe_click(
            self.page.get_by_role("button", name="Vyzvať na riešenie konfliktu"),
            "Vyzvať na riešenie konfliktu"
        )

    def odoslat_vyzvu_na_vyriesenie_konfliktu(self):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Sprievodná správa:"),
            self.DEFAULT_VYZVA_TEXT,
            "Sprievodná správa k výzve"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Odoslať výzvu"),
            "Odoslať výzvu"
        )

    def click_on_vyriesenie_konfliktu(self):
        self._safe_click(
            self.page.get_by_role("button", name="Vyriešiť konflikt"),
            "Vyriešiť konflikt"
        )

    def odoslat_vyriesenie_konfliktu(self, text: str):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Sprievodná správa:"),
            text,
            "Sprievodná správa k vyriešeniu konfliktu"
        )
        self._safe_click(
            self.page.locator("button.btn-vyriesit-konflikt.govuk-button.govuk-button__basic.last-focusable"),
            "Odoslať vyriešenie konfliktu"
        )