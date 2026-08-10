# ePrihlášky – Playwright Test Suite

End-to-end regression tests for the [ePrihlášky](https://test-eprihlasky.iedu.sk/) portal built with [Playwright](https://playwright.dev/python/) and [pytest](https://docs.pytest.org/).

---

## Project Structure

```
tests/
├── Riaditel/               # Tests for the Riaditeľ (principal) role
│   ├── SpravaPouzivatelov/ # User management
│   └── ...                 # Rozhodnutia, Prijímačky, Správa školy, Odbory, Profil
├── VerejnaZona/            # Tests for the public zone (Kontrola škôl)
└── ZZ/                     # Tests for the Zákonný zástupca (guardian) role
pages/                      # Page Object Model classes
fixtures/                   # Shared test fixtures
utils/                      # Helper utilities
data/                       # Test data files
conftest.py                 # Session fixtures, browser config, base URL setup
```

---

## Requirements

- Python 3.10+
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
| `EPRIHLASKY_TEST_URL` | Test environment URL (default: `https://test-eprihlasky.iedu.sk/`) |
| `EPRIHLASKY_LOCAL_URL` | Local environment URL (default: `http://localhost:3000`) |
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

**Run against a specific URL:**
```bash
pytest --env test --base-url https://test-eprihlasky.iedu.sk/
```

---

## Test Markers

| Marker | Description |
|---|---|
| `regres1kolo` | Regression suite for 1st admission round |
| `regres2kolo` | Regression suite for 2nd admission round |
| `spravaSkoly` | School profile management tests |

---

## Reports

After a test run, reports are available at:

- **HTML report:** `reports/report.html`
- **Allure results:** `allure-results/`

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
