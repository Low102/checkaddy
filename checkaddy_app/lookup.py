from __future__ import annotations

from datetime import datetime, timezone

from .api import ApiClient
from .constants import DATA_SOURCE_BY_COIN, EXPLORER_URL_BY_COIN
from .models import LookupResult
from .validators import validate_address


def build_lookup_result(client: ApiClient, coin: str, address: str) -> LookupResult:
    explorer_url = EXPLORER_URL_BY_COIN[coin].format(address=address)
    data_source = DATA_SOURCE_BY_COIN[coin]
    is_valid, reason = validate_address(coin, address)

    result = LookupResult(
        coin=coin,
        address=address,
        is_valid_format=is_valid,
        validation_reason=reason,
        confirmed_balance=None,
        unconfirmed_balance=None,
        total_received=None,
        total_sent=None,
        tx_count=None,
        explorer_url=explorer_url,
        data_source=data_source,
        fetched_at_utc=datetime.now(timezone.utc).isoformat(),
        api_error=None,
        api_skipped=False,
    )

    if not is_valid:
        result.api_skipped = True
        return result

    try:
        payload = client.fetch_coin_info(coin, address)
    except RuntimeError as exc:
        result.api_error = str(exc)
        return result

    if isinstance(payload.get("data_source"), str):
        result.data_source = payload["data_source"]
    result.confirmed_balance = payload["confirmed_balance"]
    result.unconfirmed_balance = payload["unconfirmed_balance"]
    result.total_received = payload["total_received"]
    result.total_sent = payload["total_sent"]
    result.tx_count = payload["tx_count"]
    return result
