import pytest
import os
import re
import utils.data_helper as Data
from utils.helpers import Helper
from utils.mail_helper import Mail
from pages.logout_page import LogoutPage
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.prihlaska_ZS_page import PrihlaskaZS
from pages.papierova_prihlaska_ZS_page import PapierovaPrihlaskaZS
from pages.prilohy_ZS_page import PrilohyZS


mailuser = os.getenv("GMAIL_USERNAME")
mailpw = os.getenv("GMAIL_APP_PASSWORD")
username = os.getenv("EPRIHLASKY_ZZ_USERNAME")
password = os.getenv("EPRIHLASKY_ZZ_PASSWORD")
username_riad = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password_riad = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


@pytest.fixture(scope="module")
def person_data():
    return Data.generate_unique_person(min_age=6, max_age=7)


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_prihlaska_na_ZS(page: Page, person_data) -> None:
    data = person_data
    helper = Helper()
    login = LoginPage(page)
    logout = LogoutPage(page)
    prihlaska = PrihlaskaZS(page)
    prihlaska_papierova = PapierovaPrihlaskaZS(page)

    login.login_as_zakonny_zastupca(username, password)
    prihlaska.pridanie_prihlasky()
    prihlaska.step_1_pridat_dieta(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska.step_2_SVVP()
    prihlaska.step_3_vyber_skoly("Základná škola pre AT")
    prihlaska.step_4_ZZ()
    prihlaska.step_5_prilohy()

    expect(
        page.locator("#suhrnny-prehlad").get_by_text("P-2026-"),
        "Identifikátor prihlášky sa v súhrnnom prehľade nezobrazil."
    ).to_be_visible()

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba školský rok 2026/2027."
    ).to_contain_text("2026/2027")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba meno dieťaťa."
    ).to_contain_text(data.meno)

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba priezvisko dieťaťa."
    ).to_contain_text(data.priezvisko)

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba rodné číslo dieťaťa."
    ).to_contain_text(data.rodne_cislo)

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba dátum narodenia dieťaťa."
    ).to_contain_text(helper.rc_to_datum_narodenia(data.rodne_cislo))

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba štát Slovensko."
    ).to_contain_text("Slovensko")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba slovenský jazyk."
    ).to_contain_text("slovenská")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba Slovenská republika."
    ).to_contain_text("Slovenská republika")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba rodný jazyk."
    ).to_contain_text("slovenský")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba adresa dieťaťa."
    ).to_contain_text("Cibulková 8/63, 03687, Brusno, Slovenská republika")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba náboženské vyznanie."
    ).to_contain_text("Náboženská - Rímskokatolícka")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýbajú hodnoty Áno."
    ).to_contain_text("Áno")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýbajú hodnoty Nie."
    ).to_contain_text("Nie")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba položka ŠVVP."
    ).to_contain_text("ŠVVP")

    expect(
        page.locator("#skoly"),
        "Vybraná škola sa v prehľade škôl nezobrazila."
    ).to_contain_text("Základná škola pre AT")

    expect(
        page.locator("#skoly"),
        "Adresa školy sa v prehľade škôl nezobrazila."
    ).to_contain_text("Jalmová 266/19, 06534 Prešov")

    expect(
        page.locator("#zastupcovia"),
        "V prehľade zákonných zástupcov chýba meno."
    ).to_contain_text("Mária")

    expect(
        page.locator("#zastupcovia"),
        "V prehľade zákonných zástupcov chýba priezvisko."
    ).to_contain_text("Bartošová")

    expect(
        page.locator("#zastupcovia"),
        "V prehľade zákonných zástupcov chýba rodné číslo."
    ).to_contain_text("855215/3830")

    expect(
        page.locator("#zastupcovia"),
        "V prehľade zákonných zástupcov chýba dátum narodenia."
    ).to_contain_text("15.02.1985")

    expect(
        page.locator("#zastupcovia"), #zastupovcovia
        "V prehľade zákonných zástupcov chýba adresa."
    ).to_contain_text("Mandľová 16/745, 03874, Trenčianska Teplá, Slovenská republika")

    expect(
        page.locator("#zastupcovia"),
        "V prehľade zákonných zástupcov chýba e-mail."
    ).to_contain_text("katalontest987@gmail.com")

    expect(
        page.locator("#zastupcovia"),
        "V prehľade zákonných zástupcov chýba telefónne číslo."
    ).to_contain_text("+421999888777")

    expect(
        page.locator("#zastupcovia"),
        "V prehľade zákonných zástupcov chýba informácia o druhom zákonnom zástupcovi."
    ).to_contain_text("Druhý zákonný zástupca nie je známy.")

    expect(
        page.locator("#prilohyContainer"),
        "V súhrne príloh sa nezobrazila informácia o nenahratých prílohách."
    ).to_contain_text("Neboli nahrané žiadne prílohy.")

    prihlaska.accept_terms_and_submit()

    expect(
        page,
        "Po odoslaní prihlášky sa neprepla na stránku 'Prihlaska-odoslana'."
    ).to_have_url(re.compile(r".*/Prihlaska-odoslana.*"), timeout=60000)

    expect(
        page.locator("h1"),
        "Na potvrdení odoslania sa nezobrazil úspešný nadpis."
    ).to_contain_text("Prihláška bola úspešne odoslaná!")

    prihlaska.click_on_prejst_na_prihlasky()
    logout.logout()

    login.login_as_riaditel(username_riad, password_riad, "910021625")
    prihlaska_papierova.najdi_prihlasku(data.meno, data.priezvisko)
    prihlaska_papierova.click_on_zobrazit_prihlasku()

    expect(
        page.locator("#detail-prihlasky-riad-MS-ZS-content"),
        "V detaile prihlášky na strane riaditeľa sa nezobrazuje stav 'Elektronicky'."
    ).to_contain_text("Elektronicky")

    expect(
        page.locator("#detail-prihlasky-riad-MS-ZS-content"),
        "V detaile prihlášky na strane riaditeľa sa nezobrazuje stav 'Podaná'."
    ).to_contain_text("Podaná")

    expect(
        page.locator("#dietaMeno"),
        "V detaile prihlášky chýba meno dieťaťa."
    ).to_contain_text(data.meno)

    expect(
        page.locator("#dietaPriezvisko"),
        "V detaile prihlášky chýba priezvisko dieťaťa."
    ).to_contain_text(data.priezvisko)

    expect(
        page.locator("#dietaRodneCislo"),
        "V detaile prihlášky chýba rodné číslo dieťaťa."
    ).to_contain_text(data.rodne_cislo)


@pytest.mark.regres1kolo
@pytest.mark.regres2kolo
def test_doplnenie_prilohy_na_ZS(page: Page, person_data) -> None:
    data = person_data
    helper = Helper()
    login = LoginPage(page)
    logout = LogoutPage(page)
    mail = Mail()
    prilohy = PrilohyZS(page)
    prihlaska_papierova = PapierovaPrihlaskaZS(page)

    login.login_as_riaditel(username_riad, password_riad, "910021625")
    prihlaska_papierova.najdi_prihlasku(data.meno, data.priezvisko)
    prihlaska_papierova.click_on_zobrazit_prihlasku()

    expect(
        page.locator("#detail-prihlasky-riad-MS-ZS-content"),
        "Na detaile prihlášky sa nezobrazuje stav 'Podaná'."
    ).to_contain_text("Podaná")

    identifikator = page.locator("div.prihlaskaIdentifikator").text_content()

    prilohy.vyziadat_prilohu("Odvolanie prílohy.")

    expect(
        page.locator("#detail-prihlasky-riad-MS-ZS-content"),
        "Po odvolaní výzvy sa prihláška neprepína do stavu 'Neúplná'."
    ).to_contain_text("Neúplná")

    prilohy.odvolat_ziadost()

    odvolanie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    odvolanie_prilohy = helper.cleanup_email_text(odvolanie_prilohy)
    expected = (
        f"Vážený/á pán/pani Mária Bartošová, radi by sme Vás informovali, že požiadavka na doloženie dodatočných dokumentov príloh k Vašej prihláške zaevidovanej v portáli Elektronické prihlášky do škôl bola zrušená. Nie je teda potrebné dodatočne nahrávať žiadne ďalšie prílohy k prihláške pre: {data.meno} {data.priezvisko} nar. {helper.rc_to_datum_narodenia(data.rodne_cislo)}. Ak ste už zadali dokumenty na základe predchádzajúceho odkazu, upozorňujeme, že tento odkaz je už neaktívny. V prípade akýchkoľvek otázok nás neváhajte kontaktovať. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň.\""
    )
    assert odvolanie_prilohy == expected, "Text e-mailu o odvolaní prílohy sa nezhoduje s očakávaným obsahom."

    expect(
        page.locator("#skoly"),
        "V prehľade škôl sa nezobrazila informácia o odvolanej výzve."
    ).to_contain_text("info Výzva odvolaná")

    expect(
        page.locator("#detail-prihlasky-riad-MS-ZS-content"),
        "Po odvolaní výzvy sa prihláška nevrátila do stavu 'Podaná'."
    ).to_contain_text("Podaná")

    prilohy.vyziadat_prilohu("Vyžiadanie prílohy.")

    vyziadanie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyziadanie_prilohy = helper.cleanup_email_text(vyziadanie_prilohy)
    expected = (
        f"Vážený/á pán/pani Mária Bartošová, pri kontrole prihlášky {identifikator} pre školu Základná škola pre AT pre {data.meno} {data.priezvisko} sme zistili, že je potrebné doložiť nasledujúcu prílohu: Čestné vyhlásenie zákonného zástupcu z dôvodu že \" Vyžiadanie prílohy. \". Prosíme Vás o doplnenie požadovanej prílohy k prihláške. Doplnenie príloh môžete vykonať prostredníctvom portálu Elektronické prihlášky do škôl: Link na prihlásenie Ak ešte nemáte vytvorené konto, zaregistrujte sa prostredníctvom odkazu: Registrovať sa Po registrácii a prihlásení sa dostanete do sekcie Moje prihlášky, kde nájdete možnosť pridať existujúcu prihlášku do svojho konta. Na pridanie prihlášky zadajte tento identifikátor prihlášky: {identifikator} Po pridaní prihlášky do konta budete môcť sledovať jej stav, doplniť požadované prílohy a komunikovať so školou. V prípade, že už konto v portáli máte, prihláste sa a pokračujte podľa pokynov v portáli. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
    )
    assert vyziadanie_prilohy == expected, "Text e-mailu o vyžiadanej prílohe sa nezhoduje s očakávaným obsahom."

    expect(
        page.locator("#message-box"),
        "Žiadosť o doplnenie prílohy sa neodoslala úspešne."
    ).to_contain_text("Žiadosť o doplnenie prílohy bola úspešne odoslaná")

    expect(
        page.locator("#info-panel-red-neuplnu-prihlasku-nie-je-mozne-oznacit-ako-skontrolovanu"),
        "Chýba informácia, že neúplnú prihlášku nie je možné označiť ako skontrolovanú."
    ).to_contain_text("Neúplnú prihlášku nie je možné označiť ako skontrolovanú")

    expect(
        page.locator("#info-panel-red-neuplnu-prihlasku-nie-je-mozne-oznacit-ako-skontrolovanu"),
        "Chýba vysvetlenie stavu neúplnej prihlášky."
    ).to_contain_text(
        "Prihláška je aktuálne v stave Neúplná. Tento stav zostáva platný až do momentu, kým zákonný zástupca požadovanú prílohu nedoplní, alebo kým neodvoláte výzvu na jej doplnenie."
    )

    logout.logout()
    login.login_as_zakonny_zastupca(username, password)

    expect(
        page,
        "Po prihlásení zákonného zástupcu sa neotvorila stránka so zoznamom prihlášok."
    ).to_have_url(re.compile(r".*/Prihlasky*"), timeout=60000)

    expect(
        page.locator("#moje-prihlasky"),
        "Na stránke Moje prihlášky sa nezobrazila výzva na doplnenie príloh."
    ).to_contain_text(
        "Nahrajte prílohyRiaditeľ základnej školy požaduje doplnenie príloh. Pridanie prílohy nájdete v stĺpci Akcia."
    )

    prilohy.pridat_prilohu()

    expect(
        page.locator("#pridat-prilohy"),
        "Po nahratí prílohy sa nezobrazila úspešná hláška."
    ).to_contain_text("Dokumenty ste úspešne nahrali")

    expect(
        page.locator("#pridat-prilohy"),
        "Po nahratí prílohy sa nezobrazilo potvrdenie o ďalšom posúdení prihlášky."
    ).to_contain_text("Vaša prihláška bude čoskoro posúdená. Ďakujeme za trpezlivosť.")

    prijatie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    prijatie_prilohy = helper.cleanup_email_text(prijatie_prilohy)
    expected = (
        f"Vážený/á pán/pani/ Mária Bartošová, dovoľujeme si Vás informovať, že k Vašej prihláške do Základná škola pre AT pre {data.meno} {data.priezvisko}, zaevidovanej v elektronickom portáli prihlášok bola doručená príloha s názvom Čestné vyhlásenie zákonného zástupcu. Doručenú prílohu si prosím starostlivo skontrolujte prihlásením sa na portáli Elektronických prihlášok v detaile prihlášky, alebo v prílohe tohto mailu. Prihlásením sa na portáli zároveň získate aj ďalšie informácie o stave Vašej prihlášky a priebehu jej spracovania. Link na prihlásenie S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň.\""
    )
    assert prijatie_prilohy == expected, "Text e-mailu o prijatí prílohy sa nezhoduje s očakávaným obsahom."

    prilohy.click_on_prejst_na_prihlasky()
    logout.logout()

    login.login_as_riaditel(username_riad, password_riad, "910021625")
    prihlaska_papierova.najdi_prihlasku(data.meno, data.priezvisko)
    prihlaska_papierova.click_on_zobrazit_prihlasku()

    expect(
        page.locator("#detail-prihlasky-riad-MS-ZS-content"),
        "Na strane riaditeľa sa po doplnení prílohy nezobrazil stav 'Doplnená'."
    ).to_contain_text("Doplnená")

    expect(
        page.locator("#skoly"),
        "V prehľade škôl sa nezobrazil zoznam priložených dokumentov."
    ).to_contain_text("Priložené dokumenty:")