from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class VyveskaMS(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def navigate_to_vyveska(self):
        self._safe_click(
            self.page.get_by_role("link", name="Elektronická výveska"),
            "Elektronická výveska"
        )
        self.page.wait_for_load_state("networkidle")

    def verify_page_header(self):
        expect(self.page.locator("h1")).to_contain_text("Elektronická výveska")

    def verify_page_text_logged_in(self):
        expect(self.page.locator("#elektronicka-vyveska")).to_contain_text(
            "Na tejto stránke si môžete jednoducho a rýchlo overiť výsledky prijímacieho konania na materské, základné a stredné školy. Zadajte kód uchádzača, ktorý Vám pridelila škola, a zobrazia sa Vám najaktuálnejšie informácie o prijatí, neprijatí alebo o výsledkoch prijímacích skúšok."
        )
        expect(self.page.locator("#elektronicka-vyveska")).to_contain_text("Aktuálne výsledky pre Vaše prihlášky")
        expect(self.page.locator("#elektronicka-vyveska")).to_contain_text(
            "Nižšie nájdete prehľad výsledkov prijímacieho konania na všetkých školách, na ktoré ste v tomto školskom roku podali prihlášku. Pri každej škole je uvedený aktuálny stav Vašej prihlášky alebo informácia o tom, že škola zatiaľ výsledky nezverejnila. V prípade stredných škôl sú uvedené aj výsledky prijímacích skúšok, ak sú súčasťou konania. Zobrazované údaje vychádzajú z informácií poskytnutých jednotlivými školami."
        )

    def verify_page_text_logged_out(self):
        expect(self.page.locator("#elektronicka-vyveska")).to_contain_text(
            "Na tejto stránke si môžete jednoducho a rýchlo overiť výsledky prijímacieho konania na materské, základné a stredné školy. Zadajte kód uchádzača, ktorý Vám pridelila škola, a zobrazia sa Vám najaktuálnejšie informácie o prijatí, neprijatí alebo o výsledkoch prijímacích skúšok."
        )

    def fill_pristupovy_kod(self, kod: str):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Prístupový kód*"),
            kod,
            "Prístupový kód"
        )

    def click_zobrazit_vysledky(self):
        self._safe_click(
            self.page.get_by_role("button", name="Zobraziť výsledky"),
            "Zobraziť výsledky"
        )

    def verify_kod_already_shown(self, kod: str):
        expect(self.page.get_by_role("paragraph")).to_contain_text(
            f"Výsledky pre \"{kod}\" sú už zobrazené v sekcii \"Aktuálne výsledky pre Vaše prihlášky\"."
        )

    def verify_vysledky_vyhladavania(self, kod: str):
        expect(self.page.locator("#elektronicka-vyveska")).to_contain_text("Výsledky vyhľadávania na základe")
        expect(self.page.locator("#elektronicka-vyveska")).to_contain_text(f'"{kod}"')

    def click_expand_result(self, kod: str = None):
        if kod:
            self._safe_click(
                self.page.locator(".profile-wrapper", has_text=kod).locator(".material-icons.add"),
                f"Rozbaliť výsledok - {kod}"
            )
        else:
            self._safe_click(
                self.page.get_by_text("add"),
                "Rozbaliť výsledok"
            )

    def verify_prijaty_in_table(self):
        expect(self.page.get_by_role("table")).to_contain_text("Prijatý")

    def verify_neprijaty_in_table(self):
        expect(self.page.get_by_role("table")).to_contain_text("Neprijatý")
