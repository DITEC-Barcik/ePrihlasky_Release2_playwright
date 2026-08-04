import os
import re
import pytest
import utils.data_helper as Data

from utils.helpers import Helper
from utils.mail_helper import Mail
from pages.logout_page import LogoutPage
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.prihlaska_SS_page import PrihlaskaSS
from pages.prilohy_SS_page import PrilohySS


mailuser = os.getenv("GMAIL_USERNAME")
mailpw = os.getenv("GMAIL_APP_PASSWORD")
username = os.getenv("EPRIHLASKY_ZZ_USERNAME")
password = os.getenv("EPRIHLASKY_ZZ_PASSWORD")
username_riad = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password_riad = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


@pytest.fixture(scope="module")
def person_data():
    return Data.generate_unique_person(min_age=15, max_age=17)


def _expect_text(locator, text, message: str) -> None:
    expect(locator, message).to_contain_text(text)


def _expect_visible(locator, message: str) -> None:
    expect(locator, message).to_be_visible()


def _expect_url(page: Page, pattern: str, message: str, timeout: int = 60000) -> None:
    expect(page, message).to_have_url(re.compile(pattern), timeout=timeout)


def _assert_equal(actual: str, expected: str, message: str) -> None:
    assert actual == expected, (
        f"{message}\n\n=== EXPECTED ===\n{expected}\n\n=== ACTUAL ===\n{actual}"
    )


def _expect_summary(page: Page, data, helper: Helper) -> None:
    summary = page.locator("#suhrnny-prehlad")

    _expect_text(summary, re.compile(r"P-2026-.+"), "V súhrne chýba identifikátor prihlášky.")
    _expect_text(summary, "2026/2027", "V súhrne chýba školský rok.")
    _expect_text(summary, "2. kolo", "V súhrne chýba informácia o 2. kole.")
    _expect_text(summary, data.meno, "V súhrne chýba meno dieťaťa.")
    _expect_text(summary, data.priezvisko, "V súhrne chýba priezvisko dieťaťa.")
    _expect_text(summary, data.rodne_cislo, "V súhrne chýba rodné číslo dieťaťa.")
    _expect_text(
        summary,
        helper.rc_to_datum_narodenia(data.rodne_cislo),
        "V súhrne chýba dátum narodenia dieťaťa."
    )

    pohlavie = "žena" if helper.get_pohlavie(data.rodne_cislo) == "ženské" else "muž"
    _expect_text(summary, pohlavie, "V súhrne chýba pohlavie dieťaťa.")
    _expect_text(summary, "Slovensko", "V súhrne chýba miesto narodenia.")
    _expect_text(summary, "slovenská", "V súhrne chýba národnosť.")
    _expect_text(summary, "Slovenská republika", "V súhrne chýba štátna príslušnosť.")
    _expect_text(summary, "slovenský", "V súhrne chýba materinský jazyk.")
    _expect_text(summary, "Narcisová 4/2048, 03845, Myjava, Slovenská republika", "V súhrne chýba adresa dieťaťa.")
    _expect_text(summary, "ŠVVP", "V súhrne chýba informácia o ŠVVP.")


def _expect_school(page: Page) -> None:
    skoly = page.locator("#skoly")
    for text, msg in [
        ("1 Stredná škola č. 1", "V sekcii škôl chýba poradie školy."),
        ("910021624", "V sekcii škôl chýba EDUID školy."),
        ("Stredná škola pre AT", "V sekcii škôl chýba názov školy."),
        ("2285H00", "V sekcii škôl chýba kód odboru."),
        ("zlievač -3 ročné", "V sekcii škôl chýba odbor."),
        ("Netalentový", "V sekcii škôl chýba typ odboru."),
        ("1. termín", "V sekcii škôl chýba termín."),
        ("slovenský", "V sekcii škôl chýba vyučovací jazyk."),
    ]:
        _expect_text(skoly, text, msg)


def _expect_guardians(page: Page) -> None:
    z = page.locator("#zastupcovia")
    for text, msg in [
        ("Osobné údaje zákonného zástupcu č. 1", "Chýba sekcia zákonného zástupcu č. 1."),
        ("Mária", "Chýba meno zákonného zástupcu."),
        ("Bartošová", "Chýba priezvisko zákonného zástupcu."),
        ("855215/3830", "Chýba rodné číslo zákonného zástupcu."),
        ("15.02.1985", "Chýba dátum narodenia zákonného zástupcu."),
        ("Mandľová 16/745, 03874, Trenčianska Teplá, Slovenská republika", "Chýba adresa zákonného zástupcu."),
        ("katalontest987@gmail.com", "Chýba e-mail zákonného zástupcu."),
        ("+421999888777", "Chýba telefón zákonného zástupcu."),
        ("Osobné údaje zákonného zástupcu č. 2", "Chýba sekcia zákonného zástupcu č. 2."),
        ("Druhý zákonný zástupca nie je známy.", "Chýba informácia o druhom zákonnom zástupcovi."),
    ]:
        _expect_text(z, text, msg)


def _expect_zs_info(page: Page) -> None:
    info = page.locator("#info-o-zs")
    for text, msg in [
        ("Informácie o základnej škole", "Chýba hlavička informácií o základnej škole."),
        ("Zo školy v zahraničí", "Chýba informácia o pôvode zo školy v zahraničí."),
        ("9.", "Chýba ročník."),
        ("9", "Chýba rok školskej dochádzky."),
        ("Francúzsky", "Chýba vyučovací jazyk."),
    ]:
        _expect_text(info, text, msg)


def _expect_results(page: Page) -> None:
    results = page.locator("#vysledky-vzdelavania-suhrn")
    for text, msg in [
        ("6. ročník (2. polrok)", "Chýba výsledok za 6. ročník."),
        ("uspokojivé", "Chýba správanie za 6. ročník."),
        ("1 - výborný", "Chýba klasifikácia za 6. ročník."),
        ("7. ročník (2. polrok)", "Chýba výsledok za 7. ročník."),
        ("menej uspokojivé", "Chýba správanie za 7. ročník."),
        ("3 - dobrý", "Chýba klasifikácia za 7. ročník."),
        ("8. ročník (2. polrok)", "Chýba výsledok za 8. ročník."),
        ("veľmi dobré", "Chýba správanie za 8. ročník alebo 9. ročník."),
        ("2 - chválitebný", "Chýba klasifikácia za 8. ročník."),
        ("9. ročník (1. polrok)", "Chýba výsledok za 9. ročník."),
        ("1 - výborný", "Chýba klasifikácia za 9. ročník."),
    ]:
        _expect_text(results, text, msg)


def _expect_competitions(page: Page) -> None:
    sutaze = page.locator("#sutaze-suhrn")
    for text, msg in [
        ("Zumba", "Chýba súťaž Zumba."),
        ("1. miesto - Školská úroveň", "Chýba umiestnenie v súťaži."),
        ("Umelecké", "Chýba kategória súťaže."),
        ("Školský rok: 2023/2024", "Chýba školský rok súťaže."),
    ]:
        _expect_text(sutaze, text, msg)


@pytest.mark.regres2kolo
def test_prihlaska_na_SS_2_kolo(page: Page, person_data) -> None:
    data = person_data
    helper = Helper()
    login = LoginPage(page)
    logout = LogoutPage(page)
    prihlaska = PrihlaskaSS(page)

    login.login_as_zakonny_zastupca(username, password)
    prihlaska.click_on_vytvorit_prihlasku()
    prihlaska.pridat_dieta(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska.step_1_vyber_ziaka()
    prihlaska.step_2_SVVP()
    prihlaska.step_3_vyber_skoly("pre AT")
    prihlaska.step_4_ZZ()
    prihlaska.step_5_ziak_navsteva_skoly()
    prihlaska.step_6_znamky()
    prihlaska.step_7_sutaze()
    prihlaska.step_8_prilohy()

    _expect_summary(page, data, helper)
    _expect_school(page)
    _expect_guardians(page)
    _expect_zs_info(page)
    _expect_results(page)
    _expect_competitions(page)

    _expect_visible(page.locator(".prilohaItem").first, "Prvá príloha sa nezobrazuje.")
    for idx in range(2, 6):
        _expect_visible(page.locator(f"#prilohyContainer > div:nth-child({idx})"), f"Príloha číslo {idx} sa nezobrazuje.")

    _expect_text(
        page.locator("#layoutDorucenie"),
        "Rozhodnutia o prijatí budú zverejnené na elektronickej výveske, o čom budete informovaný e-mailovou správou.",
        "V sekcii doručenia chýba text o elektronickej výveske."
    )

    prihlaska.click_on_odoslat_prihlasku()
    _expect_text(
        page.locator("body"),
        "Chystáte sa odoslať prihlášku na stredné školy, ktoré ste uviedli v prihláške.",
        "Nezobrazil sa potvrdzovací text pred odoslaním prihlášky."
    )

    prihlaska.click_on_potvrdit_odoslanie()

    _expect_url(page, r".*/Prihlaska-odoslana.*", "Po odoslaní prihlášky sa neotvorila stránka 'Prihláška odoslaná'.")
    _expect_text(page.locator("h1"), "Prihláška bola úspešne odoslaná!", "Po odoslaní sa nezobrazil úspešný nadpis.")

    identifikator = page.get_by_text("P-2026-").text_content()
    prihlaska.click_on_prejst_na_prihlasky()

    _expect_url(page, r".*/Prihlasky.*", "Po prechode na prihlášky sa neotvoril správny zoznam.")
    logout.logout()

    login.login_as_riaditel(username_riad, password_riad, "910021624")
    prihlaska.vyhladanie_prihlasky(data.meno, data.priezvisko)

    _expect_visible(page.get_by_text(f"{data.priezvisko} {data.meno}", exact=True), "V zozname sa nenašlo meno dieťaťa.")
    _expect_visible(page.get_by_text(identifikator, exact=True), "V zozname sa nenašiel identifikátor prihlášky.")
    _expect_text(
        page.locator("div[class='sub-container'] div[class='scrollable-middle-area'] div:nth-child(2) div:nth-child(1) div:nth-child(1)"),
        "V spracovaní",
        "Prihláška nemá očakávaný stav 'V spracovaní'."
    )


@pytest.mark.regres2kolo
def test_doplnenie_prilohy_na_SS_2_kolo(page: Page) -> None:
    helper = Helper()
    mail = Mail()
    login = LoginPage(page)
    logout = LogoutPage(page)
    priloha = PrilohySS(page)

    login.login_as_riaditel(username_riad, password_riad, "910021624")
    priloha.najdi_poslednu_prihlasku()

    _expect_text(page.locator("#detail-prihlasky-riad-SS-content"), "Elektronicky", "V detaile prihlášky chýba spôsob podania 'Elektronicky'.")

    meno = page.locator("#dietaMeno").text_content()
    priezvisko = page.locator("#dietaPriezvisko").text_content()
    identifikator = page.locator("div.prihlaskaIdentifikator").text_content()
    datum_narodenia = page.locator("#dietaDatumNarodenia").text_content()

    priloha.vyziadaj_prilohu_na_poslednej_prihlaske()
    _expect_text(page.locator("#message-box"), "Žiadosť o doplnenie prílohy bola úspešne odoslaná", "Žiadosť o doplnenie prílohy sa neodoslala správne.")
    _expect_text(page.locator("#detail-prihlasky-riad-SS-content"), "Neúplná", "Stav prihlášky sa po žiadosti nezmenil na 'Neúplná'.")
    _expect_text(page.locator("#skoly"), "Riaditeľ školy Stredná škola pre AT požadoval ďalšie prílohy.", "V sekcii škôl chýba informácia o požadovaných prílohách.")
    _expect_text(page.locator("#skoly"), "Čestné vyhlásenie zákonného zástupcu", "V sekcii škôl chýba názov požadovanej prílohy.")
    _expect_text(page.locator("#skoly"), "Žiadam o úpravu alebo doplnenie príloh v prihláške na školu. Detaily v sprievodnom texte: Žiadosť o doplnenie prílohy.", "V sekcii škôl chýba sprievodný text k žiadosti.")

    priloha.odvolanie_ziadosti()

    odvolanie_prilohy = helper.cleanup_email_text(mail.get_last_email_text("imap.gmail.com", mailuser, mailpw))
    expected_odvolanie = (
        f"Vážený/á pán/pani Mária Bartošová, radi by sme Vás informovali, že požiadavka na doloženie dodatočných dokumentov "
        f"príloh k Vašej prihláške zaevidovanej v portáli Elektronické prihlášky do škôl bola zrušená. Nie je teda potrebné "
        f"dodatočne nahrávať žiadne ďalšie prílohy k prihláške pre: {meno} {priezvisko} nar. {datum_narodenia}. Ak ste už zadali "
        f"dokumenty na základe predchádzajúceho odkazu, upozorňujeme, že tento odkaz je už neaktívny. V prípade akýchkoľvek "
        f"otázok nás neváhajte kontaktovať. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný "
        f"automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže "
        f"Slovenskej republiky. Neodpovedajte naň.\""
    )
    _assert_equal(odvolanie_prilohy, expected_odvolanie, "Obsah e-mailu o odvolaní žiadosti o prílohu nezodpovedá očakávaniu.")

    _expect_text(page.locator("#skoly"), "info Výzva odvolaná", "Po odvolaní žiadosti sa nezobrazil text 'Výzva odvolaná'.")
    _expect_text(page.locator("#detail-prihlasky-riad-SS-content"), "V spracovaní", "Po odvolaní žiadosti sa stav prihlášky nevrátil na 'V spracovaní'.")

    priloha.vyziadaj_prilohu_na_poslednej_prihlaske()

    vyziadanie_prilohy = helper.cleanup_email_text(mail.get_last_email_text("imap.gmail.com", mailuser, mailpw))
    expected_vyziadanie = (
        f"Vážený/á pán/pani Mária Bartošová, pri kontrole prihlášky {identifikator} pre školu zlievač pre {meno} {priezvisko} "
        f"sme zistili, že je potrebné doložiť nasledujúcu prílohu: Čestné vyhlásenie zákonného zástupcu z dôvodu že \" Žiadosť o doplnenie prílohy. \". "
        f"Prosíme Vás o doplnenie požadovanej prílohy k prihláške. Doplnenie príloh môžete vykonať prostredníctvom portálu "
        f"Elektronické prihlášky do škôl: Link na prihlásenie Ak ešte nemáte vytvorené konto, zaregistrujte sa prostredníctvom odkazu: "
        f"Registrovať sa Po registrácii a prihlásení sa dostanete do sekcie Moje prihlášky, kde nájdete možnosť pridať existujúcu prihlášku "
        f"do svojho konta. Na pridanie prihlášky zadajte tento identifikátor prihlášky: {identifikator} Po pridaní prihlášky do konta "
        f"budete môcť sledovať jej stav, doplniť požadované prílohy a komunikovať so školou. V prípade, že už konto v portáli máte, "
        f"prihláste sa a pokračujte podľa pokynov v portáli. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol "
        f"generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže "
        f"Slovenskej republiky. Neodpovedajte naň."
    )
    _assert_equal(vyziadanie_prilohy, expected_vyziadanie, "Obsah e-mailu o vyžiadaní prílohy nezodpovedá očakávaniu.")

    logout.logout()

    login.login_as_zakonny_zastupca(username, password)
    _expect_text(page.locator("#moje-prihlasky"), "Nahrajte prílohy", "V sekcii 'Moje prihlášky' chýba výzva na nahratie príloh.")
    _expect_text(page.locator("#moje-prihlasky"), "Nahrajte prílohyRiaditeľ strednej školy požaduje doplnenie príloh. Pridanie prílohy nájdete v stĺpci Akcia.", "V sekcii 'Moje prihlášky' chýba vysvetľujúci text k prílohám.")

    priloha.nahrat_prilohu()
    _expect_text(page.locator("#pridat-prilohy"), "Dokumenty ste úspešne nahrali", "Po nahratí príloh sa nezobrazila úspešná hláška.")
    _expect_text(page.locator("#pridat-prilohy"), "Vaša prihláška bude čoskoro posúdená. Ďakujeme za trpezlivosť.", "Po nahratí príloh chýba ďakovná správa.")

    prijatie_prilohy = helper.cleanup_email_text(mail.get_last_email_text("imap.gmail.com", mailuser, mailpw))
    expected_prijatie = (
        f"Vážený/á pán/pani/ Mária Bartošová, dovoľujeme si Vás informovať, že k Vašej prihláške do Stredná škola pre AT zlievač "
        f"pre {meno} {priezvisko}, zaevidovanej v elektronickom portáli prihlášok bola doručená príloha s názvom Čestné vyhlásenie "
        f"zákonného zástupcu. Doručenú prílohu si prosím starostlivo skontrolujte prihlásením sa na portáli Elektronických prihlášok "
        f"v detaile prihlášky, alebo v prílohe tohto mailu. Prihlásením sa na portáli zároveň získate aj ďalšie informácie o stave "
        f"Vašej prihlášky a priebehu jej spracovania. Link na prihlásenie S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email "
        f"bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže "
        f"Slovenskej republiky. Neodpovedajte naň.\""
    )
    _assert_equal(prijatie_prilohy, expected_prijatie, "Obsah e-mailu o prijatej prílohe nezodpovedá očakávaniu.")

    priloha.click_on_prejst_na_prihlasky()
    _expect_text(page.locator("#moje-prihlasky"), "Doplnená", "Po návrate na prihlášky sa nezobrazuje stav 'Doplnená'.")

    logout.logout()

    login.login_as_riaditel(username_riad, password_riad, "910021624")
    priloha.najdi_prihlasku_po_nahrati_prilohy(meno, priezvisko)
    _expect_text(page.locator("#detail-prihlasky-riad-SS-content"), "Doplnená", "V detaile riaditeľa sa nezobrazuje stav 'Doplnená'.")
    _expect_visible(page.get_by_text("Priložené dokumenty:"), "Sekcia 'Priložené dokumenty' sa nezobrazuje.")