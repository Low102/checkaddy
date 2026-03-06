from __future__ import annotations

from .common import base58check_verify, bech32_decode


def validate_ltc_address(address: str) -> tuple[bool, str]:
    address = address.strip()
    if address.lower().startswith("ltc1"):
        hrp, data, spec = bech32_decode(address)
        if hrp is None:
            return False, "Invalid Bech32 or Bech32m checksum"
        if hrp != "ltc":
            return False, "Invalid HRP for LTC"
        if not data:
            return False, "Missing witness program"
        return True, f"Valid {spec} address"

    if not (address.startswith("L") or address.startswith("M") or address.startswith("3")):
        return False, "LTC Base58 addresses must start with L, M, or 3"

    valid, reason, version, payload_len = base58check_verify(address)
    if not valid:
        return False, reason
    if payload_len != 21:
        return False, "Unexpected Base58 payload length"
    if version not in (0x30, 0x32, 0x05):
        return False, "Invalid LTC version byte"
    return True, "Valid Base58Check address"
