"""Pydantic models — per spec: ConversionResult and CurrencyInfo."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ConversionResult(BaseModel):
    """Response schema for GET /convert."""

    from_currency: str
    to_currency: str
    amount: float
    converted: float
    rate: float


class CurrencyInfo(BaseModel):
    """Single item in GET /currencies response."""

    code: str
    name: str
