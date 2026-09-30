# ePrihlášky – Playwright Test Suite

End-to-end regression tests for the [ePrihlášky](https://test-eprihlasky.iedu.sk/) portal built with [Playwright](https://playwright.dev/python/) and [pytest](https://docs.pytest.org/).

---

## Project Structure

```
tests/
├── Riaditel/               # Tests for the Riaditeľ (principal) role
│   ├── SpravaPouzivatelov/ # User management
│   └── ...                 # Rozhodnutia, Prijímačky, Odbory, Správa školy,
│                           # Papierové prihlášky, Správne konanie, Profil
├── VerejnaZona/            # Tests for the public zone (Kontrola škôl)
│   └── __snapshots__/      # Reference screenshots for visual tests
└── ZZ/                     # Tests for the Zákonný zástupca (guardian) role
pages/                      # Page Object Model classes
utils/                      # api_register, data_helper, helpers,
                            # mail_helper, pdf_helper
data/                       # Test data files and reference PDFs
playwright/.auth/           # Saved storage state (used by --role)
reports/                    # HTML report, screenshots, visual and PDF diffs
allure-results/             # Raw Allure results
conftest.py                 # Shared fixtures, browser config, base URL setup
```

> Shared fixtures live in `conftest.py`. The `fixtures/` directory is currently empty.

---

## Requirements

- Python 3.10+ (currently developed and run on 3.14)
- [Playwright](https://playwright.dev/python/) browsers installed

Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

---

## Environment Variables

Create a `.env` file in the project root (or set variables in CI):

| Variable | Description |
|---|---|
| `EPRIHLASKY_RIADITEL_USERNAME` | Riaditeľ account username |
| `EPRIHLASKY_RIADITEL_PASSWORD` | Riaditeľ account password |
| `EPRIHLASKY_SEC_RIADITEL_USERNAME` | Secondary riaditeľ username |
| `EPRIHLASKY_SEC_RIADITEL_PASSWORD` | Secondary riaditeľ password |
| `EPRIHLASKY_ZZ_USERNAME` | Zákonný zástupca username |
| `EPRIHLASKY_ZZ_PASSWORD` | Zákonný zástupca password |
| `EPRIHLASKY_LOCAL_URL` | Local environment URL (default: `http://localhost:3000`) |
| `EPRIHLASKY_TEST_URL` | Test environment URL (default: `https://test-eprihlasky.iedu.sk/`) |
| `EPRIHLASKY_STAGE_URL` | Stage environment URL |
| `EPRIHLASKY_PROD_URL` | Production environment URL |
| `GMAIL_USERNAME` | Gmail address for email verification |
| `GMAIL_APP_PASSWORD` | Gmail app password |
| `GMAIL_SEC_USERNAME` | Secondary Gmail address |
| `GMAIL_SEC_APP_PASSWORD` | Secondary Gmail app password |

---

## Running Tests

**Run all tests:**
```bash
pytest
```

**Run a specific test suite by marker:**
```bash
pytest -m regres1kolo
pytest -m regres2kolo
```

**Run a single test:**
```bash
pytest "tests\ZZ\Prihlaska na MS.py::test_prihlaska_na_MS"
```

**Run headed (visible browser):**
```bash
pytest --headed
```

---

## Command Line Options

| Option | Values | Description |
|---|---|---|
| `--env` | `local`, `test`, `stage`, `prod` | Target environment (default: `test`). The URL is read from the matching environment variable. |
| `--role` | `none`, `zz`, `riaditel` | Loads saved storage state from `playwright/.auth/` (default: `none`). The file is only used if it exists. |
| `--update-snapshots` | – | Overwrites reference screenshots used by the `visual_snapshot` fixture. |

```bash
pytest --env stage
pytest -m regres1kolo --update-snapshots
```

> The base URL is resolved from `--env` by a fixture in `conftest.py`, so `--base-url` has no effect.

---

## Test Markers

Markers are declared in `pytest.ini`. `--strict-markers` is enabled, so an unregistered marker fails the run.

| Marker | Description |
|---|---|
| `regres1kolo` | Regression suite for 1st admission round |
| `regres2kolo` | Regression suite for 2nd admission round |
| `spravaSkoly` | School profile management tests |
| `profil` | Principal / user profile tests |
| `prihlaskaRiaditel` | Paper applications created by the principal |
| `smoke` | Smoke tests |
| `regression` | Regression tests |
| `ui` | UI tests |
| `slow` | Slow running tests |
| `retest` | Debugging only |

---

## Reports

After a test run, reports are available at:

- **HTML report:** `reports/report.html`
- **Allure results:** `allure-results/`
- **Failure screenshots:** `reports/screenshots/`
- **Visual snapshot diffs:** `reports/visual-diffs/`
- **PDF comparison diffs:** `reports/pdf-visual-diffs/`, `reports/pdf-text-diffs/`

To generate and open an Allure report:
```bash
allure serve allure-results
```

---

## CI/CD

Tests are executed via Jenkins. The pipeline supports:

- **`suite` mode** – runs all tests matching a marker (`regres1kolo` / `regres2kolo`)
- **`single` mode** – runs one test by node ID or `-k` expression

Credentials are injected as Jenkins credentials and are never stored in the repository.
