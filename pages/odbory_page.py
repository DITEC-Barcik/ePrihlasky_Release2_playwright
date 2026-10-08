from playwright.sync_api import Page, expect
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
        # Modal je v kontajneri s aria-hidden="true", takže role lokátory ho nenájdu.
        self._safe_click(
            self.page.locator("button.btn-pridat-odbory:visible"),
            "Pridať odbor/y"
        )

    def _klikni_akciu_odboru(self, selector: str, nazov: str):
        # Zoznam sa po ulozeni prekresluje a otvorenu ponuku pritom zatvori,
        # preto sa otvorenie aj klik na polozku opakuju spolu.
        self.page.wait_for_load_state("networkidle")
        akcie = self.page.locator(".odbor-akcie-button").first
        polozka = self.page.locator(selector).first

        for _ in range(3):
            try:
                akcie.scroll_into_view_if_needed()
                akcie.click()
                expect(polozka).to_be_visible(timeout=5000)
                polozka.click(timeout=5000)
                return
            except Exception:
                continue

        self.screenshot(f"error_akcia_odboru_{self._sanitize_filename(nazov)}")
        raise AssertionError(f'Akciu "{nazov}" na odbore sa nepodarilo vykonať.')

    def aktualizuj_odbory_1_kolo(self):
        self._klikni_akciu_odboru(".btn-edit", "Upraviť")
        self._safe_fill(
            self.page.locator("#input-modalUpravitOdborKapacitaOdboruInput"),
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
            self.page.locator("#input-modalUpravitOdborIcoZamestnavatelaInput"),
            self.ICO_ZAMESTNAVATELA,
            "IČO zamestnávateľa"
        )
        # Tlacidlo sa spristupni az po opusteni pola s ICO.
        self.page.locator("#input-modalUpravitOdborIcoZamestnavatelaInput").press("Tab")
        self._safe_click(
            self.page.locator("#btn-pridat-ico"),
            "Pridať zamestnávateľa"
        )
        # Pocas dohladavania firmy prekryva modal spinner, ktory blokuje dalsie kliky.
        expect(
            self.page.locator("#zamestnavatelia-container"),
            "Zamestnávateľ sa po pridaní IČO nezobrazil."
        ).to_contain_text(self.ICO_ZAMESTNAVATELA, timeout=60000)
        self._safe_fill(
            self.page.locator("#input-modalUpravitOdborDualneVzdelavanieKapacitaInput"),
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
        self._klikni_akciu_odboru(".btn-delete", "Odstrániť")
        self._safe_click(
            self.page.locator("button").filter(has_text=re.compile(r"^Odstrániť$")),
            "Potvrdiť odstránenie"
        )