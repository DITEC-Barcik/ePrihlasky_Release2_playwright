from playwright.sync_api import Page
from pages.base_page import BasePage


class PrilohySS(BasePage):
    ODBOR_2_KOLO = "2b3813df-fbe6-41ce-be28-0efc6dfaca83"
    # Nová konfigurácia portálu (šk. rok 2027/2028); pôvodne "fa97e1ee-cf77-4880-853a-5972261cdb4c" (2026/2027).
    ODBOR_1_KOLO = "456570b0-6b5d-48ea-98a2-01751dca1a0a"
    TYP_PRILOHY = "3"
    SUBOR = "./data/Dokument.pdf"

    def __init__(self, page: Page):
        super().__init__(page)

    def _zorad_a_otvor_poslednu_prihlasku(self, nazov_akcie: str):
        self._safe_click(
            self.page.get_by_role("button", name="Zoradiť podľa: Predvolené"),
            "Zoradiť podľa: Predvolené"
        )
        # Modal je vnorený v #riaditel-home-page, ktorý má pri otvorení aria-hidden="true",
        # takže obsah modalu nie je v accessibility strome a role/name lokátory ho nenájdu.
        self._safe_check(
            self.page.locator("#modalZoraditPrihlaskyRadio_option_1"),
            "Podľa dátumu podania"
        )
        self._safe_click(
            self.page.locator("button.btn-zoradit:visible"),
            "Zoradiť prihlášky"
        )

        self.page.wait_for_load_state("networkidle")

        self._safe_click(
            self.page.get_by_role("button", name="Zobraziť").first,
            nazov_akcie
        )
        self.page.wait_for_load_state("networkidle")

    def _vyhladaj_a_otvor_prihlasku(self, meno: str, priezvisko: str, nazov_akcie: str):
        self.page.wait_for_timeout(3000)

        self._safe_fill(
            self.page.locator("#fulltext-input"),
            f"{meno} {priezvisko}",
            "Vyhľadávanie prihlášky"
        )
        self._safe_click(
            self.page.locator("div.input-with-button").locator("button").nth(1),
            "Hľadať prihlášku"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Zobraziť").first,
            nazov_akcie
        )

        self.page.wait_for_load_state("networkidle")

    def najdi_poslednu_prihlasku(self):
        self.page.wait_for_load_state("networkidle")

        self._safe_select(
            self.page.get_by_label("Kolo"),
            "2",
            "Kolo"
        )
        self._safe_select(
            self.page.get_by_label("Odbor"),
            self.ODBOR_2_KOLO,
            "Odbor"
        )

        self._zorad_a_otvor_poslednu_prihlasku("Zobraziť poslednú prihlášku")

    def najdi_poslednu_prihlasku_1_kolo(self):
        self.page.wait_for_load_state("networkidle")

        self._safe_select(
            self.page.get_by_label("Odbor"),
            self.ODBOR_1_KOLO,
            "Odbor pre 1. kolo"
        )

        self._zorad_a_otvor_poslednu_prihlasku("Zobraziť poslednú prihlášku pre 1. kolo")

    def vyziadaj_prilohu_na_poslednej_prihlaske(self):
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
            "Žiadosť o doplnenie prílohy.",
            "Dôvod vyžiadania prílohy"
        )

        self._safe_click(
            self.page.get_by_role("button", name="Odoslať"),
            "Odoslať žiadosť o doplnenie prílohy"
        )

    def odvolanie_ziadosti(self):
        self.page.wait_for_timeout(5000)

        self._safe_click(
            self.page.get_by_role("button", name="Odvolať žiadosť"),
            "Odvolať žiadosť"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Áno, odvolať"),
            "Potvrdiť odvolanie žiadosti"
        )

    def nahrat_prilohu(self):
        self.page.wait_for_load_state("networkidle")

        self._safe_click(
            self.page.get_by_role("link", name="Pridať prílohy").first,
            "Pridať prílohy"
        )
        self._safe_click(
            self.page.get_by_text("Čestné vyhlásenie zákonného zástupcu Nenahrané Nenahrané Nahrané"),
            "Vybrať prílohu - Čestné vyhlásenie zákonného zástupcu"
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

    def najdi_prihlasku_po_nahrati_prilohy(self, meno: str, priezvisko: str):
        self.page.wait_for_load_state("networkidle")

        self._safe_select(
            self.page.get_by_label("Kolo"),
            "2",
            "Kolo"
        )
        self._safe_select(
            self.page.get_by_label("Odbor"),
            self.ODBOR_2_KOLO,
            "Odbor"
        )

        self._vyhladaj_a_otvor_prihlasku(
            meno,
            priezvisko,
            "Zobraziť prihlášku po nahratí prílohy"
        )

    def najdi_prihlasku_po_nahrati_prilohy_1_kolo(self, meno: str, priezvisko: str):
        self.page.wait_for_load_state("networkidle")

        self._safe_select(
            self.page.get_by_label("Odbor"),
            self.ODBOR_1_KOLO,
            "Odbor pre 1. kolo"
        )

        self._vyhladaj_a_otvor_prihlasku(
            meno,
            priezvisko,
            "Zobraziť prihlášku po nahratí prílohy pre 1. kolo"
        )