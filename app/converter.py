"""Exchange rates and conversion logic.

All rates are relative to USD as the base currency.
Static table — no external API calls required.
"""

from __future__ import annotations

# Base: 1 USD = X of the target currency
_RATES: dict[str, float] = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "INR": 83.52,
    "JPY": 157.30,
    "AUD": 1.54,
    "CAD": 1.37,
    "CHF": 0.90,
    "CNY": 7.24,
    "SGD": 1.35,
    "MXN": 17.15,
    "BRL": 5.08,
    "KRW": 1350.00,
    "HKD": 7.82,
    "SEK": 10.42,
    "NOK": 10.55,
    "DKK": 6.88,
    "NZD": 1.64,
    "ZAR": 18.63,
    "AED": 3.67,
}

_NAMES: dict[str, str] = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "INR": "Indian Rupee",
    "JPY": "Japanese Yen",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "SGD": "Singapore Dollar",
    "MXN": "Mexican Peso",
    "BRL": "Brazilian Real",
    "KRW": "South Korean Won",
    "HKD": "Hong Kong Dollar",
    "SEK": "Swedish Krona",
    "NOK": "Norwegian Krone",
    "DKK": "Danish Krone",
    "NZD": "New Zealand Dollar",
    "ZAR": "South African Rand",
    "AED": "UAE Dirham",
}


def supported_currencies() -> dict[str, str]:
    """Return mapping of currency code → full name."""
    return dict(_NAMES)


def convert(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert amount from one currency to another via USD as base."""
    fc = from_currency.upper()
    tc = to_currency.upper()
    if fc not in _RATES:
        raise ValueError(f"Unsupported currency: {fc!r}")
    if tc not in _RATES:
        raise ValueError(f"Unsupported currency: {tc!r}")
    # Convert to USD first, then to target
    in_usd = amount / _RATES[fc]
    return round(in_usd * _RATES[tc], 6)
