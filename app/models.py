"""Pydantic models for the Currency Converter API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ConversionRequest(BaseModel):
    from_currency: str = Field(examples=["USD"])
    to_currency: str = Field(examples=["INR"])
    amount: float = Field(gt=0, examples=[100.0])


class ConversionResult(BaseModel):
    from_currency: str
    to_currency: str
    amount: float
    converted: float
    rate: float


class CurrencyInfo(BaseModel):
    code: str
    name: str
