# 💱 Currency Converter

A fast, offline-capable currency converter built with **FastAPI + Pydantic**.  
20 currencies · Zero external API calls · Fully deterministic.

> **Live UI →** [saishyam1.github.io/openspec_try](https://saishyam1.github.io/openspec_try)  
> **Repo →** [github.com/saishyam1/openspec_try](https://github.com/saishyam1/openspec_try)

---

## Branches

| Branch | Approach | Description |
|---|---|---|
| `vibe_coded_submission` | 🎯 Vibe Coding | Built fast and iteratively — scaffold → logic → endpoints → history → popular pairs |
| `sdd_submission` | 📐 Spec-Driven Dev | Built with OpenSpec — proposal → design → specs → tasks → implementation |

---

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000** in your browser.

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | HTML landing page |
| `GET` | `/health` | `{"status": "ok"}` |
| `GET` | `/currencies` | All 20 supported currencies |
| `GET` | `/convert` | Convert between any two currencies |
| `GET` | `/history` | Last 50 conversions this session |
| `GET` | `/popular` | Top 5 most-used currency pairs |
| `GET` | `/docs` | Swagger UI |

### `/convert` query params

| Param | Type | Required | Description |
|---|---|---|---|
| `from_currency` | string | ✓ | Source currency code e.g. `USD` |
| `to_currency` | string | ✓ | Target currency code e.g. `INR` |
| `amount` | float > 0 | ✓ | Amount to convert |

### Example

```bash
curl "http://localhost:8000/convert?from_currency=USD&to_currency=INR&amount=100"
```

```json
{
  "from_currency": "USD",
  "to_currency": "INR",
  "amount": 100.0,
  "converted": 8352.0,
  "rate": 83.52
}
```

---

## Supported Currencies

`USD` `EUR` `GBP` `INR` `JPY` `AUD` `CAD` `CHF` `CNY` `SGD`  
`MXN` `BRL` `KRW` `HKD` `SEK` `NOK` `DKK` `NZD` `ZAR` `AED`

---

## Project Layout

```
app/
├── __init__.py
├── converter.py   # Rate table + conversion logic
├── history.py     # In-memory session history
├── models.py      # Pydantic response models
└── main.py        # FastAPI HTTP layer
docs/
└── index.html     # GitHub Pages standalone UI
pyproject.toml
```

---

Built by **Sai Shyam** · Spec-Driven Development Workshop
