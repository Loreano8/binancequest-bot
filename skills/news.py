"""
BinanceQuest AI — News & Market Analysis Skill
AI-powered market briefing using OpenClaw/Claude.
Combines live Binance prices with intelligent analysis.
"""

def build_market_prompt(prices, lang="fr"):
    """Build the prompt for AI market analysis."""
    price_ctx = ""
    if prices:
        btc = prices.get("BTC", {})
        eth = prices.get("ETH", {})
        bnb = prices.get("BNB", {})
        price_ctx = (
            f"BTC ${btc.get('price', 0):,.0f} ({btc.get('change_24h', 0):+.1f}%), "
            f"ETH ${eth.get('price', 0):,.0f} ({eth.get('change_24h', 0):+.1f}%), "
            f"BNB ${bnb.get('price', 0):,.0f} ({bnb.get('change_24h', 0):+.1f}%)"
        )

    lang_instr = "Respond in English." if lang == "en" else "Réponds en français."

    system = (
        f"You are BinanceQuest AI, crypto education expert. {lang_instr} "
        "Give a concise market briefing covering: "
        "1) Overall market sentiment "
        "2) Key observations "
        "3) Educational opportunity for learners. "
        "Be factual, educational, no financial advice. Max 250 words."
    )

    user_msg = f"Analyze the current crypto market. Live prices: {price_ctx}"
    return system, user_msg

def format_news_message(analysis, lang="fr"):
    """Format the news response."""
    title = "📰 Market News" if lang == "en" else "📰 Actualités Marché"
    disclaimer = "⚠️ Not financial advice." if lang == "en" else "⚠️ Pas un conseil financier."
    return f"{title}\n\n{analysis}\n\n{disclaimer}"
