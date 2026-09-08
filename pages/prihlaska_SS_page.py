from playwright.sync_api import Page
from pages.base_page import BasePage


class PrihlaskaSS(BasePage):
    ODBOR_2_KOLO = "2b3813df-fbe6-41ce-be28-0efc6dfaca83"
    # Nová konfigurácia portálu (šk. rok 2027/2028); pôvodne "fa97e1ee-cf77-4880-853a-5972261cdb4c" (2026/2027).
    ODBOR_1_KOLO = "456570b0-6b5d-48ea-98a2-01751dca1a0a"
    TERMIN_PRIJIMACEJ_SKUSKY = "11"
    SUBOR_PRILOHA = "./data/Dokument.pdf"
    ADRESA = "Prvej SNR 33/23"
    ADRESA_LABEL = "Prvej SNR 33/23, 90701, Myjava, Myjava"

    def __init__(self, page: Page):
        super().__init__(page)

    def _click_dalej(self, nazov_kroku: str):
        self._safe_click(
            self.page.locator("button.btn-dalej:visible").last,
            nazov_kroku
        )

    def _upload_prilohy(self, index: int, nazov_prvku: str):
        self._safe_click(
            self.page.locator(".priloha-header").nth(index - 1),
            nazov_prvku
        )
        with self.page.expect_file_chooser() as fc_info:
            self._safe_click(
                self.page.locator(f"#prilohyUploadZone{index} a.govuk-button__large"),
                f"Vybrať súbor - {nazov_prvku}"
            )
        file_chooser = fc_info.value
        file_chooser.set_files(self.SUBOR_PRILOHA)

    def _vyhladaj_prihlasku(self, meno: str, priezvisko: str, nazov_vyhladavania: str):
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000)

        self._safe_fill(
            self.page.locator("#fulltext-input"),
            f"{meno} {priezvisko}",
            nazov_vyhladavania
        )
        self._safe_click(
            self.page.locator("button.govuk-button.govuk-button__basic.button-search:visible"),
            f"Hľadať - {nazov_vyhladavania}"
        )

    def click_on_vytvorit_prihlasku(self):
        self.page.wait_for_load_state("networkidle")

        self._safe_click(
            self.page.locator("#btn-vytvorit-prihlasku:visible"),
            "Vytvoriť prihlášku"
        )
        self._safe_check(
            self.page.locator("#modalVytvoritPrihlaskuRadio_option_3"),
            "Typ prihlášky - ďalšie kolo"
        )
        self._safe_click(
            self.page.locator("button.btn-pridat.govuk-button:visible"),
            "Pridať prihlášku"
        )

    def click_on_vytvorit_prihlasku_1_kolo(self):
        self.page.wait_for_load_state("networkidle")

        self._safe_click(
            self.page.locator("#btn-vytvorit-prihlasku:visible"),
            "Vytvoriť prihlášku"
        )
        self._safe_check(
            self.page.locator("#modalVytvoritPrihlaskuRadio_option_2"),
            "Typ prihlášky - 1. kolo"
        )
        self._safe_click(
            self.page.locator("button.btn-pridat.govuk-button:visible"),
            "Pridať prihlášku"
        )

    def pridat_dieta(self, meno: str, priezvisko: str, rc: str):
        self._safe_check(
            self.page.get_by_role("radio", name="Iný žiak Pridajte dieťa alebo"),
            "Iný žiak"
        )
        self._safe_click(
            self.page.get_by_role("button", name="Pridať žiaka"),
            "Pridať žiaka"
        )
        self._safe_check(
            self.page.locator("#maDietaRCRadio_option_0"),
            "Žiak má rodné číslo"
        )

        self._safe_fill(
            self.page.locator("#input-rodneCislo"),
            rc,
            "Rodné číslo"
        )
        self._safe_fill(
            self.page.locator("#input-krstneMeno"),
            meno,
            "Krstné meno"
        )
        self._safe_fill(
            self.page.locator("#input-priezvisko"),
            priezvisko,
            "Priezvisko"
        )
        self._safe_fill(
            self.page.locator("#input-rodnePriezvisko"),
            priezvisko,
            "Rodné priezvisko"
        )

        self._safe_click(
            self.page.locator("button.btn-dalej.last-focusable:visible"),
            "Ďalej - krok 1"
        )

        self._safe_fill(
            self.page.locator("#input-miestoNarodenia"),
            "Slovensko",
            "Miesto narodenia"
        )
        self._safe_fill(
            self.page.locator("#adresaTPKrajina input.autocomplete-input"),
            "Slovenská re",
            "Krajina"
        )
        self._safe_click(
            self.page.locator("#adresaTPKrajina").get_by_text("Slovenská republika", exact=True),
            "Slovenská republika"
        )

        self._safe_fill(
            self.page.locator("#adresaTPAdresaRA input.autocomplete-input"),
            self.ADRESA,
            "Adresa"
        )
        self._safe_click(
            self.page.locator("#adresaTPAdresaRA").get_by_text(self.ADRESA_LABEL, exact=True),
            self.ADRESA_LABEL
        )

        self._safe_click(
            self.page.locator("button.btn-dalej.last-focusable:visible"),
            "Pridať dieťa"
        )

    def step_1_vyber_ziaka(self):
        self._click_dalej("Ďalej - výber žiaka 1")
        self._click_dalej("Ďalej - výber žiaka 2")

    def step_2_SVVP(self):
        self._safe_check(
            self.page.locator("#zmenenaPracovnaSchopnostRadio_option_1"),
            "Zmenená pracovná schopnosť - Nie"
        )
        self._safe_check(
            self.page.locator("#specialneVVP_option_1"),
            "Špeciálne výchovno-vzdelávacie potreby - Nie"
        )
        self._safe_check(
            self.page.locator("#mentalnePostihnutie_option_1"),
            "Mentálne postihnutie - Nie"
        )
        self._safe_fill(
            self.page.locator("#textarea-DPDPoznamkaText"),
            "ŠVVP",
            "Poznámka"
        )
        self._click_dalej("Ďalej - krok SVVP")

    def step_3_vyber_skoly(self, nazov: str):
        self._safe_fill(
            self.page.locator("#fulltext-input-SS"),
            nazov,
            "Názov školy alebo jej adresa"
        )
        self._safe_click(
            self.page.locator("#fulltext-input-SS-button"),
            "Hľadať školu"
        )
        self._safe_click(
            self.page.locator("button.pridat-do-prihlasky").nth(3),
            "Pridať školu do prihlášky"
        )
        self._click_dalej("Ďalej - výber školy 1")

        self._expect_contains_text(
            self.page.locator("#vyber-skoly-message-panel"),
            "Prihlášku môžete podať len na jeden odbor.",
            "Po výbere školy sa nezobrazila informácia, že prihlášku možno podať len na jeden odbor."
        )

        self._click_dalej("Ďalej - výber školy 2")

    def step_3_vyber_skoly_1_kolo(self, nazov: str):
        self._safe_fill(
            self.page.locator("#fulltext-input-SS"),
            nazov,
            "Názov školy alebo jej adresa"
        )
        self._safe_click(
            self.page.locator("#fulltext-input-SS-button"),
            "Hľadať školu"
        )
        self._safe_click(
            self.page.locator("button.pridat-do-prihlasky").nth(3),
            "Pridať školu do prihlášky"
        )
        self._click_dalej("Ďalej - výber školy 1")

        self._safe_select(
            self.page.get_by_label("Termín prijímacej skúšky"),
            self.TERMIN_PRIJIMACEJ_SKUSKY,
            "Termín prijímacej skúšky"
        )

        self._click_dalej("Ďalej - výber školy 2")
        self._click_dalej("Ďalej - výber školy 3")
        self._safe_click(
            self.page.get_by_role("button", name="Mám skontrolované"),
            "Mám skontrolované"
        )

    def step_4_ZZ(self):
        # Portál skryl výber "Uveďte adresu, na ktorú prijímate poštové zásielky"
        # (#zastupca1AdresaRadio má triedu hidden), formulár inej adresy je rovno viditeľný.
        self._safe_fill(
            self.page.locator("#zastupca1InaAdresaKrajina input.autocomplete-input"),
            "Slovenská re",
            "Krajina korešpondenčnej adresy"
        )
        self._safe_click(
            self.page.locator("#zastupca1InaAdresaKrajina").get_by_text("Slovenská republika", exact=True),
            "Slovenská republika"
        )
        self._safe_fill(
            self.page.locator("#zastupca1InaAdresaAdresaRA input.autocomplete-input"),
            self.ADRESA,
            "Korešpondenčná adresa"
        )
        self._safe_click(
            self.page.locator("#zastupca1InaAdresaAdresaRA").get_by_text(self.ADRESA_LABEL, exact=True),
            self.ADRESA_LABEL
        )

        self._safe_check(
            self.page.locator("#zastupca2Radio_option_1"),
            "Druhý zákonný zástupca nie je známy"
        )
        self._click_dalej("Ďalej - krok zákonný zástupca")

    def step_5_ziak_navsteva_skoly(self):
        self._safe_check(
            self.page.locator("#prichodZiakaRadio_option_1"),
            "Zo školy v zahraničí"
        )

        self._safe_select(
            self.page.locator("#select-rocnikSelect"),
            "9",
            "Ročník"
        )
        self._safe_select(
            self.page.locator("#select-rokSkolskejDochadzkySelect"),
            "9",
            "Rok školskej dochádzky"
        )

        self._safe_fill(
            self.page.locator("#vyucovaciJazykVZakladnejSkoleAutocomplete input.autocomplete-input"),
            "francúzsky",
            "Jazyk školy"
        )
        self._safe_click(
            self.page.locator("#vyucovaciJazykVZakladnejSkoleAutocomplete").get_by_text("francúzsky", exact=True),
            "francúzsky"
        )
        self._click_dalej("Ďalej - návšteva školy")

    def step_6_znamky(self):
        self._safe_select(
            self.page.locator("#select-hodnotenie-1-1"),
            "30",
            "Hodnotenie 6. ročník - 1"
        )
        self._safe_select(
            self.page.locator("#select-hodnotenie-1-2"),
            "1",
            "Hodnotenie 6. ročník - 2"
        )
        for _ in range(17):
            self._safe_click(
                self.page.locator("button.btn-odstranit:visible").nth(2),
                "Odstrániť predmet zo 6. ročníka"
            )

        self._safe_click(
            self.page.get_by_text("7. ročník", exact=True),
            "7. ročník"
        )
        self._safe_select(
            self.page.locator("#select-hodnotenie-2-1"),
            "31",
            "Hodnotenie 7. ročník - 1"
        )
        self._safe_select(
            self.page.locator("#select-hodnotenie-2-2"),
            "3",
            "Hodnotenie 7. ročník - 2"
        )
        for _ in range(17):
            self._safe_click(
                self.page.locator("button.btn-odstranit:visible").nth(2),
                "Odstrániť predmet zo 7. ročníka"
            )

        self._safe_click(
            self.page.get_by_text("8. ročník", exact=True),
            "8. ročník"
        )
        self._safe_select(
            self.page.locator("#select-hodnotenie-3-1"),
            "29",
            "Hodnotenie 8. ročník - 1"
        )
        self._safe_select(
            self.page.locator("#select-hodnotenie-3-2"),
            "2",
            "Hodnotenie 8. ročník - 2"
        )
        for _ in range(17):
            self._safe_click(
                self.page.locator("button.btn-odstranit:visible").nth(2),
                "Odstrániť predmet z 8. ročníka"
            )

        self._safe_click(
            self.page.get_by_text("9. ročník", exact=True),
            "9. ročník"
        )
        self._safe_select(
            self.page.locator("#select-hodnotenie-4-1"),
            "29",
            "Hodnotenie 9. ročník - 1"
        )
        self._safe_select(
            self.page.locator("#select-hodnotenie-4-2"),
            "1",
            "Hodnotenie 9. ročník - 2"
        )
        for _ in range(17):
            self._safe_click(
                self.page.locator("button.btn-odstranit:visible").nth(2),
                "Odstrániť predmet z 9. ročníka"
            )

        self._click_dalej("Ďalej - známky")

    def step_7_sutaze(self):
        self._safe_click(
            self.page.locator("#btn-pridat-sutaz"),
            "Pridať súťaž"
        )
        self._safe_fill(
            self.page.locator("#input-modalNazovSutazeText"),
            "Zumba",
            "Názov súťaže"
        )

        self._safe_select(
            self.page.locator("#select-modalDruhSutazeSelect"),
            "2",
            "Druh súťaže"
        )
        self._safe_select(
            self.page.locator("#select-modalUrovenSutazeSelect"),
            "6",
            "Úroveň súťaže"
        )

        self._safe_check(
            self.page.locator("#modalTypUmiestneniaRadio_option_0"),
            "1. miesto"
        )

        self._safe_select(
            self.page.locator("#select-modalSkolskyRokSelect"),
            "2023/2024",
            "Školský rok"
        )

        self._safe_click(
            self.page.locator("button.btn-pridat:visible"),
            "Pridať súťaž"
        )
        self._click_dalej("Ďalej - súťaže")

    def step_8_prilohy(self):
        self._upload_prilohy(1, "Príloha - Vysvedčenie zo 6. ročníka")
        self._upload_prilohy(2, "Príloha - Vysvedčenie zo 7. ročníka")
        self._upload_prilohy(3, "Príloha - Vysvedčenie z 8. ročníka")
        self._upload_prilohy(4, "Príloha - Vysvedčenie z 9. ročníka")
        self._upload_prilohy(5, "Príloha - Olympiáda alebo súťaž Zumba")
        self._upload_prilohy(6, "Príloha - Potvrdenie o zdravotnej spôsobilosti (stredná škola)")

        self._click_dalej("Ďalej - prílohy")

    def click_on_odoslat_prihlasku(self):
        self._safe_click(
            self.page.locator("#cestnePrehlasenie > .checkmark"),
            "Čestné prehlásenie"
        )
        self._safe_click(
            self.page.locator("#suhlasOsobneUdaje > .checkmark"),
            "Súhlas so spracovaním osobných údajov"
        )
        self._safe_click(
            self.page.locator("button.btn-odoslat-prihlasku"),
            "Odoslať prihlášku"
        )

    def click_on_potvrdit_odoslanie(self):
        self._safe_click(
            self.page.locator("button.btn-confirm.govuk-button.govuk-button__large.last-focusable"),
            "Potvrdiť odoslanie prihlášky"
        )
        self.page.wait_for_load_state("networkidle")

    def vyhladanie_prihlasky(self, meno: str, priezvisko: str):
        self.page.wait_for_load_state("networkidle")

        self._safe_select(
            self.page.get_by_label("Kolo"),
            "2",
            "Kolo"
        )
        self._safe_select(
            self.page.get_by_label("Odbor"),
            self.ODBOR_2_KOLO,
            "Odbor pre ďalšie kolo"
        )

        self.page.wait_for_load_state("networkidle")
        self._vyhladaj_prihlasku(meno, priezvisko, "Vyhľadávanie prihlášky")

    def vyhladanie_prihlasky_1_kolo(self, meno: str, priezvisko: str):
        self.page.wait_for_load_state("networkidle")

        self._safe_select(
            self.page.get_by_label("Odbor"),
            self.ODBOR_1_KOLO,
            "Odbor pre 1. kolo"
        )

        self.page.wait_for_load_state("networkidle")
        self._vyhladaj_prihlasku(meno, priezvisko, "Vyhľadávanie prihlášky pre 1. kolo")

    def click_on_prejst_na_prihlasky(self):
        self._safe_click(
            self.page.get_by_role("button", name="Prejsť na prihlášky"),
            "Prejsť na prihlášky"
        )