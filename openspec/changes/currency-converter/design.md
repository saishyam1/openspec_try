## Context

A currency converter REST API built with FastAPI. Exchange rates are stored as a static in-memory dict mapping currency codes to their USD equivalent. All conversions route through USD as the base currency. No database, no external HTTP calls — the service is fully self-contained.

## Goals / Non-Goals

**Goals:**
- Expose `GET /convert?from_currency=X&to_currency=Y&amount=N` returning converted value and rate
- Expose `GET /currencies` returning all supported codes and names
- Validate unknown currency codes and non-positive amounts with HTTP 400
- Keep implementation stateless and dependency-free

**Non-Goals:**
- Live/real-time exchange rates (static table only)
- Authentication or rate limiting
- Currency pairs beyond the 20 supported codes
- Persistent storage

## Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Rate base currency | USD | Simplest — one table, any pair calculable via triangulation |
| Conversion formula | `(amount / from_rate) * to_rate` | Direct, readable, no rounding until final result |
| Rounding | 6 decimal places on converted, 6 on rate | Enough precision for financial display without float noise |
| Framework | FastAPI + Pydantic v2 | Matches existing project stack |
| Module layout | `converter.py` (rates + logic) · `models.py` (schemas) · `main.py` (HTTP layer) | Single-responsibility, mirrors SDD separation of concerns |

## Risks / Trade-offs

- Static rates go stale over time — acceptable for a demo/workshop context; a future version would call an external rates API
- All 20 currencies share one rate table — no bid/ask spread simulation
