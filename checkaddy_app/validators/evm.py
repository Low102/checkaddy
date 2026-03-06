from __future__ import annotations

from ..constants import EVM_ADDRESS_RE


def validate_evm_address(address: str) -> tuple[bool, str]:
    address = address.strip()
    if not EVM_ADDRESS_RE.fullmatch(address):
        return False, "EVM address must match 0x + 40 hex characters"

    body = address[2:]
    if body.islower() or body.isupper():
        return True, "Valid EVM hex address"
    return True, "Valid mixed-case EVM address (checksum not verified)"
