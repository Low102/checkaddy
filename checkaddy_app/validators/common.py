from __future__ import annotations

import hashlib
from typing import Optional

from ..constants import ADDRESS_SAFE_RE, BASE58_INDEX, BECH32_CHARSET_MAP


def is_address_characters_safe(address: str) -> bool:
    return ADDRESS_SAFE_RE.fullmatch(address) is not None


def base58_decode(value: str) -> Optional[bytes]:
    number = 0
    for char in value:
        digit = BASE58_INDEX.get(char)
        if digit is None:
            return None
        number = number * 58 + digit

    raw = b"" if number == 0 else number.to_bytes((number.bit_length() + 7) // 8, "big")
    pad = len(value) - len(value.lstrip("1"))
    return b"\x00" * pad + raw


def base58check_verify(address: str) -> tuple[bool, str, Optional[int], Optional[int]]:
    decoded = base58_decode(address)
    if decoded is None:
        return False, "Invalid Base58 characters", None, None
    if len(decoded) < 4:
        return False, "Too short for Base58Check", None, None

    payload, checksum = decoded[:-4], decoded[-4:]
    digest = hashlib.sha256(hashlib.sha256(payload).digest()).digest()
    if checksum != digest[:4]:
        return False, "Base58Check checksum mismatch", None, None
    if not payload:
        return False, "Missing version byte", None, None

    return True, "Valid Base58Check", payload[0], len(payload)


def bech32_polymod(values: list[int]) -> int:
    generator = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    checksum = 1
    for value in values:
        top = checksum >> 25
        checksum = ((checksum & 0x1FFFFFF) << 5) ^ value
        for index in range(5):
            if (top >> index) & 1:
                checksum ^= generator[index]
    return checksum


def bech32_hrp_expand(hrp: str) -> list[int]:
    return [ord(char) >> 5 for char in hrp] + [0] + [ord(char) & 31 for char in hrp]


def bech32_verify_checksum(hrp: str, data: list[int], spec: str) -> bool:
    expected = 1 if spec == "bech32" else 0x2BC830A3
    return bech32_polymod(bech32_hrp_expand(hrp) + data) == expected


def bech32_decode(address: str) -> tuple[Optional[str], Optional[list[int]], Optional[str]]:
    if address.lower() != address and address.upper() != address:
        return None, None, None

    normalized = address.lower()
    separator_index = normalized.rfind("1")
    if separator_index < 1 or separator_index + 7 > len(normalized):
        return None, None, None

    hrp = normalized[:separator_index]
    data: list[int] = []
    for char in normalized[separator_index + 1 :]:
        mapped = BECH32_CHARSET_MAP.get(char)
        if mapped is None:
            return None, None, None
        data.append(mapped)

    if bech32_verify_checksum(hrp, data, "bech32"):
        return hrp, data[:-6], "bech32"
    if bech32_verify_checksum(hrp, data, "bech32m"):
        return hrp, data[:-6], "bech32m"
    return None, None, None
