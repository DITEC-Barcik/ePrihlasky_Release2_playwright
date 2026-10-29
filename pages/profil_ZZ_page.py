from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ProfilZZ(BasePage):
    KRAJINA = "slovenská rep"
    KRAJINA_LABEL = "Slovenská republika"

    def __init__(self, page: Page):
        super().__init__(page)

    def _otvorit_profilove_menu(self):
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.locator(".profil-dropdown"),
            "Rozbaliť profilové menu"
        )
        self._safe_click(
            self.page.get_by_role("link", name="Môj profil"),
            "Môj profil"
        )
        self.page.wait_for_load_state("networkidle")

    def _otvorit_upravu_udajov(self):
        self._safe_click(
            self.page.get_by_role("link", name="Upraviť údaje"),
            "Upraviť údaje"
        )
        # Page loads data asynchronously and re-disables the save button when done
        expect(self.page.locator("#input-telefon")).not_to_have_value("", timeout=60000)
        expect(self.page.locator("button.btn-ulozit:visible")).to_be_disabled(timeout=60000)

    def otvorit_profil(self):
        self._otvorit_profilove_menu()

    def zmen_tel_cislo(self, cislo: str):
        self._otvorit_upravu_udajov()
        self._safe_fill(
            self.page.locator("#input-telefon"),
            cislo,
            "Telefónne číslo"
        )
        self.page.locator("#input-telefon").press("Tab")

    def click_on_ulozit_zmeny(self):
        self._safe_click(
            self.page.locator("button.btn-ulozit:visible"),
            "Uložiť zmeny"
        )

    def zmenit_mail(self, mail: str):
        self._safe_click(
            self.page.get_by_role("button", name="Zmeniť e-mail"),
            "Zmeniť e-mail"
        )
        self._safe_fill(
            self.page.locator("#input-zmenitEmail"),
            mail,
            "Vaša nová emailová adresa"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Zmeniť email"),
            "Zmeniť email"
        )

    def overit_kod_mailu(self, kod: str):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Overovací kód"),
            kod,
            "Overovací kód"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Overiť"),
            "Overiť"
        )

    def zmenit_adresu(self, adresa: str, adresa_label: str):
        # Page reloads after e-mail verification; wait until its async init finishes
        self.page.wait_for_load_state("networkidle")
        expect(self.page.locator("#input-telefon")).not_to_have_value("", timeout=60000)
        expect(self.page.locator("button.btn-ulozit:visible")).to_be_disabled(timeout=60000)
        pridat_adresu = self.page.locator(".pridat-adresu-dalej")
        ina_adresa = self.page.locator("label[for='trvalyPobytRadio_option_1']")
        expect(pridat_adresu.or_(ina_adresa).filter(visible=True).first).to_be_visible(timeout=60000)
        if pridat_adresu.is_visible():
            self._safe_click(pridat_adresu, "Pridať adresu")
        else:
            self._safe_click(ina_adresa, "Iná korešpondenčná adresa")

        self._safe_fill(
            self.page.locator("#adresaTPKrajina input.autocomplete-input"),
            self.KRAJINA,
            "Krajina"
        )
        self._safe_click(
            self.page.locator("#adresaTPKrajina").get_by_text(self.KRAJINA_LABEL, exact=True),
            self.KRAJINA_LABEL
        )
        self._safe_fill(
            self.page.locator("#adresaTPAdresaRA input.autocomplete-input"),
            adresa,
            "Adresa"
        )
        self._safe_click(
            self.page.locator("#adresaTPAdresaRA").get_by_text(adresa_label, exact=True),
            adresa_label
        )
        self._safe_click(
            self.page.locator("#ulozit-adresu"),
            "Uložiť adresu"
        )