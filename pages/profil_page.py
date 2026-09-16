from playwright.sync_api import Page
from pages.base_page import BasePage


class ProfilPage(BasePage):
    KONTAKTNY_EMAIL = "mail@tst.net"

    def __init__(self, page: Page):
        super().__init__(page)

    def _open_profil(self):
        self.page.wait_for_load_state("networkidle")

        self._safe_click(
            self.page.get_by_role("link", name="Rozbaliť profilové menu"),
            "Rozbaliť profilové menu"
        )
        self._safe_click(
            self.page.get_by_role("link", name="Môj profil"),
            "Môj profil"
        )

        self.page.wait_for_load_state("networkidle")

    def _change_phone_number(self, cislo: str):
        self._safe_fill(
            self.page.locator("#input-telefon"),
            cislo,
            "Telefónne číslo"
        )
        # Nové povinné pole portálu; kým je prázdne, tlačidlo Uložiť zmeny zostáva disabled.
        self._safe_fill(
            self.page.locator("#input-kontaktnyEmail"),
            self.KONTAKTNY_EMAIL,
            "Kontaktná e-mailová adresa"
        )
        # Formulár sa prevaliduje až po opustení poľa.
        self.page.locator("#input-kontaktnyEmail").press("Tab")
        self._safe_click(
            self.page.get_by_role("button", name="Uložiť zmeny"),
            "Uložiť zmeny"
        )

    def click_on_profil(self):
        self._open_profil()

    def click_on_upravit_udaje(self):
        self._safe_click(
            self.page.get_by_role("link", name="Upraviť údaje"),
            "Upraviť údaje"
        )
        # Bez počkania sa polia vyplnia skôr, než sa naviaže validácia, a tlačidlo zostane disabled.
        self.page.wait_for_load_state("networkidle")

    def change_tel_cislo(self, cislo: str):
        self._change_phone_number(cislo)

    def change_email(self, mail: str):
        self._safe_fill(
            self.page.locator("#input-zmenitEmail"),
            mail,
            "Vaša nová emailová adresa"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Zmeniť email"),
            "Zmeniť email"
        )

    def load_kod(self, kod: str):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Overovací kód"),
            kod,
            "Overovací kód"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Overiť"),
            "Overiť"
        )

        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(5000)

    def change_school(self, school_name: str):
        self._safe_click(
            self.page.get_by_role("textbox", name="Škola"),
            "Škola"
        )
        self._safe_click(
            self.page.get_by_text(school_name, exact=True),
            f"Škola - {school_name}"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Zmeniť školu"),
            "Zmeniť školu"
        )

    def get_email_riaditela(self) -> str:
        try:
            locator = self.page.locator("#profil-riaditel-mail")
            self._expect_visible(
                locator,
                "E-mail riaditeľa nie je v profile viditeľný."
            )
            return (locator.text_content() or "").strip()
        except Exception as e:
            self.screenshot("error_get_email_riaditela")
            raise AssertionError(f'Nepodarilo sa načítať e-mail riaditeľa z profilu: {e}')