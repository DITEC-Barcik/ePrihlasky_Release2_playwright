from playwright.sync_api import Page
from pages.base_page import BasePage


class LogoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def _click_on_menu(self):
        self._safe_click(
            self.page.locator(".profil-dropdown"),
            "Rozbaliť profilové menu"
        )

    def _click_on_logout(self):
        self._safe_click(
            self.page.get_by_role("link", name="Odhlásiť"),
            "Odhlásiť"
        )

    def logout(self):
        self._click_on_menu()
        self._click_on_logout()