from playwright.sync_api import Page
from pages.base_page import BasePage


class KofliktSS(BasePage):
    KOLO_2 = "2"
    ODBOR_2_KOLO = "2b3813df-fbe6-41ce-be28-0efc6dfaca83"
    # Nová konfigurácia portálu (šk. rok 2027/2028); pôvodne "fa97e1ee-cf77-4880-853a-5972261cdb4c".
    ODBOR_1_KOLO = "456570b0-6b5d-48ea-98a2-01751dca1a0a"

    def __init__(self, page: Page):
        super().__init__(page)

    def _zorad_prihlasky_podla_datumu(self):
        self._safe_click(
            self.page.get_by_role("button", name="Zoradiť podľa: Predvolené"),
            "Zoradiť podľa: Predvolené"
        )
        self._safe_check(
            self.page.get_by_role("radio", name="Podľa dátumu podania (od"),
            "Podľa dátumu podania"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Zoradiť prihlášky"),
            "Zoradiť prihlášky"
        )

    def _zobraz_prihlasku_v_konflikte(self):
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.get_by_role("button", name="Zobraziť").first,
            "Zobraziť prihlášku v konflikte"
        )
        self.page.wait_for_load_state("networkidle")

    def najdi_prihlasku_v_konflikte(self):
        self.page.wait_for_load_state("networkidle")

        self._safe_select(
            self.page.get_by_label("Kolo"),
            self.KOLO_2,
            "Kolo"
        )
        self._safe_select(
            self.page.get_by_label("Odbor"),
            self.ODBOR_2_KOLO,
            "Odbor - 2. kolo"
        )

        self._zorad_prihlasky_podla_datumu()
        self._zobraz_prihlasku_v_konflikte()

    def najdi_prihlasku_v_konflikte_1_kolo(self):
        self.page.wait_for_load_state("networkidle")

        self._safe_select(
            self.page.get_by_label("Odbor"),
            self.ODBOR_1_KOLO,
            "Odbor - 1. kolo"
        )

        self._zorad_prihlasky_podla_datumu()
        self._zobraz_prihlasku_v_konflikte()

    def click_on_vyzva_na_vyriesenie_konfliktu(self):
        self._safe_click(
            self.page.get_by_role("button", name="Vyzvať na riešenie konfliktu"),
            "Vyzvať na riešenie konfliktu"
        )

    def click_on_odoslat_vyzvu(self, text: str):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Sprievodná správa:"),
            text,
            "Sprievodná správa"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Odoslať výzvu"),
            "Odoslať výzvu"
        )

    def click_on_vyriesit_konflikt(self):
        self._safe_click(
            self.page.locator("#btn-vyriesit-konflikt"),
            "Vyriešiť konflikt"
        )

    def click_on_odoslat_konflikt(self, text: str):
        self._safe_fill(
            self.page.locator("#textarea-sprievodnaSpravaTextarea"),
            text,
            "Sprievodná správa k vyriešeniu konfliktu"
        )
        self.page.wait_for_timeout(3000)
        self._safe_click(
            self.page.locator("button.btn-vyriesit-konflikt.govuk-button.govuk-button__basic.last-focusable"),
            "Odoslať vyriešenie konfliktu"
        )