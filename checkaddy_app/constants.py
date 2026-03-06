from __future__ import annotations

import re

BTC = "BTC"
LTC = "LTC"
DOGE = "DOGE"
DASH = "DASH"
ETH = "ETH"
BSC = "BSC"
POLYGON = "POLYGON"
BCH = "BCH"

REPOSITORY_URL = "https://github.com/zvspany/checkaddy"

BLOCKSTREAM_BASE = "https://blockstream.info/api"
BLOCKCYPHER_BASE = "https://api.blockcypher.com/v1"
FULLSTACK_BCH_BASE = "https://api.fullstack.cash/v5/electrumx"

ETH_RPC_URLS = (
    "https://ethereum-rpc.publicnode.com",
    "https://eth.llamarpc.com",
    "https://rpc.flashbots.net",
    "https://cloudflare-eth.com",
)
BSC_RPC_URLS = (
    "https://bsc-dataseed.binance.org",
    "https://bsc-rpc.publicnode.com",
)
POLYGON_RPC_URLS = (
    "https://polygon-bor-rpc.publicnode.com",
    "https://polygon-rpc.com",
)

TRANSIENT_HTTP_STATUSES = {429, 500, 502, 503, 504}

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BASE58_INDEX = {char: index for index, char in enumerate(BASE58_ALPHABET)}

BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
BECH32_CHARSET_MAP = {char: index for index, char in enumerate(BECH32_CHARSET)}

ADDRESS_SAFE_RE = re.compile(r"^[A-Za-z0-9:]+$")
EVM_ADDRESS_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")
BCH_CASHADDR_RE = re.compile(r"^[qpzry9x8gf2tvdw0s3jn54khce6mua7l]+$")

COIN_OPTIONS: list[tuple[str, str]] = [
    (BTC, "Bitcoin (BTC)"),
    (LTC, "Litecoin (LTC)"),
    (DOGE, "Dogecoin (DOGE)"),
    (DASH, "Dash (DASH)"),
    (ETH, "Ethereum (ETH)"),
    (BSC, "BNB Chain (BSC)"),
    (POLYGON, "Polygon PoS (MATIC)"),
    (BCH, "Bitcoin Cash (BCH)"),
]

COIN_RADIO_IDS = {coin: f"coin-{coin.lower()}" for coin, _ in COIN_OPTIONS}
COIN_FROM_RADIO_ID = {radio_id: coin for coin, radio_id in COIN_RADIO_IDS.items()}

COIN_DECIMALS = {
    BTC: 8,
    LTC: 8,
    DOGE: 8,
    DASH: 8,
    BCH: 8,
    ETH: 18,
    BSC: 18,
    POLYGON: 18,
}

COIN_UNIT_LABEL = {
    BTC: "satoshis",
    LTC: "litoshis",
    DOGE: "koinu",
    DASH: "duffs",
    BCH: "satoshis",
    ETH: "wei",
    BSC: "wei",
    POLYGON: "wei",
}

COIN_DISPLAY_SYMBOL = {
    BTC: "BTC",
    LTC: "LTC",
    DOGE: "DOGE",
    DASH: "DASH",
    BCH: "BCH",
    ETH: "ETH",
    BSC: "BNB",
    POLYGON: "MATIC",
}

BLOCKCYPHER_NETWORKS = {
    LTC: "ltc",
    DOGE: "doge",
    DASH: "dash",
}

EVM_RPC_BY_COIN = {
    ETH: ETH_RPC_URLS,
    BSC: BSC_RPC_URLS,
    POLYGON: POLYGON_RPC_URLS,
}

EXPLORER_URL_BY_COIN = {
    BTC: "https://blockstream.info/address/{address}",
    LTC: "https://live.blockcypher.com/ltc/address/{address}/",
    DOGE: "https://live.blockcypher.com/doge/address/{address}/",
    DASH: "https://live.blockcypher.com/dash/address/{address}/",
    BCH: "https://blockchair.com/bitcoin-cash/address/{address}",
    ETH: "https://etherscan.io/address/{address}",
    BSC: "https://bscscan.com/address/{address}",
    POLYGON: "https://polygonscan.com/address/{address}",
}

DATA_SOURCE_BY_COIN = {
    BTC: "blockstream.info",
    LTC: "api.blockcypher.com",
    DOGE: "api.blockcypher.com",
    DASH: "api.blockcypher.com",
    BCH: "api.fullstack.cash",
    ETH: "public RPC fallback",
    BSC: "public RPC fallback",
    POLYGON: "public RPC fallback",
}
