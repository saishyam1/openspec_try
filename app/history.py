"""In-memory conversion history — stores the last 50 conversions."""

from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from typing import NamedTuple


class HistoryEntry(NamedTuple):
    from_currency: str
    to_currency: str
    amount: float
    converted: float
    rate: float
    timestamp: str


_history: deque[HistoryEntry] = deque(maxlen=50)


def record(from_currency: str, to_currency: str, amount: float, converted: float, rate: float) -> None:
    _history.appendleft(
        HistoryEntry(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            converted=converted,
            rate=rate,
            timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )
    )


def recent(limit: int = 10) -> list[HistoryEntry]:
    return list(_history)[:limit]
