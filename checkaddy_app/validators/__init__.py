from __future__ import annotations

from ..constants import BCH, BSC, BTC, DASH, DOGE, ETH, LTC, POLYGON
from .bch import validate_bch_address
from .btc import validate_btc_address
from .common import is_address_characters_safe
from .dash import validate_dash_address
from .doge import validate_doge_address
from .evm import validate_evm_address
from .ltc import validate_ltc_address


def validate_address(coin: str, address: str) -> tuple[bool, str]:
    if not address:
        return False, "Address is required"
    if not is_address_characters_safe(address):
        return False, "Address contains unsupported characters"

    if coin == BTC:
        return validate_btc_address(address)
    if coin == LTC:
        return validate_ltc_address(address)
    if coin == DOGE:
        return validate_doge_address(address)
    if coin == DASH:
        return validate_dash_address(address)
    if coin == BCH:
        return validate_bch_address(address)
    if coin in (ETH, BSC, POLYGON):
        return validate_evm_address(address)
    return False, "Unsupported coin"
