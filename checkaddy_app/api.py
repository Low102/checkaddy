from __future__ import annotations

import time
from typing import Any, Optional
from urllib.parse import urlparse

import requests

from .constants import (
    BCH,
    BTC,
    BLOCKCYPHER_BASE,
    BLOCKCYPHER_NETWORKS,
    BLOCKSTREAM_BASE,
    COIN_DECIMALS,
    EVM_RPC_BY_COIN,
    FULLSTACK_BCH_BASE,
    TRANSIENT_HTTP_STATUSES,
)
from .formatters import parse_optional_int, sats_to_coin_str, units_to_coin_str


class ApiClient:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "checkaddy/1.0"})

    def close(self) -> None:
        self.session.close()

    @staticmethod
    def rpc_host(url: str) -> str:
        parsed = urlparse(url)
        return parsed.netloc or url

    @staticmethod
    def format_rpc_error(error: Any) -> str:
        if isinstance(error, dict):
            code = error.get("code")
            message = error.get("message")
            if code is not None and message is not None:
                return f"{code}: {message}"
            if message is not None:
                return str(message)
        return str(error)

    @staticmethod
    def extract_error_message(response: requests.Response) -> str:
        try:
            payload = response.json()
        except ValueError:
            return response.text.strip() or f"HTTP {response.status_code}"

        if isinstance(payload, dict):
            data = payload.get("data")
            if isinstance(data, dict):
                error_message = data.get("error_message")
                if isinstance(error_message, str) and error_message.strip():
                    return error_message

            for key in ("error", "message", "detail"):
                value = payload.get(key)
                if isinstance(value, str) and value.strip():
                    return value

        return f"HTTP {response.status_code}"

    def _request_json(
        self,
        method: str,
        url: str,
        payload: Optional[dict[str, Any]] = None,
        max_retries: int = 3,
    ) -> dict[str, Any]:
        backoffs = [0.4, 0.8, 1.6]
        for attempt in range(max_retries + 1):
            try:
                response = self.session.request(method, url, json=payload, timeout=(3, 12))
            except requests.RequestException as exc:
                if attempt < max_retries:
                    time.sleep(backoffs[min(attempt, len(backoffs) - 1)])
                    continue
                raise RuntimeError(f"Network error: {exc}") from exc

            if response.status_code in TRANSIENT_HTTP_STATUSES:
                if attempt < max_retries:
                    time.sleep(backoffs[min(attempt, len(backoffs) - 1)])
                    continue
                raise RuntimeError(f"HTTP {response.status_code} from API")

            if not response.ok:
                message = self.extract_error_message(response)
                raise RuntimeError(f"HTTP {response.status_code} from API: {message}")

            try:
                return response.json()
            except ValueError as exc:
                raise RuntimeError("Invalid JSON response from API") from exc

        raise RuntimeError("Request failed after retries")

    def request_json(self, url: str, max_retries: int = 3) -> dict[str, Any]:
        return self._request_json("GET", url, payload=None, max_retries=max_retries)

    def request_json_post(
        self, url: str, payload: dict[str, Any], max_retries: int = 3
    ) -> dict[str, Any]:
        return self._request_json("POST", url, payload=payload, max_retries=max_retries)

    def fetch_btc_info(self, address: str) -> dict[str, Any]:
        payload = self.request_json(f"{BLOCKSTREAM_BASE}/address/{address}")
        chain = payload.get("chain_stats", {})
        mempool = payload.get("mempool_stats", {})

        funded = int(chain.get("funded_txo_sum", 0))
        spent = int(chain.get("spent_txo_sum", 0))
        tx_count = int(chain.get("tx_count", 0))
        mem_funded = int(mempool.get("funded_txo_sum", 0))
        mem_spent = int(mempool.get("spent_txo_sum", 0))

        return {
            "confirmed_balance": sats_to_coin_str(funded - spent),
            "unconfirmed_balance": sats_to_coin_str(mem_funded - mem_spent),
            "total_received": sats_to_coin_str(funded),
            "total_sent": sats_to_coin_str(spent),
            "tx_count": tx_count,
        }

    def fetch_blockcypher_utxo_info(self, coin: str, address: str) -> dict[str, Any]:
        network = BLOCKCYPHER_NETWORKS[coin]
        payload = self.request_json(f"{BLOCKCYPHER_BASE}/{network}/main/addrs/{address}/balance")

        confirmed_units = parse_optional_int(payload.get("balance"))
        unconfirmed_units = parse_optional_int(payload.get("unconfirmed_balance"))
        total_received_units = parse_optional_int(payload.get("total_received"))
        total_sent_units = parse_optional_int(payload.get("total_sent"))
        tx_count = parse_optional_int(payload.get("n_tx"))

        if confirmed_units is None:
            raise RuntimeError("Missing confirmed balance in response")

        return {
            "confirmed_balance": units_to_coin_str(confirmed_units, COIN_DECIMALS[coin]),
            "unconfirmed_balance": (
                units_to_coin_str(unconfirmed_units, COIN_DECIMALS[coin])
                if unconfirmed_units is not None
                else None
            ),
            "total_received": (
                units_to_coin_str(total_received_units, COIN_DECIMALS[coin])
                if total_received_units is not None
                else None
            ),
            "total_sent": (
                units_to_coin_str(total_sent_units, COIN_DECIMALS[coin])
                if total_sent_units is not None
                else None
            ),
            "tx_count": tx_count,
        }

    def fetch_bch_info(self, address: str) -> dict[str, Any]:
        payload = self.request_json(f"{FULLSTACK_BCH_BASE}/balance/{address}")
        if payload.get("success") is not True:
            raise RuntimeError("API returned a non-success status")

        balance = payload.get("balance", {})
        confirmed_units = parse_optional_int(balance.get("confirmed"))
        unconfirmed_units = parse_optional_int(balance.get("unconfirmed"))

        if confirmed_units is None:
            raise RuntimeError("Missing confirmed balance in response")

        tx_count: Optional[int] = None
        try:
            tx_payload = self.request_json(f"{FULLSTACK_BCH_BASE}/transactions/{address}")
            if tx_payload.get("success") is True:
                transactions = tx_payload.get("transactions")
                if isinstance(transactions, list):
                    tx_count = len(transactions)
        except RuntimeError:
            pass

        return {
            "confirmed_balance": units_to_coin_str(confirmed_units, COIN_DECIMALS[BCH]),
            "unconfirmed_balance": (
                units_to_coin_str(unconfirmed_units, COIN_DECIMALS[BCH])
                if unconfirmed_units is not None
                else None
            ),
            "total_received": None,
            "total_sent": None,
            "tx_count": tx_count,
        }

    def fetch_evm_info(self, coin: str, address: str) -> dict[str, Any]:
        errors: list[str] = []
        for rpc_url in EVM_RPC_BY_COIN[coin]:
            balance_payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "eth_getBalance",
                "params": [address, "latest"],
            }
            tx_count_payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "eth_getTransactionCount",
                "params": [address, "latest"],
            }

            try:
                balance_response = self.request_json_post(rpc_url, balance_payload)
                tx_count_response = self.request_json_post(rpc_url, tx_count_payload)
                if "error" in balance_response:
                    raise RuntimeError(
                        f"RPC eth_getBalance error: {self.format_rpc_error(balance_response['error'])}"
                    )
                if "error" in tx_count_response:
                    raise RuntimeError(
                        "RPC eth_getTransactionCount error: "
                        f"{self.format_rpc_error(tx_count_response['error'])}"
                    )

                balance_hex = balance_response.get("result")
                tx_count_hex = tx_count_response.get("result")
                if not isinstance(balance_hex, str) or not balance_hex.startswith("0x"):
                    raise RuntimeError("Missing eth_getBalance result")
                if not isinstance(tx_count_hex, str) or not tx_count_hex.startswith("0x"):
                    raise RuntimeError("Missing eth_getTransactionCount result")

                try:
                    balance_units = int(balance_hex, 16)
                    tx_count = int(tx_count_hex, 16)
                except ValueError as exc:
                    raise RuntimeError("Invalid hex value in RPC response") from exc

                return {
                    "confirmed_balance": units_to_coin_str(balance_units, COIN_DECIMALS[coin]),
                    "unconfirmed_balance": None,
                    "total_received": None,
                    "total_sent": None,
                    "tx_count": tx_count,
                    "data_source": self.rpc_host(rpc_url),
                }
            except RuntimeError as exc:
                errors.append(f"{self.rpc_host(rpc_url)}: {exc}")
                continue

        short_errors = "; ".join(errors[:2])
        if len(errors) > 2:
            short_errors += f"; +{len(errors) - 2} more"
        raise RuntimeError(f"All RPC endpoints failed: {short_errors}")

    def fetch_coin_info(self, coin: str, address: str) -> dict[str, Any]:
        if coin == BTC:
            return self.fetch_btc_info(address)
        if coin in BLOCKCYPHER_NETWORKS:
            return self.fetch_blockcypher_utxo_info(coin, address)
        if coin == BCH:
            return self.fetch_bch_info(address)
        if coin in EVM_RPC_BY_COIN:
            return self.fetch_evm_info(coin, address)
        raise RuntimeError(f"Unsupported coin: {coin}")
