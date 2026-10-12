# Stav regresnej sady a poznámky k portálu

Posledná aktualizácia: 12. 10. 2026

Tento súbor slúži na prenos kontextu medzi strojmi a medzi sedeniami.
Obsahuje stav testov, otvorené chyby portálu a overené postupy, ktoré sa
pri práci s `test-eprihlasky.iedu.sk` opakovane osvedčili.

---

## 1. Stav sady

Spolu **56 testov**.

| Kategória | Počet |
|---|---|
| Prechádzajúce | 24 |
| Zlyháva na chybe portálu | 1 |
| Blokované | 21 |
| Nikdy nespúšťané | 10 |

### Prechádzajúce (overené 8. 10. 2026)

| Test | Počet |
|---|---|
| `tests/ZZ/Prihlaska na SS 1 kolo.py` | 2 |
| `tests/ZZ/Prihlaska na ZS.py` | 2 |
| `tests/ZZ/Prihlaska na MS.py` | 2 |
| `tests/ZZ/Zmena udajov v profile IFO osoby.py` | 1 |
| `tests/ZZ/Registracia.py` | 1 |
| `tests/Riaditel/Zmena udajov v profile.py` | 1 |
| `tests/Riaditel/Zmena skoly v profile.py` | 1 |
| `tests/Riaditel/Sprava skoly - Profil skoly MS\|SS\|ZS.py` | 3 |
| `tests/Riaditel/SpravaPouzivatelov/...::test_odstran_rolu` | 1 |
| `tests/Riaditel/Odbory.py::test_pridanie_a_vymazanie_odboru_1_kolo` | 1 |
| `tests/Riaditel/Prijimacky 1 kolo.py` | 6 |
| `tests/VerejnaZona/Kontrola skol.py` | 3 |

### Nikdy nespúšťané — nič ich neblokuje (10)

- `tests/Riaditel/Rozhodnutie MS|SS|ZS.py` — 6 testov
- `tests/ZZ/Vyveska MS|SS|ZS.py` — 3 testy
- `tests/Riaditel/Spravne konanie.py` — 1 test

Žiadny z nich nevytvára papierovú prihlášku (overené cez importy), pracujú
s už existujúcimi prihláškami. **Toto je najlepší ďalší krok.**

---

## 2. Otvorené chyby portálu

### Rola Administrátor končí chybou 401

`SpravaPouzivatelov/Pridat a odstranit pouzivatela.py::test_pridaj_rolu`

Účet s rolou **Administrátor** sa prihlási, dostane sa do `/Riaditel`
a portál ho okamžite odhlási cez SAML logout:

```
NAV tiamidsk.iedu.sk/saml2/authn/final   ← overenie OK
NAV test-eprihlasky.iedu.sk/Riaditel     ← dostal sa dnu
NAV tiamidsk.iedu.sk/saml2/logout?...    ← portal ho sam odhlasi
→ /Error?code=401&corrid=3e7e5230-5df9-422c-92b0-7d6c68dba179
```

Reprodukované 4×. Rola **Spracovateľ funguje** bez problémov.

Súvisiace, menšie: **rola sa neprejaví okamžite.** Hneď po priradení portál
používateľa odhlási, o pár minút už prihlásenie prejde (09:05 odhlásený,
09:12 OK). Test priraďuje rolu a vzápätí sa tým účtom prihlasuje — súbeh.
Riešenie zatiaľ neimplementované.

### Odosielanie prihlášok na MŠ a ZŠ je nestabilné

Posledný krok sprievodcu občas skončí červeným bannerom **„Došlo k chybe pri
komunikácii so serverom."**, URL zostane na `/Prihlaska?typSaSZ=...`.
SŠ funguje vždy.

- 7. 10.: MŠ aj ZŠ padli opakovane
- 8. 10.: obe prešli

Nie je to chyba testov — sprievodca prejde a súhrn je správny. Nie je to ani
dátum prijatia pri MŠ (po oprave na budúci dátum chyba pretrvávala a ZŠ také
pole vôbec nemá).

### Papierové prihlášky — prebieha vývoj

Zatiaľ nespúšťať. Dotknuté (overené cez import `pages.papierova_prihlaska_*`):

- `tests/Riaditel/Papierova prihlaska na MS|SS 1 kolo|SS 2 kolo|ZS.py`
- `tests/Riaditel/ZS - Papierova prihlaska na SS.py`
- `tests/ZZ/Konflikt MS.py`, `Konflikt SS 1 kolo.py`, `Konflikt SS 2 kolo.py`

**Pozor na falošnú zhodu:** `tests/ZZ/Prihlaska na ZS.py` tiež importuje
`PapierovaPrihlaskaZS`, ale prihlášku nevytvára — volá len `najdi_prihlasku()`
a `click_on_zobrazit_prihlasku()`. Nie je dotknutý a ostáva zelený.

### Druhé kolo — odložené

Portál je konfiguračne v 1. kole, preto testy 2. kola zatiaľ nespúšťať.
Lokátory v nich sú opravené, len neoverené behom.

`tests/ZZ/Prihlaska na SS 2 kolo.py:70` má stále starú skrátenú adresu
`"33/23, 90701, Slovenská republika"` — po odblokovaní opraviť na plnú.

---

## 3. Overené zmeny portálu a vzory lokátorov

Tieto sa opakovane osvedčili, oplatí sa ich skúsiť ako prvé.

1. **Hviezdička `*` v labeloch má `aria-hidden="true"`**, takže
   `get_by_role(..., name="X *")` nenájde nič. Labely majú navyše „povinné".
   → používať ID polí.
   **Neplatí to plošne** — niektoré formuláre s hviezdičkou stále fungujú.
   Každý výskyt treba overiť behom testu, nie hromadne nahrádzať.

2. **Modály sú v kontajneroch s `aria-hidden="true"`** → role lokátory vrátia
   0 prvkov. Používať ID:
   `#modalVytvoritPrihlaskuRadio_option_{0=MŠ, 1=ZŠ, 2=SŠ}`,
   `button.btn-pridat.govuk-button:visible`.

3. **Autocomplete polia zmenili ARIA rolu z `textbox` na `combobox`.**
   Neoverené výskyty: `prihlaska_MS_page.py:168`, `prihlaska_ZS_page.py:153`,
   `verejna_zona_page.py:25`, `papierova_prihlaska_ZSSS_page.py:134`.

4. **Profilové menu**: spúšťač je na strane ZZ `<button>`, na riaditeľskej
   `<a>`. Role lokátor nepokryje obe → používať `page.locator(".profil-dropdown")`.

5. **Hodnoty v detaile sú `<dd>`.** Na SŠ majú ID aj triedu, na MŠ a ZŠ len
   triedu → používať triedny selektor (`.prihlaskaIdentifikator`, `.stavPrihlasky`).

6. **Skryté template riadky zmizli** → `get_by_role("button", name="Zobraziť").nth(1)`
   otvára nesprávny riadok, správne je `.first`.

7. **Register adries** nahradil polia Obec/Ulica/PSČ v sprievodcoch SŠ, ZŠ a MŠ
   (`#adresaTPKrajina` → `#adresaTPAdresaRA`). Profil a papierová prihláška
   register **nepoužívajú**, majú stále pôvodné polia.

8. **Pribudol chatbot EDO** (widget vpravo dole). Zatiaľ nič nerozbil, ale je to
   ďalší prvok, ktorý môže prekrývať kliky — objavuje sa v stromoch prístupnosti
   pri chybách.

### Vlastné checkboxy

Reálny `<input>` býva skrytý, kliká sa na `span.checkmark`. Bez `:visible`
vracia selektor aj desiatky skrytých prvkov:

```python
page.locator("div.vybrate-wrapper:visible .checkmark").first
```

### Odbory — rozbaľovacia ponuka v riadku

„Upraviť" a „Odstrániť" nie sú priame tlačidlá, ale `.btn-edit` / `.btn-delete`
v ponuke `.odbor-akcie-button`. Dve veci sú nutné:

- bez `scroll_into_view_if_needed()` sa ponuka vôbec neotvorí
- zoznam sa po uložení prekresľuje a otvorenú ponuku zatvorí, preto musí byť
  otvorenie ponuky a klik na položku v jednom opakovanom kroku
  (`_klikni_akciu_odboru`)

`#btnPridatOdbor` je tlačidlo prázdneho stavu. Keď odbory existujú, zobrazuje sa
`#odbory-list-btn-pridat-odbor`. Padnutý beh necháva odbor v škole `910021685`.

---

## 4. Ponaučenia

**Keď test padá zakaždým inde, hľadať spoločnú príčinu.** Pri odboroch viedlo
postupné opravovanie „kroku, kde to práve padlo" k výsledkom 0 z 3 → 2 zo 4 →
6 zo 6. Skutočné príčiny boli dve systémové veci (prekresľovanie zoznamu a
spinner počas dohľadávania IČO), nie jednotlivé kroky.

**Nepovažovať nestabilitu automaticky za chybu portálu.** Spinner pri IČO som
od septembra viedol ako chybu portálu. V skutočnosti to bol súbeh v teste —
spinner trvá pár sekúnd a test doň narazil ďalším krokom. Odhalilo sa to až
ručným overením.

**Pri vizuálnych porovnaniach PDF maskovať celé dynamické oblasti.** Dĺžka mena
žiaka mení počet riadkov odseku a tým posúva všetok text pod ním vrátane podpisu.
Pevné malé masky to nedokážu absorbovať. Overenie masky na jedinej dvojici PDF
nestačí — treba dvojicu s rôznym počtom riadkov.

**Overiť každé tvrdenie v DOM pred úpravou.** Niekoľkokrát sa stalo, že
„zrejmá" príčina bola nesprávna.

---

## 5. Prostredie a príkazy

Python **3.14**, závislosti zafixované v `requirements.txt`.

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install
```

Spustenie testu:

```powershell
.\.venv\Scripts\python.exe -m pytest "<subor>" -p no:randomly --no-header -q
```

Mimo gitu, treba preniesť ručne: **`.env`** (zoznam premenných je v `README.md`)
a **`AGENTS.md`**. Voliteľne `playwright/.auth/`, dá sa vygenerovať znova.

### Na čo si dať pozor po prenose na iný stroj

Vizuálne snapshoty verejnej zóny (`tests/VerejnaZona/__snapshots__/chromium/win32/`)
sa porovnávajú po pixeloch. Na inom stroji sa môže líšiť vykresľovanie písma a
testy `Kontrola skol` môžu padnúť, aj keď je všetko v poriadku. Vtedy:

```powershell
.\.venv\Scripts\python.exe -m pytest "tests/VerejnaZona/Kontrola skol.py" --update-snapshots -p no:randomly
```

Snapshot sníma celú stránku vrátane **živého počtu podaných prihlášok**, ktorý
rastie po každom našom teste. Ak pribudne alebo ubudne škola, zmení sa výška
stránky a kontrola rozmeru zlyhá ešte pred porovnaním pixelov.

Commit správy píšeme cez `git commit -F <subor>` — here-string (`@"..."@`)
v tomto termináli commit zasekne.

---

## 6. Vyriešené, ponechané pre kontext

- **Registrácia**: `api.mail.tm` je z tejto siete nedostupné (TLS handshake sa
  nedokončí, web `mail.tm` pritom funguje). Nahradené jednorazovými Gmail
  plus-aliasmi do existujúcej schránky — `GmailAliasClient` v
  `utils/api_register.py`. Hlavičky `To` / `Delivered-To` / `X-Original-To`
  kontrolujeme v Pythone, pretože vyhľadávanie Gmailu s plus-aliasmi nie je
  spoľahlivé.
  Pozor: portál posiela HTML aj v textovej časti e-mailu, takže na odkaz treba
  `https?://[^\s"'<>]+`. Pôvodné `\S+` vytiahlo aj `>odkaz</a></b` a aktivácia
  nikdy neprebehla. **Tá istá chyba je stále v nepoužívanom `MailTmClient`.**
  Pozorované aj to, že portál občas potvrdzovací e-mail vôbec neodošle
  (1 z 5 behov, ani v spame).
- **Súpisné číslo v profile ZZ** — opravené vývojom, zobrazuje sa `Záštepy 32/98`.
- **Prihlásenie riaditeľa `code=10015`** — opravené vývojom.
- **Vyhľadávanie škôl** — opravené vývojom.
