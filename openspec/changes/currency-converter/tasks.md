## 1. Project Scaffold

- [x] 1.1 Create `pyproject.toml` with FastAPI, Uvicorn, Pydantic dependencies
- [x] 1.2 Create `.gitignore` for Python / venv artifacts
- [x] 1.3 Create `app/__init__.py` package marker

## 2. Rate Table & Conversion Logic

- [x] 2.1 Create `app/converter.py` with `_RATES` dict (20 currencies, USD base)
- [x] 2.2 Create `app/converter.py::supported_currencies()` returning code → name mapping
- [x] 2.3 Create `app/converter.py::convert(amount, from_currency, to_currency)` with USD triangulation and ValueError on unknown codes

## 3. Pydantic Models

- [x] 3.1 Create `app/models.py::ConversionResult` with fields: `from_currency`, `to_currency`, `amount`, `converted`, `rate`
- [x] 3.2 Create `app/models.py::CurrencyInfo` with fields: `code`, `name`

## 4. FastAPI HTTP Layer

- [x] 4.1 Create `app/main.py` with FastAPI app instance
- [x] 4.2 Add `GET /health` → `{"status": "ok"}`
- [x] 4.3 Add `GET /currencies` → list of `CurrencyInfo`, sourced from `supported_currencies()`
- [x] 4.4 Add `GET /convert?from_currency&to_currency&amount` → `ConversionResult`; raise HTTP 400 on ValueError, rely on Pydantic for 422 on invalid amount
- [x] 4.5 Add `GET /` HTML landing page with endpoint list and currency table

## 5. Verification

- [ ] 5.1 Run `uvicorn app.main:app --reload --port 8000` and confirm `/health` returns `{"status":"ok"}`
- [ ] 5.2 Test `GET /convert?from_currency=USD&to_currency=INR&amount=100` returns positive converted value
- [ ] 5.3 Test `GET /convert?from_currency=XYZ&to_currency=USD&amount=10` returns HTTP 400
- [ ] 5.4 Test `GET /currencies` returns at least 20 items including `{"code":"USD","name":"US Dollar"}`
