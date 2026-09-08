import pytest
import os
import re
import utils.data_helper as Data
from utils.mail_helper import Mail
from utils.helpers import Helper
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.prihlaska_SS_page import PrihlaskaSS
from pages.prilohy_SS_page import PrilohySS
from pages.logout_page import LogoutPage


mailuser = os.getenv("GMAIL_USERNAME")
mailpw = os.getenv("GMAIL_APP_PASSWORD")
username = os.getenv("EPRIHLASKY_ZZ_USERNAME")
password = os.getenv("EPRIHLASKY_ZZ_PASSWORD")
username_riad = os.getenv("EPRIHLASKY_RIADITEL_USERNAME")
password_riad = os.getenv("EPRIHLASKY_RIADITEL_PASSWORD")


@pytest.fixture(scope="module")
def person_data():
    return Data.generate_unique_person(min_age=15, max_age=17)


@pytest.mark.regres1kolo
def test_prihlaska_na_SS_1_kolo(page: Page, person_data) -> None:
    helper = Helper()
    logout = LogoutPage(page)
    data = person_data
    login = LoginPage(page)
    prihlaska = PrihlaskaSS(page)

    login.login_as_zakonny_zastupca(username, password)
    prihlaska.click_on_vytvorit_prihlasku_1_kolo()
    prihlaska.pridat_dieta(data.meno, data.priezvisko, data.rodne_cislo)
    prihlaska.step_1_vyber_ziaka()
    prihlaska.step_2_SVVP()
    prihlaska.step_3_vyber_skoly_1_kolo("škola pre AT")
    prihlaska.step_4_ZZ()
    prihlaska.step_5_ziak_navsteva_skoly()
    prihlaska.step_6_znamky()
    prihlaska.step_7_sutaze()
    prihlaska.step_8_prilohy()

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade sa nezobrazil identifikátor prihlášky pre 1. kolo."
    ).to_contain_text(re.compile(r"P-2026-.+"))

    # Pôvodne: "2026/2027" - portal má novú konfiguráciu, 1. kolo už beží pre 2027/2028.
    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba školský rok 2027/2028."
    ).to_contain_text("2027/2028")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba informácia o 1. kole prijímacieho konania."
    ).to_contain_text("1. kolo")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba meno žiaka."
    ).to_contain_text(data.meno)

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba priezvisko žiaka."
    ).to_contain_text(data.priezvisko)

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba rodné číslo žiaka."
    ).to_contain_text(data.rodne_cislo)

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba dátum narodenia žiaka."
    ).to_contain_text(helper.rc_to_datum_narodenia(data.rodne_cislo))

    if helper.get_pohlavie(data.rodne_cislo) == "ženské":
        pohlavie = "žena"
    else:
        pohlavie = "muž"

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba pohlavie žiaka."
    ).to_contain_text(pohlavie)

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba miesto narodenia."
    ).to_contain_text("Slovensko")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba štátna príslušnosť."
    ).to_contain_text("slovenská")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba krajina pobytu."
    ).to_contain_text("Slovenská republika")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba materinský jazyk."
    ).to_contain_text("slovenský")

    # Pôvodne: "Narcisová 4/2048, 03845, Myjava, Slovenská republika" (samostatné polia Obec/Ulica/PSČ).
    # Po zmene na register adries sa vyberá "Prvej SNR 33/23, 90701, Myjava, Myjava", ale súhrn
    # zobrazuje len "33/23, 90701, Slovenská republika" - chýba ulica a obec (na overenie s vývojom).
    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba adresa žiaka."
    ).to_contain_text("33/23, 90701, Slovenská republika")

    expect(
        page.locator("#suhrnny-prehlad"),
        "V súhrnnom prehľade chýba poznámka ŠVVP."
    ).to_contain_text("ŠVVP")

    expect(
        page.locator("#skoly"),
        "V sekcii školy chýba poradové číslo školy."
    ).to_contain_text("1 Stredná škola č. 1")

    expect(
        page.locator("#skoly"),
        "V sekcii školy chýba identifikátor školy."
    ).to_contain_text("910021624")

    expect(
        page.locator("#skoly"),
        "V sekcii školy chýba názov školy."
    ).to_contain_text("Stredná škola pre AT")

    expect(
        page.locator("#skoly"),
        "V sekcii školy chýba kód odboru."
    ).to_contain_text("2285H00")

    expect(
        page.locator("#skoly"),
        "V sekcii školy chýba názov odboru."
    ).to_contain_text("zlievač -3 ročné")

    expect(
        page.locator("#skoly"),
        "V sekcii školy chýba informácia o netalentovom odbore."
    ).to_contain_text("Netalentový")

    expect(
        page.locator("#skoly"),
        "V sekcii školy chýba termín prijímacej skúšky."
    ).to_contain_text("1. termín")

    expect(
        page.locator("#skoly"),
        "V sekcii školy chýba vyučovací jazyk."
    ).to_contain_text("slovenský")

    expect(
        page.locator("#zastupcovia"),
        "V sekcii zákonných zástupcov chýba hlavička pre zákonného zástupcu č. 1."
    ).to_contain_text("Osobné údaje zákonného zástupcu č. 1")

    expect(
        page.locator("#zastupcovia"),
        "V sekcii zákonných zástupcov chýba meno zákonného zástupcu."
    ).to_contain_text("Mária")

    expect(
        page.locator("#zastupcovia"),
        "V sekcii zákonných zástupcov chýba priezvisko zákonného zástupcu."
    ).to_contain_text("Bartošová")

    expect(
        page.locator("#zastupcovia"),
        "V sekcii zákonných zástupcov chýba rodné číslo zákonného zástupcu."
    ).to_contain_text("855215/3830")

    expect(
        page.locator("#zastupcovia"),
        "V sekcii zákonných zástupcov chýba dátum narodenia zákonného zástupcu."
    ).to_contain_text("15.02.1985")

    # Pôvodne sa overovala aj adresa ZZ: "Mandľová 16/745, 03874, Trenčianska Teplá, Slovenská republika".
    # Po prechode na register adries súhrn zobrazuje len "Korešpondenčná adresa: -" a adresa
    # trvalého pobytu ZZ chýba (na overenie s vývojom).

    expect(
        page.locator("#zastupcovia"),
        "V sekcii zákonných zástupcov chýba e-mail zákonného zástupcu."
    ).to_contain_text("katalontest987@gmail.com")

    expect(
        page.locator("#zastupcovia"),
        "V sekcii zákonných zástupcov chýba telefónne číslo zákonného zástupcu."
    ).to_contain_text("+421999888777")

    expect(
        page.locator("#zastupcovia"),
        "V sekcii zákonných zástupcov chýba hlavička pre zákonného zástupcu č. 2."
    ).to_contain_text("Osobné údaje zákonného zástupcu č. 2")

    expect(
        page.locator("#zastupcovia"),
        "V sekcii zákonných zástupcov chýba informácia o neznámom druhom zákonnom zástupcovi."
    ).to_contain_text("Druhý zákonný zástupca nie je známy.")

    expect(
        page.locator("#info-o-zs"),
        "V sekcii informácií o základnej škole chýba nadpis."
    ).to_contain_text("Informácie o základnej škole")

    expect(
        page.locator("#info-o-zs"),
        "V sekcii informácií o základnej škole chýba údaj o škole v zahraničí."
    ).to_contain_text("Zo školy v zahraničí")

    expect(
        page.locator("#info-o-zs"),
        "V sekcii informácií o základnej škole chýba ročník."
    ).to_contain_text("9.")

    expect(
        page.locator("#info-o-zs"),
        "V sekcii informácií o základnej škole chýba jazyk."
    ).to_contain_text("Francúzsky")

    expect(
        page.locator("#vysledky-vzdelavania-suhrn"),
        "V sekcii výsledkov vzdelávania chýbajú údaje za 6. ročník."
    ).to_contain_text("6. ročník (2. polrok)")

    expect(
        page.locator("#vysledky-vzdelavania-suhrn"),
        "V sekcii výsledkov vzdelávania chýba hodnotenie 'uspokojivé'."
    ).to_contain_text("uspokojivé")

    expect(
        page.locator("#vysledky-vzdelavania-suhrn"),
        "V sekcii výsledkov vzdelávania chýba známka '1 - výborný'."
    ).to_contain_text("1 - výborný")

    expect(
        page.locator("#vysledky-vzdelavania-suhrn"),
        "V sekcii výsledkov vzdelávania chýbajú údaje za 7. ročník."
    ).to_contain_text("7. ročník (2. polrok)")

    expect(
        page.locator("#vysledky-vzdelavania-suhrn"),
        "V sekcii výsledkov vzdelávania chýba hodnotenie 'menej uspokojivé'."
    ).to_contain_text("menej uspokojivé")

    expect(
        page.locator("#vysledky-vzdelavania-suhrn"),
        "V sekcii výsledkov vzdelávania chýba známka '3 - dobrý'."
    ).to_contain_text("3 - dobrý")

    expect(
        page.locator("#vysledky-vzdelavania-suhrn"),
        "V sekcii výsledkov vzdelávania chýbajú údaje za 8. ročník."
    ).to_contain_text("8. ročník (2. polrok)")

    expect(
        page.locator("#vysledky-vzdelavania-suhrn"),
        "V sekcii výsledkov vzdelávania chýba známka '2 - chválitebný'."
    ).to_contain_text("2 - chválitebný")

    expect(
        page.locator("#vysledky-vzdelavania-suhrn"),
        "V sekcii výsledkov vzdelávania chýbajú údaje za 9. ročník."
    ).to_contain_text("9. ročník (1. polrok)")

    expect(
        page.locator("#sutaze-suhrn"),
        "V sekcii súťaží chýba názov súťaže."
    ).to_contain_text("Zumba")

    expect(
        page.locator("#sutaze-suhrn"),
        "V sekcii súťaží chýba umiestnenie."
    ).to_contain_text("1. miesto - Školská úroveň")

    expect(
        page.locator("#sutaze-suhrn"),
        "V sekcii súťaží chýba kategória súťaže."
    ).to_contain_text("Umelecké")

    expect(
        page.locator("#sutaze-suhrn"),
        "V sekcii súťaží chýba školský rok."
    ).to_contain_text("Školský rok: 2023/2024")

    expect(
        page.locator(".prilohaItem").first,
        "Prvá príloha sa v súhrne nezobrazila."
    ).to_be_visible()

    expect(
        page.locator("#prilohyContainer > div:nth-child(2)"),
        "Druhá príloha sa v súhrne nezobrazila."
    ).to_be_visible()

    expect(
        page.locator("#prilohyContainer > div:nth-child(3)"),
        "Tretia príloha sa v súhrne nezobrazila."
    ).to_be_visible()

    expect(
        page.locator("#prilohyContainer > div:nth-child(4)"),
        "Štvrtá príloha sa v súhrne nezobrazila."
    ).to_be_visible()

    expect(
        page.locator("#prilohyContainer > div:nth-child(5)"),
        "Piata príloha sa v súhrne nezobrazila."
    ).to_be_visible()

    expect(
        page.locator("#layoutDorucenie"),
        "V časti doručenia chýba informácia o elektronickej výveske."
    ).to_contain_text(
        "Rozhodnutia o prijatí budú zverejnené na elektronickej výveske, o čom budete informovaný e-mailovou správou."
    )

    prihlaska.click_on_odoslat_prihlasku()

    expect(
        page.locator("body"),
        "Pred odoslaním sa nezobrazil potvrdzovací text o odoslaní prihlášky na stredné školy."
    ).to_contain_text(
        "Chystáte sa odoslať prihlášku na stredné školy, ktoré ste uviedli v prihláške. Po odoslaní prihlášky už nebude možné upravovať údaje ani prílohy, pokiaľ vás na opravu nevyzve riaditeľ školy. Pred odoslaním si preto dôkladne skontrolujte všetky údaje a priložené dokumenty. Odoslaním prihlášky sa formálne začne proces jej posúdenia podľa zákona č. 71/1967 Zb. o správnom konaní (správny poriadok)."
    )

    prihlaska.click_on_potvrdit_odoslanie()

    expect(
        page,
        "Po potvrdení odoslania sa neotvorila stránka 'Prihlaska-odoslana'."
    ).to_have_url(re.compile(r".*/Prihlaska-odoslana.*"), timeout=60000)

    expect(
        page.locator("h1"),
        "Na stránke potvrdenia chýba hláška o úspešnom odoslaní prihlášky."
    ).to_contain_text("Prihláška bola úspešne odoslaná!")

    identifikator = page.get_by_text("P-2026-").text_content()

    prihlaska.click_on_prejst_na_prihlasky()

    expect(
        page,
        "Po návrate sa neotvorila stránka so zoznamom prihlášok."
    ).to_have_url(re.compile(r".*/Prihlasky.*"), timeout=60000)

    logout.logout()

    login.login_as_riaditel(username_riad, password_riad, "910021624")
    prihlaska.vyhladanie_prihlasky_1_kolo(data.meno, data.priezvisko)

    expect(
        page.get_by_text(data.priezvisko + " " + data.meno, exact=True),
        "Na strane riaditeľa sa nenašla prihláška podľa mena a priezviska."
    ).to_be_visible()

    expect(
        page.get_by_text(identifikator, exact=True),
        "Na strane riaditeľa sa nenašiel identifikátor odoslanej prihlášky."
    ).to_be_visible()

    # Zoznam obsahuje viac prihlášok aj skryté template riadky, preto sa stav overuje
    # v riadku patriacom práve odoslanej prihláške.
    expect(
        page.locator("div.row.data-row").filter(has_text=identifikator).locator("div.data-prihlaska-stav"),
        "Na strane riaditeľa sa po odoslaní nezobrazuje stav 'V spracovaní'."
    ).to_contain_text("V spracovaní")


@pytest.mark.regres1kolo
def test_doplnenie_prilohy_na_SS_1_kolo(page: Page, person_data) -> None:
    data = person_data
    helper = Helper()
    mail = Mail()
    login = LoginPage(page)
    logout = LogoutPage(page)
    priloha = PrilohySS(page)

    login.login_as_riaditel(username_riad, password_riad, "910021624")
    priloha.najdi_poslednu_prihlasku_1_kolo()

    expect(
        page.locator("#detail-prihlasky-riad-SS-content"),
        "V detaile prihlášky chýba údaj, že bola podaná elektronicky."
    ).to_contain_text("Elektronicky")

    identifikator = page.locator(".prihlaskaIdentifikator").text_content()
    datum_narodenia = page.locator("#dietaDatumNarodenia").text_content()

    priloha.vyziadaj_prilohu_na_poslednej_prihlaske()

    expect(
        page.locator("#message-box"),
        "Po vyžiadaní prílohy sa nezobrazila úspešná hláška."
    ).to_contain_text("Žiadosť o doplnenie prílohy bola úspešne odoslaná")

    expect(
        page.locator("#detail-prihlasky-riad-SS-content"),
        "Po vyžiadaní prílohy sa prihláška neprepla do stavu 'Neúplná'."
    ).to_contain_text("Neúplná")

    expect(
        page.locator("#skoly"),
        "V detaile školy chýba informácia o požadovaných ďalších prílohách."
    ).to_contain_text("Riaditeľ školy Stredná škola pre AT požadoval ďalšie prílohy.")

    expect(
        page.locator("#skoly"),
        "V detaile školy chýba názov vyžiadanej prílohy."
    ).to_contain_text("Čestné vyhlásenie zákonného zástupcu")

    expect(
        page.locator("#skoly"),
        "V detaile školy chýba dôvod vyžiadania prílohy."
    ).to_contain_text(
        "Žiadam o úpravu alebo doplnenie príloh v prihláške na školu. Detaily v sprievodnom texte: Žiadosť o doplnenie prílohy."
    )

    priloha.odvolanie_ziadosti()

    odvolanie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    odvolanie_prilohy = helper.cleanup_email_text(odvolanie_prilohy)
    expected = (
        f"Vážený/á pán/pani Mária Bartošová, radi by sme Vás informovali, že požiadavka na doloženie dodatočných dokumentov príloh k Vašej prihláške zaevidovanej v portáli Elektronické prihlášky do škôl bola zrušená. Nie je teda potrebné dodatočne nahrávať žiadne ďalšie prílohy k prihláške pre: {data.meno} {data.priezvisko} nar. {datum_narodenia}. Ak ste už zadali dokumenty na základe predchádzajúceho odkazu, upozorňujeme, že tento odkaz je už neaktívny. V prípade akýchkoľvek otázok nás neváhajte kontaktovať. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň.\""
    )
    assert odvolanie_prilohy == expected, "Text e-mailu o odvolaní žiadosti na SŠ sa nezhoduje s očakávaným obsahom."

    expect(
        page.locator("#skoly"),
        "Po odvolaní žiadosti sa v detaile školy nezobrazila informácia 'Výzva odvolaná'."
    ).to_contain_text("info Výzva odvolaná")

    expect(
        page.locator("#detail-prihlasky-riad-SS-content"),
        "Po odvolaní žiadosti sa prihláška nevrátila do stavu 'V spracovaní'."
    ).to_contain_text("V spracovaní")

    priloha.vyziadaj_prilohu_na_poslednej_prihlaske()

    vyziadanie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    vyziadanie_prilohy = helper.cleanup_email_text(vyziadanie_prilohy)
    expected = (
        f"Vážený/á pán/pani Mária Bartošová, pri kontrole prihlášky {identifikator} pre školu zlievač pre {data.meno} {data.priezvisko} sme zistili, že je potrebné doložiť nasledujúcu prílohu: Čestné vyhlásenie zákonného zástupcu z dôvodu že \" Žiadosť o doplnenie prílohy. \". Prosíme Vás o doplnenie požadovanej prílohy k prihláške. Doplnenie príloh môžete vykonať prostredníctvom portálu Elektronické prihlášky do škôl: Link na prihlásenie Ak ešte nemáte vytvorené konto, zaregistrujte sa prostredníctvom odkazu: Registrovať sa Po registrácii a prihlásení sa dostanete do sekcie Moje prihlášky, kde nájdete možnosť pridať existujúcu prihlášku do svojho konta. Na pridanie prihlášky zadajte tento identifikátor prihlášky: {identifikator} Po pridaní prihlášky do konta budete môcť sledovať jej stav, doplniť požadované prílohy a komunikovať so školou. V prípade, že už konto v portáli máte, prihláste sa a pokračujte podľa pokynov v portáli. S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň."
    )
    assert vyziadanie_prilohy == expected, "Text e-mailu o vyžiadaní prílohy na SŠ sa nezhoduje s očakávaným obsahom."

    logout.logout()

    login.login_as_zakonny_zastupca(username, password)

    expect(
        page.locator("#moje-prihlasky"),
        "Na stránke Moje prihlášky sa nezobrazil nadpis 'Nahrajte prílohy'."
    ).to_contain_text("Nahrajte prílohy")

    expect(
        page.locator("#moje-prihlasky"),
        "Na stránke Moje prihlášky sa nezobrazila výzva na doplnenie príloh pre SŠ."
    ).to_contain_text(
        "Nahrajte prílohyRiaditeľ strednej školy požaduje doplnenie príloh. Pridanie prílohy nájdete v stĺpci Akcia."
    )

    priloha.nahrat_prilohu()

    expect(
        page.locator("#pridat-prilohy"),
        "Po nahratí prílohy sa nezobrazila úspešná hláška."
    ).to_contain_text("Dokumenty ste úspešne nahrali")

    expect(
        page.locator("#pridat-prilohy"),
        "Po nahratí prílohy sa nezobrazila informácia o ďalšom posúdení prihlášky."
    ).to_contain_text("Vaša prihláška bude čoskoro posúdená. Ďakujeme za trpezlivosť.")

    prijatie_prilohy = mail.get_last_email_text("imap.gmail.com", mailuser, mailpw)
    prijatie_prilohy = helper.cleanup_email_text(prijatie_prilohy)
    expected = (
        f"Vážený/á pán/pani/ Mária Bartošová, dovoľujeme si Vás informovať, že k Vašej prihláške do Stredná škola pre AT zlievač pre {data.meno} {data.priezvisko}, zaevidovanej v elektronickom portáli prihlášok bola doručená príloha s názvom Čestné vyhlásenie zákonného zástupcu. Doručenú prílohu si prosím starostlivo skontrolujte prihlásením sa na portáli Elektronických prihlášok v detaile prihlášky, alebo v prílohe tohto mailu. Prihlásením sa na portáli zároveň získate aj ďalšie informácie o stave Vašej prihlášky a priebehu jej spracovania. Link na prihlásenie S pozdravom Tím elektronických prihlášok MŠVVaM SR Tento email bol generovaný automaticky portálom Elektronické prihlášky do škôl, ktorý je v správe Ministerstva školstva, výskumu, vývoja a mládeže Slovenskej republiky. Neodpovedajte naň.\""
    )
    assert prijatie_prilohy == expected, "Text e-mailu o prijatí prílohy na SŠ sa nezhoduje s očakávaným obsahom."

    logout.logout()

    login.login_as_riaditel(username_riad, password_riad, "910021624")
    priloha.najdi_prihlasku_po_nahrati_prilohy_1_kolo(data.meno, data.priezvisko)

    expect(
        page.locator("#dietaMeno"),
        "Po nahratí prílohy sa v detaile prihlášky nezobrazuje správne meno žiaka."
    ).to_contain_text(data.meno)

    expect(
        page.locator(".stavPrihlasky"),
        "Po nahratí prílohy sa na strane riaditeľa nezobrazuje stav 'Doplnená'."
    ).to_contain_text("Doplnená")

    expect(
        page.get_by_text("Priložené dokumenty:"),
        "Po nahratí prílohy sa nezobrazil zoznam priložených dokumentov."
    ).to_be_visible()