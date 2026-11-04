from playwright.sync_api import Page
from pages.base_page import BasePage

class SpravaPouzivatelov(BasePage):
    ROLA_ADMIN = "2"

    def __init__(self, page: Page):
        super().__init__(page)

    def otvor_spravu_pouzivatelov(self):
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.get_by_role("link", name="Správa školy"),
            "Správa školy"
        )
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.get_by_role("link", name="Správa používateľov"),
            "Správa používateľov"
        )

    def click_on_pridat_pouzivatela(self):
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.get_by_role("button", name="Pridať používateľa"),
            "Pridať používateľa"
        )

    def pridaj_rolu(self, eduid: str, rola: str):
        self._safe_click(
            self.page.locator("input.govuk-input.autocomplete-input"),
            "Výber školy podľa EDUID"
        )
        self._safe_click(
            self.page.locator(f'div.autocomplete-item[data-value="{eduid}"]'),
            f"EDUID {eduid}"
        )

        if rola == "admin":
            self._safe_select(
                self.page.get_by_label("Vyberte rolu"),
                self.ROLA_ADMIN,
                "Rola admin"
            )

        self._safe_click(
            self.page.get_by_role("button", name="Pridať"),
            "Pridať rolu"
        )

    def otvor_profil(self):
        self.page.wait_for_load_state("networkidle")
        # Mandatory contact details modal for users without saved phone/e-mail
        kontakt_modal = self.page.locator("#kontrola-kontaktnych-udajov-modal")
        if kontakt_modal.is_visible():
            self._safe_fill(kontakt_modal.locator("#input-kontrolaTelefon"), "+421999888777", "Telefónne číslo")
            self._safe_fill(kontakt_modal.locator("#input-kontrolaEmail"), "katalontest987@gmail.com", "Kontaktná e-mailová adresa")
            self._safe_click(
                kontakt_modal.get_by_role("button", name="Uložiť"),
                "Uložiť kontaktné údaje"
            )
            kontakt_modal.wait_for(state="hidden")
        self._safe_click(
            self.page.locator(".profil-dropdown"),
            "Rozbaliť profilové menu"
        )
        self._safe_click(
            self.page.get_by_role("link", name="Môj profil"),
            "Môj profil"
        )

    def click_on_odstranit(self, eduid: str):
        self._safe_click(
            self.page.locator(".pouzivatel-item")
            .filter(has_text=f"EDUID: {eduid}")
            .locator("button[data-pouzivatel-odstranit]"),
            f"Odstrániť {eduid}"
        )

    def click_on_potvrdit_odstranenie(self):
        self._safe_click(
            self.page.get_by_role("button", name="Potvrdiť").last,
            "Potvrdiť odstránenie"
        )