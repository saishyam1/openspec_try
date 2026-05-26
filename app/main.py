"""FastAPI app — Currency Converter."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

from app.converter import convert, supported_currencies
from app.models import ConversionResult, CurrencyInfo

app = FastAPI(title="Currency Converter API", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def landing() -> HTMLResponse:
    currencies = supported_currencies()
    rows = "".join(
        f"<tr><td><strong>{code}</strong></td><td>{name}</td></tr>"
        for code, name in currencies.items()
    )
    return HTMLResponse(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Currency Converter</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; background: #f8fafc; color: #1e293b; }}
    h1 {{ color: #0f172a; }} h2 {{ color: #1e40af; margin-top: 2rem; }}
    .badge {{ background: #dbeafe; color: #1d4ed8; padding: .3rem .75rem; border-radius: 999px; font-size: .9rem; font-weight: 600; }}
    code {{ background: #f1f5f9; padding: .15rem .4rem; border-radius: 4px; font-size: .9rem; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: .75rem; }}
    th, td {{ text-align: left; padding: .5rem .75rem; border-bottom: 1px solid #e2e8f0; }}
    th {{ background: #e2e8f0; }}
    a {{ color: #2563eb; }}
  </style>
</head>
<body>
  <h1>💱 Currency Converter API</h1>
  <span class="badge">Vibe Coded · FastAPI · 20 currencies</span>
  <p>Simple, fast currency conversion with no external dependencies.</p>

  <h2>Endpoints</h2>
  <ul>
    <li><a href="/convert?from_currency=USD&to_currency=INR&amount=100"><code>GET /convert</code></a> — convert an amount</li>
    <li><a href="/currencies"><code>GET /currencies</code></a> — list all supported currencies</li>
    <li><a href="/health"><code>GET /health</code></a> — liveness probe</li>
    <li><a href="/docs"><code>GET /docs</code></a> — Swagger UI</li>
  </ul>

  <h2>Example</h2>
  <p><code>GET /convert?from_currency=USD&amp;to_currency=INR&amp;amount=100</code></p>

  <h2>Supported Currencies ({len(currencies)})</h2>
  <table><tr><th>Code</th><th>Name</th></tr>{rows}</table>
</body>
</html>""")


@app.get("/currencies", response_model=list[CurrencyInfo])
def list_currencies() -> list[CurrencyInfo]:
    """Return all supported currency codes and their full names."""
    return [CurrencyInfo(code=k, name=v) for k, v in supported_currencies().items()]


@app.get("/convert", response_model=ConversionResult)
def convert_currency(
    from_currency: str = Query(..., description="Source currency code, e.g. USD"),
    to_currency: str = Query(..., description="Target currency code, e.g. INR"),
    amount: float = Query(..., gt=0, description="Amount to convert"),
) -> ConversionResult:
    """Convert an amount from one currency to another."""
    try:
        result = convert(amount, from_currency, to_currency)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    fc = from_currency.upper()
    tc = to_currency.upper()
    rate = round(result / amount, 6)
    return ConversionResult(
        from_currency=fc,
        to_currency=tc,
        amount=amount,
        converted=result,
        rate=rate,
    )
