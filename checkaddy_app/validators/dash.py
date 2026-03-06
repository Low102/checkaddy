from __future__ import annotations

from .common import base58check_verify


def validate_dash_address(address: str) -> tuple[bool, str]:
    address = address.strip()
    if not (address.startswith("X") or address.startswith("7")):
        return False, "DASH Base58 addresses must start with X or 7"

    valid, reason, version, payload_len = base58check_verify(address)
    if not valid:
        return False, reason
    if payload_len != 21:
        return False, "Unexpected Base58 payload length"
    if version not in (0x4C, 0x10):
        return False, "Invalid DASH version byte"
    return True, "Valid Base58Check address"
