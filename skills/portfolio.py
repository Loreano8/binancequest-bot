"""
BinanceQuest AI — Portfolio Skill
Track crypto holdings and get AI-powered rebalancing suggestions.
"""

COIN_IDS = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "BNB": "BNBUSDT",
    "SOL": "SOLUSDT",
    "XRP": "XRPUSDT",
}

def calculate_portfolio_value(portfolio, prices):
    """
    Calculate total portfolio value.
    portfolio: dict {coin: quantity} e.g. {"BTC": 0.5, "ETH": 2}
    prices: dict from prices.py get_prices()
    """
    total = 0
    breakdown = []
    for coin, qty in portfolio.items():
        coin_upper = coin.upper()
        price_data = prices.get(coin_upper, {})
        price = price_data.get("price", 0)
        value = price * qty
        total += value
        breakdown.append({
            "coin": coin_upper,
            "quantity": qty,
            "price": price,
            "value": value,
            "percentage": 0
        })

    # Calculate percentages
    for item in breakdown:
        item["percentage"] = (item["value"] / total * 100) if total > 0 else 0

    return total, breakdown

def format_portfolio_message(portfolio, prices, lang="fr"):
    """Format portfolio into readable message."""
    if not portfolio:
        if lang == "en":
            return "💼 Portfolio empty!\n\nAdd crypto:\n/ajout BTC 0.5\n/ajout ETH 2"
        return "💼 Portefeuille vide!\n\nAjoute tes cryptos:\n/ajout BTC 0.5\n/ajout ETH 2"

    total, breakdown = calculate_portfolio_value(portfolio, prices)
    title = "💼 My Portfolio" if lang == "en" else "💼 Mon Portefeuille"
    lines = [title, ""]

    for item in breakdown:
        lines.append(f"• {item['coin']}: {item['quantity']} × ${item['price']:,.2f} = ${item['value']:,.2f} ({item['percentage']:.1f}%)")

    lines.append("")
    total_label = "Total value" if lang == "en" else "Valeur totale"
    lines.append(f"💰 {total_label}: ${total:,.2f}")
    return "\n".join(lines)
