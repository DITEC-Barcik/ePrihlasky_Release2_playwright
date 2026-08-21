from playwright.sync_api import Page
from pages.base_page import BasePage
import re


class Odbory(BasePage):
    ODBOR_2_KOLO_ID = "6565e543-a930-4141-ac45-4a96433cd5f4"
    KAPACITA_2_KOLO = "100"

    KAPACITA_1_KOLO = "55"
    DLZKA_STUDIA = "80"
    FORMA_STUDIA = "101"
    ICO_ZAMESTNAVATELA = "31385401"
    KAPACITA_DUAL = "12"

    def __init__(self, page: Page):
        super().__init__(page)

    def click_on_menu_odbory(self):
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.get_by_role("link", name="Odbory a kritériá"),
            "Odbory a kritériá"
        )

    def click_on_otvorit_odbor(self):
        self._safe_click(
            self.page.get_by_role("button", name="Otvoriť odbor pre 2. kolo"),
            "Otvoriť odbor pre 2. kolo"
        )

    def vyber_odbor_kapacitu(self):
        self._safe_select(
            self.page.get_by_label("Odbor pre 2. kolo"),
            self.ODBOR_2_KOLO_ID,
            "Odbor pre 2. kolo"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Kapacita odboru pre 2. kolo *"),
            self.KAPACITA_2_KOLO,
            "Kapacita odboru pre 2. kolo"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať"),
            "Pridať"
        )

    def click_on_zverejnit_odbor(self):
        self._safe_click(
            self.page.get_by_role("button", name="Zverejniť odbory pre 2. kolo"),
            "Zverejniť odbory pre 2. kolo"
        )

    def odstran_odbor(self):
        self._safe_click(
            self.page.get_by_role("button", name="Zrušiť"),
            "Zrušiť"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Odstrániť"),
            "Odstrániť"
        )

    def pridaj_odbor_1_kolo(self):
        self._safe_click(
            self.page.get_by_role("link", name="Odbory a kritériá"),
            "Odbory a kritériá"
        )
        self._safe_click(
            self.page.locator("#btnPridatOdbor"),
            "Pridať odbor"
        )
        self._safe_click(
            self.page.get_by_text("1113311"),
            "Odbor 1113311"
        )
        self._safe_click(
            self.page.locator(".checkmark").first,
            "Prvá voľba checkboxu"
        )
        self._safe_click(
            self.page.locator(".checkmark").first,
            "Prvá voľba checkboxu"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať odbor/y"),
            "Pridať odbor/y"
        )

    def aktualizuj_odbory_1_kolo(self):
        self._safe_click(
            self.page.get_by_role("button", name="Upraviť"),
            "Upraviť"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Kapacita odboru *"),
            self.KAPACITA_1_KOLO,
            "Kapacita odboru"
        )
        self._safe_click(
            self.page.locator("div:nth-child(6) > .checkmark").first,
            "Checkbox v 6. riadku"
        )
        self._safe_click(
            self.page.get_by_text("Žiaci 8. ročníka"),
            "Žiaci 8. ročníka"
        )
        self._safe_select(
            self.page.get_by_label("Dĺžka štúdia"),
            self.DLZKA_STUDIA,
            "Dĺžka štúdia"
        )
        self._safe_select(
            self.page.get_by_label("Forma štúdia"),
            self.FORMA_STUDIA,
            "Forma štúdia"
        )
        self._safe_click(
            self.page.locator("#modalUpravitOdborDualneVzdelavania > .checkmark"),
            "Duálne vzdelávanie"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="IČO zamestnávateľa"),
            self.ICO_ZAMESTNAVATELA,
            "IČO zamestnávateľa"
        )
        self._safe_click(
            self.page.get_by_role("link", name="Pridať"),
            "Pridať zamestnávateľa"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Kapacita pre duálne vzdelá"),
            self.KAPACITA_DUAL,
            "Kapacita pre duálne vzdelávanie"
        )
        self._safe_click(
            self.page.locator("#modalUpravitOdborPrijimaciaSkuska > .checkmark"),
            "Prijímacia skúška"
        )
        self._safe_click(
            self.page.locator("#modalUpravitOdborPrijimaciaSkuskaCheckboxList > .govuk-form-group.checkbox-list-control > .govuk-fieldset > .govuk-checkboxes > div > .checkmark").first,
            "Prvý predmet prijímacej skúšky"
        )
        self._safe_click(
            self.page.locator("#modalUpravitOdborPrijimaciaSkuskaCheckboxList > .govuk-form-group.checkbox-list-control > .govuk-fieldset > .govuk-checkboxes > div:nth-child(3) > .checkmark"),
            "Tretí predmet prijímacej skúšky"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Uložiť zmeny"),
            "Uložiť zmeny"
        )

    def odstran_odbor_1_kolo(self):
        self._safe_click(
            self.page.get_by_role("button", name="Odstrániť"),
            "Odstrániť"
        )
        self._safe_click(
            self.page.locator("button").filter(has_text=re.compile(r"^Odstrániť$")),
            "Potvrdiť odstránenie"
        )