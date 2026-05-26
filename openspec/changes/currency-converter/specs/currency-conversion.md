## ADDED Requirements

### Requirement: Convert currency amount

Given a valid source currency, target currency, and positive amount, the API returns the converted value and effective rate.

#### Scenario: Successful conversion USD to INR
- **WHEN** `GET /convert?from_currency=USD&to_currency=INR&amount=100`
- **THEN** response is HTTP 200 with `from_currency=USD`, `to_currency=INR`, `amount=100.0`, `converted` is a positive float, `rate` is a positive float

#### Scenario: Same currency conversion
- **WHEN** `GET /convert?from_currency=EUR&to_currency=EUR&amount=50`
- **THEN** `converted == 50.0` and `rate == 1.0`

#### Scenario: Unknown source currency
- **WHEN** `GET /convert?from_currency=XYZ&to_currency=USD&amount=10`
- **THEN** HTTP 400 with detail containing `"XYZ"`

#### Scenario: Unknown target currency
- **WHEN** `GET /convert?from_currency=USD&to_currency=AAA&amount=10`
- **THEN** HTTP 400 with detail containing `"AAA"`

#### Scenario: Zero amount rejected
- **WHEN** `GET /convert?from_currency=USD&to_currency=EUR&amount=0`
- **THEN** HTTP 422 (validation error — amount must be > 0)

#### Scenario: Negative amount rejected
- **WHEN** `GET /convert?from_currency=USD&to_currency=EUR&amount=-5`
- **THEN** HTTP 422 (validation error — amount must be > 0)

---

### Requirement: List supported currencies

The API exposes a stable list of all currency codes with their full English names.

#### Scenario: List all currencies
- **WHEN** `GET /currencies`
- **THEN** HTTP 200 with a JSON array; each item has `code` (3-letter string) and `name` (non-empty string); at least 20 items returned

#### Scenario: USD always present
- **WHEN** `GET /currencies`
- **THEN** one item has `code == "USD"` and `name == "US Dollar"`

---

### Requirement: Health check

#### Scenario: Health endpoint returns ok
- **WHEN** `GET /health`
- **THEN** HTTP 200 with `{"status": "ok"}`
