"""
BinanceQuest AI — Portfolio Skill
Track crypto holdings and get AI-powered rebalancing suggestions.
Supports major cryptos and stablecoins (USDT, USDC, FDUSD, TUSD, DAI).
"""

COIN_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "BNB": "binancecoin",
    "SOL": "solana",
    "XRP": "ripple",
    "DAI": "dai",
}

STABLECOINS = {"USDT", "USDC", "FDUSD", "TUSD", "DAI"}

def calculate_portfolio_value(portfolio, prices):
    """
    Calculate total portfolio value.
    portfolio: dict {coin: quantity} e.g. {"BTC": 0.5, "ETH": 2, "USDC": 1000}
    prices: dict from prices.py get_prices()
    Stablecoins are always valued at $1.00
    """
    total = 0
    breakdown = []
    for coin, qty in portfolio.items():
        coin_upper = coin.upper()
        if coin_upper in STABLECOINS:
            price = 1.0
            change = 0.0
        else:
            price_data = prices.get(coin_upper, {})
            price = price_data.get("price", 0)
            change = price_data.get("change_24h", 0)
        value = price * qty
        total += value
        breakdown.append({
            "coin": coin_upper,
            "quantity": qty,
            "price": price,
            "change": change,
            "value": value,
            "percentage": 0
        })

    for item in breakdown:
        item["percentage"] = (item["value"] / total * 100) if total > 0 else 0

    return total, breakdown

def add_coin(portfolio, coin, qty):
    """Add or update a coin in portfolio."""
    portfolio[coin.upper()] = qty
    return portfolio

def remove_coin(portfolio, coin):
    """Remove a coin from portfolio. Returns True if removed, False if not found."""
    coin_upper = coin.upper()
    if coin_upper in portfolio:
        del portfolio[coin_upper]
        return True
    return False

def reset_portfolio(portfolio):
    """Clear entire portfolio."""
    portfolio.clear()
    return portfolio

def format_portfolio_message(portfolio, prices, lang="fr"):
    """Format portfolio into readable message."""
    if not portfolio:
        if lang == "en":
            return "💼 Portfolio empty!\n\nAdd crypto:\n/ajout BTC 0.5\n/ajout ETH 2\n/ajout USDC 1000"
        return "💼 Portefeuille vide!\n\nAjoute tes cryptos:\n/ajout BTC 0.5\n/ajout ETH 2\n/ajout USDC 1000"

    total, breakdown = calculate_portfolio_value(portfolio, prices)
    title = "💼 My Portfolio" if lang == "en" else "💼 Mon Portefeuille"
    lines = [title, ""]

    for item in breakdown:
        lines.append(f"• {item['coin']}: {item['quantity']} × ${item['price']:,.2f} = ${item['value']:,.2f} ({item['percentage']:.1f}%)")

    lines.append("")
    total_label = "Total value" if lang == "en" else "Valeur totale"
    lines.append(f"💰 {total_label}: ${total:,.2f}")
    lines.append("")
    hint = "Commands: /ajout BTC 0.5 | /retirer BTC | /reset_portfolio"
    lines.append(f"ℹ️ {hint}")
    return "\n".join(lines)
