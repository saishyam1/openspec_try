## Why

Users working with international data — prices, invoices, salaries — need a reliable way to convert amounts between currencies without relying on external services. A self-contained, spec-driven currency converter API provides a predictable, testable solution with no rate-limit or network dependency concerns.

## What Changes

A new FastAPI microservice is built from scratch providing:
- Currency conversion via a static, deterministic exchange rate table
- A listing endpoint to discover supported currencies
- A clean HTML landing page with live examples

The implementation follows a strict spec-driven approach: proposal → specs → design → tasks → implementation.

## Capabilities

### New Capabilities

- `currency-conversion`: Accept a source currency, target currency, and positive amount; return the converted value, the effective rate, and metadata. Validate unknown currency codes with a clear 400 error.
- `currency-listing`: Return all supported currency codes with their full English names, suitable for populating a UI dropdown.

### Modified Capabilities

<!-- none — this is a greenfield service -->

## Impact

- New package: `app/` with `converter.py`, `models.py`, `main.py`, `__init__.py`
- New config: `pyproject.toml`, `.gitignore`
- No database required — rates stored in a static in-memory dict
- No external API calls — fully deterministic and offline-capable
