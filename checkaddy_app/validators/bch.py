from __future__ import annotations

from ..constants import BCH_CASHADDR_RE
from .common import base58check_verify


def validate_bch_address(address: str) -> tuple[bool, str]:
    address = address.strip()
    lower = address.lower()
    if lower.startswith("bitcoincash:"):
        payload = lower.split(":", 1)[1]
    else:
        payload = lower

    if payload.startswith("q") or payload.startswith("p"):
        if not BCH_CASHADDR_RE.fullmatch(payload):
            return False, "Invalid characters in BCH CashAddr payload"
        if len(payload) < 30:
            return False, "BCH CashAddr payload is too short"
        # Future improvement: replace this with full BCH CashAddr checksum verification.
        return True, "CashAddr format (checksum not verified)"

    if address.startswith("1") or address.startswith("3"):
        valid, reason, version, payload_len = base58check_verify(address)
        if not valid:
            return False, reason
        if payload_len != 21:
            return False, "Unexpected Base58 payload length"
        if version not in (0x00, 0x05):
            return False, "Invalid BCH legacy version byte"
        return True, "Valid legacy Base58Check address"

    return False, "BCH addresses must be CashAddr or legacy Base58"
