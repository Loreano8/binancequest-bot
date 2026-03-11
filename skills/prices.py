"""
BinanceQuest AI — Prices Skill
Real-time cryptocurrency prices via official Binance API.
No third-party dependency — direct from Binance.
"""

import requests

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/24hr"

TRACKED_SYMBOLS = {
    "BTCUSDT": {"name": "Bitcoin", "symbol": "BTC"},
    "ETHUSDT": {"name": "Ethereum", "symbol": "ETH"},
    "BNBUSDT": {"name": "BNB", "symbol": "BNB"},
    "SOLUSDT": {"name": "Solana", "symbol": "SOL"},
    "XRPUSDT": {"name": "XRP", "symbol": "XRP"},
}

def get_prices():
    """Fetch real-time prices from Binance API."""
    try:
        response = requests.get(BINANCE_API_URL, timeout=8)
        data = response.json()
        result = {}
        for item in data:
            sym = item.get("symbol", "")
            if sym in TRACKED_SYMBOLS:
                info = TRACKED_SYMBOLS[sym]
                result[info["symbol"]] = {
                    "name": info["name"],
                    "price": float(item["lastPrice"]),
                    "change_24h": float(item["priceChangePercent"]),
                    "volume": float(item["volume"]),
                }
        return result
    except Exception as e:
        return None

def format_price_message(prices, lang="fr"):
    """Format prices into a readable message."""
    if not prices:
        return "❌ " + ("Unable to fetch prices. Try again." if lang == "en" else "Impossible de récupérer les prix.")

    title = "💰 Live Crypto Prices" if lang == "en" else "💰 Prix Crypto en Direct"
    lines = [title, ""]

    for symbol, data in prices.items():
        change = data["change_24h"]
        emoji = "🟢" if change >= 0 else "🔴"
        arrow = "+" if change >= 0 else ""
        lines.append(f"{emoji} {data['name']} ({symbol}): ${data['price']:,.2f} ({arrow}{change:.2f}%)")

    lines.append("")
    lines.append("📊 Source: Binance API")
    return "\n".join(lines)
