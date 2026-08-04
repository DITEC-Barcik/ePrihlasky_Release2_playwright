from playwright.sync_api import Page
from pages.base_page import BasePage


class ProfilZZ(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def _otvorit_profilove_menu(self):
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

    def _otvorit_upravu_udajov(self):
        self._safe_click(
            self.page.get_by_role("link", name="Upraviť údaje"),
            "Upraviť údaje"
        )

    def otvorit_profil(self):
        self._otvorit_profilove_menu()

    def zmen_tel_cislo(self, cislo: str):
        self._otvorit_upravu_udajov()
        self._safe_fill(
            self.page.get_by_role("textbox", name="Telefónne číslo *"),
            cislo,
            "Telefónne číslo"
        )

    def click_on_ulozit_zmeny(self):
        self._safe_click(
            self.page.locator("button").filter(has_text="Uložiť zmeny").first,
            "Uložiť zmeny"
        )

    def zmenit_mail(self, mail: str):
        self._safe_click(
            self.page.get_by_role("button", name="Zmeniť e-mail"),
            "Zmeniť e-mail"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Vaša nová emailová adresa *"),
            mail,
            "Vaša nová emailová adresa"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Zmeniť email"),
            "Zmeniť email"
        )

    def overit_kod_mailu(self, kod: str):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Overovací kód *"),
            kod,
            "Overovací kód"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Overiť"),
            "Overiť"
        )

    def zmenit_adresu(
        self,
        krajina: str,
        mesto: str,
        ulica: str,
        scislo: str,
        ocislo: str,
        psc: str
    ):
        self._safe_check(
            self.page.get_by_role("radio", name="Iná korešpondenčná adresa"),
            "Iná korešpondenčná adresa"
        )

        self._safe_fill(
            self.page.locator("#adresaTPKrajina").get_by_role("textbox"),
            krajina,
            "Krajina"
        )
        self._safe_click(
            self.page.get_by_text("Slovenská republika", exact=True),
            "Slovenská republika"
        )

        self._safe_fill(
            self.page.locator("#adresaTPObec").get_by_role("textbox"),
            mesto,
            "Obec"
        )
        if mesto == "semero":
            self._safe_click(
                self.page.get_by_text("Semerovo (Nové Zámky)"),
                "Semerovo (Nové Zámky)"
            )
        else:
            self._safe_click(
                self.page.get_by_text("Trebatice (Piešťany)"),
                "Trebatice (Piešťany)"
            )

        self._safe_fill(
            self.page.get_by_role("textbox", name="Krajina *"),
            ulica,
            "Ulica"
        )
        if ulica == "kuri":
            self._safe_click(
                self.page.get_by_text("Kúria"),
                "Kúria"
            )
        else:
            self._safe_click(
                self.page.get_by_text("Záštepy", exact=True),
                "Záštepy"
            )

        if scislo == "32":
            self._safe_fill(
                self.page.get_by_role("textbox", name="Súpisné číslo"),
                scislo,
                "Súpisné číslo"
            )

        self._safe_fill(
            self.page.get_by_role("textbox", name="Orientačné číslo *"),
            ocislo,
            "Orientačné číslo"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="PSČ *"),
            psc,
            "PSČ"
        )
        self._safe_click(
            self.page.locator("#ulozit-adresu"),
            "Uložiť adresu"
        )