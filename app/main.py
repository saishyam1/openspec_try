"""FastAPI HTTP layer — implements all scenarios defined in specs/currency-conversion.md."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

from app.converter import convert, supported_currencies
from app.models import ConversionResult, CurrencyInfo

app = FastAPI(title="Currency Converter API", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe. Satisfies spec scenario: Health endpoint returns ok."""
    return {"status": "ok"}


@app.get("/currencies", response_model=list[CurrencyInfo])
def list_currencies() -> list[CurrencyInfo]:
    """Return all supported currency codes and names.

    Satisfies spec scenarios:
    - List all currencies (>=20 items)
    - USD always present with name 'US Dollar'
    """
    return [CurrencyInfo(code=k, name=v) for k, v in supported_currencies().items()]


@app.get("/convert", response_model=ConversionResult)
def convert_currency(
    from_currency: str = Query(..., description="Source currency code, e.g. USD"),
    to_currency: str = Query(..., description="Target currency code, e.g. INR"),
    amount: float = Query(..., gt=0, description="Positive amount to convert"),
) -> ConversionResult:
    """Convert an amount between two currencies.

    Satisfies spec scenarios:
    - Successful conversion returns converted value and rate
    - Same-currency conversion returns original amount with rate=1.0
    - Unknown currency codes return HTTP 400
    - Zero / negative amounts return HTTP 422 (Pydantic gt=0 validation)
    """
    try:
        result = convert(amount, from_currency, to_currency)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

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


@app.get("/", response_class=HTMLResponse)
def landing() -> HTMLResponse:
    """HTML landing page listing endpoints and supported currencies."""
    currencies = supported_currencies()
    rows = "".join(
        f"<tr><td><strong>{code}</strong></td><td>{name}</td></tr>"
        for code, name in currencies.items()
    )
    return HTMLResponse(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Currency Converter — SDD</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 820px; margin: 2rem auto; padding: 0 1rem; background: #f8fafc; color: #1e293b; }}
    h1 {{ color: #0f172a; }} h2 {{ color: #1e40af; margin-top: 2rem; }}
    .badge {{ background: #dcfce7; color: #166534; padding: .3rem .75rem; border-radius: 999px; font-size: .9rem; font-weight: 600; }}
    code {{ background: #f1f5f9; padding: .15rem .4rem; border-radius: 4px; font-size: .9rem; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: .75rem; }}
    th, td {{ text-align: left; padding: .5rem .75rem; border-bottom: 1px solid #e2e8f0; }}
    th {{ background: #e2e8f0; }}
    a {{ color: #2563eb; }}
  </style>
</head>
<body>
  <h1>💱 Currency Converter API</h1>
  <span class="badge">Spec-Driven Development · OpenSpec · FastAPI</span>
  <p>Built following the SDD workflow: proposal → specs → design → tasks → implementation.</p>

  <h2>Endpoints</h2>
  <ul>
    <li><a href="/convert?from_currency=USD&to_currency=INR&amount=100"><code>GET /convert?from_currency=&amp;to_currency=&amp;amount=</code></a> — convert amount</li>
    <li><a href="/currencies"><code>GET /currencies</code></a> — list all supported currencies</li>
    <li><a href="/health"><code>GET /health</code></a> — liveness probe</li>
    <li><a href="/docs"><code>GET /docs</code></a> — Swagger UI</li>
  </ul>

  <h2>Supported Currencies ({len(currencies)})</h2>
  <table><tr><th>Code</th><th>Name</th></tr>{rows}</table>
</body>
</html>""")
