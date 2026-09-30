from playwright.sync_api import Page
from pages.base_page import BasePage


class Prijimacky(BasePage):
    KOLO_2 = "2"
    ODBOR_2_KOLO = "2b3813df-fbe6-41ce-be28-0efc6dfaca83"
    # Nová konfigurácia portálu (šk. rok 2027/2028); pôvodne "fa97e1ee-cf77-4880-853a-5972261cdb4c" (2026/2027).
    ODBOR_1_KOLO = "456570b0-6b5d-48ea-98a2-01751dca1a0a"

    TERMIN_DEN = "12"
    TERMIN_MESIAC = "10"
    TERMIN_ROK = "2026"
    TERMIN_HOD = "11"
    TERMIN_MIN = "30"
    MIESTNOST = "3.E"

    VOLITELNY_TEXT_POZVANKA = "Dostavte sa na čas a prineste si kružítko."
    SUBOR_PRILOHA = "./data/Dokument.pdf"

    POZVANKA_DOWNLOAD_PATH = "data/downloads/pozvankaDownloaded.pdf"
    BODY_DOWNLOAD_PATH = "data/downloads/bodyDownloaded.pdf"

    def __init__(self, page: Page):
        super().__init__(page)

    def _open_vybrat_menu(self):
        self._safe_click(
            self.page.get_by_role("button", name="Vybrať").first,
            "Vybrať"
        )

    def _open_akcie_menu(self):
        # Vlastný checkbox - reálny input je skrytý, kliká sa na span.checkmark.
        self._safe_click(
            self.page.locator("div.vybrate-wrapper:visible .checkmark").first,
            "Výber akcie"
        )
        self._safe_click(
            self.page.locator("#vykonat-akciu-btn"),
            "Vykonať akciu"
        )

    def click_on_menu_prijimacky(self):
        self.page.wait_for_load_state("networkidle")
        self._safe_click(
            self.page.get_by_role("link", name="Prijímačky"),
            "Prijímačky"
        )

    def click_on_menu_sprava_prihlasok(self):
        self._safe_click(
            self.page.get_by_role("link", name="Správa prihlášok"),
            "Správa prihlášok"
        )

    def zmen_kolo_a_odbor(self):
        self._safe_select(
            self.page.get_by_label("Kolo"),
            self.KOLO_2,
            "Kolo"
        )
        self._safe_select(
            self.page.get_by_label("Odbor"),
            self.ODBOR_2_KOLO,
            "Odbor"
        )

    def zmen_odbor_1_kolo(self):
        self._safe_select(
            self.page.get_by_label("Odbor"),
            self.ODBOR_1_KOLO,
            "Odbor pre 1. kolo"
        )

    def zorad_prihlasky(self):
        self._safe_click(
            self.page.get_by_role("button", name="Zoradiť podľa: Predvolené"),
            "Zoradiť podľa: Predvolené"
        )
        # Modal je vnorený v kontajneri s aria-hidden="true", takže role lokátory ho nenájdu.
        self._safe_check(
            self.page.locator("#modalZoraditPrijimackyRadio_option_1"),
            "Podľa dátumu podania"
        )
        self._safe_click(
            self.page.locator("button.btn-zoradit:visible"),
            "Zoradiť prihlášky"
        )

    def click_on_uprava_prihlasky(self):
        self._open_vybrat_menu()
        self._safe_click(
            self.page.get_by_role("link", name="Upraviť"),
            "Upraviť"
        )

    def zobraz_prihlasku_detail(self):
        self._safe_click(
            self.page.get_by_role("button", name="Zobraziť").first,
            "Zobraziť detail prihlášky"
        )

    def get_udaje_dietata(self) -> tuple[str, str, str, str]:
        self.page.wait_for_load_state("networkidle")
        pristupovy_kod = self.page.locator("div.pristupovyKod").text_content()
        meno = self.page.locator("#dietaMeno").text_content()
        priezvisko = self.page.locator("#dietaPriezvisko").text_content()
        datum_narodenia = self.page.locator("#dietaDatumNarodenia").text_content()
        return pristupovy_kod, meno, priezvisko, datum_narodenia

    def nastavenie_terminu_prijimaciek(self):
        self._safe_fill(
            self.page.get_by_role("textbox", name="Deň"),
            self.TERMIN_DEN,
            "Deň"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Mesiac"),
            self.TERMIN_MESIAC,
            "Mesiac"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Rok"),
            self.TERMIN_ROK,
            "Rok"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Hod."),
            self.TERMIN_HOD,
            "Hodina"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Min."),
            self.TERMIN_MIN,
            "Minúta"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Miestnosť"),
            self.MIESTNOST,
            "Miestnosť"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Uložiť"),
            "Uložiť termín prijímačiek"
        )

    def click_on_akcia_odoslat_pozvanky(self):
        self._open_akcie_menu()
        self._safe_click(
            self.page.locator("a").filter(has_text="Odoslať pozvánky").last,
            "Odoslať pozvánky"
        )

    def odoslat_pozvanky(self):
        self._safe_click(
            self.page.get_by_role("button", name="Pokračovať"),
            "Pokračovať - pozvánky 1"
        )
        self._safe_fill(
            self.page.get_by_role("textbox", name="Voliteľný text"),
            self.VOLITELNY_TEXT_POZVANKA,
            "Voliteľný text"
        )

        with self.page.expect_file_chooser() as fc_info:
            self._safe_click(
                self.page.get_by_role("button", name="Vybrať súbor"),
                "Vybrať súbor pre pozvánky"
            )

        file_chooser = fc_info.value
        file_chooser.set_files(self.SUBOR_PRILOHA)

        self._safe_click(
            self.page.get_by_role("button", name="Odoslať"),
            "Odoslať pozvánky"
        )

    def click_on_spat_na_prijimacky(self):
        self._safe_click(
            self.page.get_by_role("link", name="Späť na prijímačky"),
            "Späť na prijímačky"
        )

    def click_on_akcia_plny_pocet_bodov(self):
        self._open_akcie_menu()
        self._safe_click(
            self.page.locator("a").filter(has_text="Odoslať správu o plnom počte bodov").last,
            "Odoslať správu o plnom počte bodov"
        )

    def odoslat_plny_pocet_bodov(self):
        self._safe_click(
            self.page.get_by_role("button", name="Pokračovať"),
            "Pokračovať - plný počet bodov 1"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pokračovať"),
            "Pokračovať - plný počet bodov 2"
        )

    def stiahni_pozvanku(self):
        self._open_vybrat_menu()
        with self.page.expect_download() as download_info:
            self._safe_click(
                self.page.locator("a").filter(has_text="Stiahnuť PDF - Pozvánka").last,
                "Stiahnuť PDF - Pozvánka"
            )
        download = download_info.value
        download.save_as(self.POZVANKA_DOWNLOAD_PATH)

    def stiahni_body(self):
        self._open_vybrat_menu()
        with self.page.expect_download() as download_info:
            self._safe_click(
                self.page.locator("a").filter(has_text="Stiahnuť PDF - Správa o bodoch").last,
                "Stiahnuť PDF - Správa o bodoch"
            )
        download = download_info.value
        download.save_as(self.BODY_DOWNLOAD_PATH)