from __future__ import annotations

from .common import base58check_verify


def validate_doge_address(address: str) -> tuple[bool, str]:
    address = address.strip()
    if not (address.startswith("D") or address.startswith("A") or address.startswith("9")):
        return False, "DOGE Base58 addresses must start with D, A, or 9"

    valid, reason, version, payload_len = base58check_verify(address)
    if not valid:
        return False, reason
    if payload_len != 21:
        return False, "Unexpected Base58 payload length"
    if version not in (0x1E, 0x16):
        return False, "Invalid DOGE version byte"
    return True, "Valid Base58Check address"
