from __future__ import annotations

from decimal import Decimal, ROUND_DOWN, getcontext
from typing import Any, Optional

from .constants import COIN_DECIMALS, COIN_DISPLAY_SYMBOL, COIN_UNIT_LABEL

getcontext().prec = 28


def quant_for_decimals(decimals: int) -> Decimal:
    return Decimal(1).scaleb(-decimals)


def parse_optional_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, list):
        return len(value)
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


def decimal_coin_str(value: Any, decimals: int = 8) -> str:
    return format(Decimal(str(value)).quantize(quant_for_decimals(decimals)), "f")


def units_to_coin_str(units: int, decimals: int) -> str:
    scale = Decimal(10) ** decimals
    return format((Decimal(units) / scale).quantize(quant_for_decimals(decimals)), "f")


def sats_to_coin_str(units: int) -> str:
    return units_to_coin_str(units, 8)


def coin_str_to_units(amount_str: str, decimals: int) -> int:
    amount = Decimal(amount_str).quantize(quant_for_decimals(decimals))
    scale = Decimal(10) ** decimals
    return int((amount * scale).to_integral_value(rounding=ROUND_DOWN))


def format_amount_display(coin: str, amount_str: Optional[str]) -> str:
    if amount_str is None:
        return "N/A"
    decimals = COIN_DECIMALS[coin]
    units = coin_str_to_units(amount_str, decimals)
    unit_label = COIN_UNIT_LABEL[coin]
    display_symbol = COIN_DISPLAY_SYMBOL[coin]
    return f"{amount_str} {display_symbol} ({units} {unit_label})"


def format_validation_badge(valid: bool, reason: str) -> str:
    state = "valid" if valid else "invalid"
    return f"{state} ({reason})"
