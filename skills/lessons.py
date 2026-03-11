"""
BinanceQuest AI — Lessons Skill
Crypto education lessons based on Binance Academy content.
Progressive learning: Beginner → Intermediate → Advanced.
"""

LESSONS = [
    {
        "title": "Bitcoin",
        "level": "beginner",
        "content": "Bitcoin is the 1st cryptocurrency (2009). Limited to 21M units, decentralized, secured by blockchain. Satoshi Nakamoto is its anonymous creator.",
        "content_fr": "Bitcoin est la 1ère cryptomonnaie (2009). Limité à 21M d'unités, décentralisé, sécurisé par la blockchain. Satoshi Nakamoto en est le créateur anonyme.",
    },
    {
        "title": "Binance & BNB",
        "level": "beginner",
        "content": "Binance is the world's largest crypto exchange, founded by CZ in 2017. BNB is its native token — used for fees, IEO, staking and much more.",
        "content_fr": "Binance est le plus grand exchange crypto au monde, fondé par CZ en 2017. BNB est son token natif — frais, IEO, staking et bien plus.",
    },
    {
        "title": "Blockchain",
        "level": "beginner",
        "content": "A distributed digital ledger shared across thousands of computers. Each transaction is grouped into blocks, chained and immutable. Transparent and secure.",
        "content_fr": "Registre numérique distribué entre des milliers d'ordinateurs. Chaque transaction est regroupée en blocs, chaînés et immuables. Transparent et sécurisé.",
    },
    {
        "title": "DeFi",
        "level": "intermediate",
        "content": "Decentralized Finance = financial services without banks. Smart contracts automate everything: loans, borrowing, trading. Accessible 24/7 to everyone.",
        "content_fr": "Finance Décentralisée = services financiers sans banque. Les smart contracts automatisent tout : prêts, emprunts, échanges. Accessible 24h/24 à tous.",
    },
    {
        "title": "Spot vs Futures",
        "level": "intermediate",
        "content": "Spot: you actually buy the asset. Futures: you speculate on its future price with leverage. Futures amplify both gains AND losses — high risk!",
        "content_fr": "Spot : vous achetez l'actif réellement. Futures : vous spéculez sur son prix futur avec du levier. Les futures amplifient gains ET pertes — risque élevé !",
    },
    {
        "title": "Staking",
        "level": "intermediate",
        "content": "Lock your crypto to help validate the Proof of Stake network. In return, you receive regular rewards. Binance Earn simplifies staking.",
        "content_fr": "Bloquez vos cryptos pour aider à valider le réseau Proof of Stake. En échange, vous recevez des récompenses régulières. Binance Earn simplifie le staking.",
    },
    {
        "title": "Technical Analysis",
        "level": "advanced",
        "content": "Study of charts to anticipate price movements. Key indicators: RSI, moving averages, Bollinger Bands, supports and resistances.",
        "content_fr": "Étude des graphiques pour anticiper les mouvements. Indicateurs clés : RSI, moyennes mobiles, bandes de Bollinger, supports et résistances.",
    },
    {
        "title": "Crypto Security",
        "level": "advanced",
        "content": "Golden rules: enable 2FA, use a hardware wallet for large sums, NEVER share your private key, beware of scams and phishing.",
        "content_fr": "Règles d'or : activez le 2FA, utilisez un hardware wallet pour les grosses sommes, ne partagez JAMAIS votre clé privée, méfiez-vous des arnaques.",
    },
]

def get_random_lesson():
    import random
    return random.choice(LESSONS)

def get_lessons_by_level(level):
    return [l for l in LESSONS if l["level"] == level]
