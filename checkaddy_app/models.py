from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass(slots=True)
class LookupResult:
    coin: str
    address: str
    is_valid_format: bool
    validation_reason: str
    confirmed_balance: Optional[str]
    unconfirmed_balance: Optional[str]
    total_received: Optional[str]
    total_sent: Optional[str]
    tx_count: Optional[int]
    explorer_url: str
    data_source: str
    fetched_at_utc: str
    api_error: Optional[str]
    api_skipped: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "coin": self.coin,
            "address": self.address,
            "is_valid_format": self.is_valid_format,
            "validation_reason": self.validation_reason,
            "confirmed_balance": self.confirmed_balance,
            "unconfirmed_balance": self.unconfirmed_balance,
            "total_received": self.total_received,
            "total_sent": self.total_sent,
            "tx_count": self.tx_count,
            "explorer_url": self.explorer_url,
            "data_source": self.data_source,
            "fetched_at_utc": self.fetched_at_utc,
            "api_error": self.api_error,
            "api_skipped": self.api_skipped,
        }
