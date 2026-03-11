"""
BinanceQuest AI — Quiz Skill
Gamified crypto quizzes based on Binance Academy content.
+15 XP per correct answer. Tracks streaks and levels.
"""

QUIZ_BANK = [
    {
        "q": "What does DeFi stand for?",
        "q_fr": "Que signifie DeFi ?",
        "options": ["Digital Finance", "Decentralized Finance", "Deferred Finance", "Defined Finance"],
        "options_fr": ["Finance Digitale", "Finance Décentralisée", "Finance Différée", "Finance Définie"],
        "answer": 1,
        "explanation": "DeFi = Decentralized Finance. Financial services without banks, on the blockchain.",
        "explanation_fr": "DeFi = Finance Décentralisée. Des services financiers sans banque, sur la blockchain."
    },
    {
        "q": "Who created Bitcoin?",
        "q_fr": "Qui a créé Bitcoin ?",
        "options": ["Elon Musk", "Vitalik Buterin", "Satoshi Nakamoto", "CZ"],
        "options_fr": ["Elon Musk", "Vitalik Buterin", "Satoshi Nakamoto", "CZ"],
        "answer": 2,
        "explanation": "Satoshi Nakamoto is the anonymous creator of Bitcoin in 2009.",
        "explanation_fr": "Satoshi Nakamoto est le pseudonyme du créateur anonyme de Bitcoin en 2009."
    },
    {
        "q": "What is Binance's native token?",
        "q_fr": "Quel est le token natif de Binance ?",
        "options": ["BTC", "ETH", "USDT", "BNB"],
        "options_fr": ["BTC", "ETH", "USDT", "BNB"],
        "answer": 3,
        "explanation": "BNB (Binance Coin) is the official token of the Binance ecosystem.",
        "explanation_fr": "BNB (Binance Coin) est le token officiel de l'écosystème Binance."
    },
    {
        "q": "What does HODL mean in crypto?",
        "q_fr": "Que veut dire HODL en crypto ?",
        "options": ["Sell quickly", "Hold your crypto long-term", "Buy in bulk", "Analyze the market"],
        "options_fr": ["Vendre rapidement", "Garder ses cryptos longtemps", "Acheter en masse", "Analyser le marché"],
        "answer": 1,
        "explanation": "HODL comes from a typo of HOLD. Strategy of keeping your crypto without panicking.",
        "explanation_fr": "HODL vient d'une faute de frappe de HOLD. Stratégie de garder ses cryptos sans paniquer."
    },
    {
        "q": "How many Bitcoins will ever exist?",
        "q_fr": "Combien de Bitcoin existeront au maximum ?",
        "options": ["10 million", "21 million", "100 million", "Unlimited"],
        "options_fr": ["10 millions", "21 millions", "100 millions", "Illimité"],
        "answer": 1,
        "explanation": "Bitcoin is limited to 21 million units, making it rare and deflationary.",
        "explanation_fr": "Bitcoin est limité à 21 millions d'unités, ce qui le rend rare et déflationniste."
    },
    {
        "q": "What is staking?",
        "q_fr": "Qu'est-ce que le staking ?",
        "options": ["Selling your crypto", "Locking crypto to validate the network", "Buying NFTs", "Trading"],
        "options_fr": ["Vendre ses cryptos", "Bloquer ses cryptos pour valider le réseau", "Acheter des NFTs", "Trader"],
        "answer": 1,
        "explanation": "Staking lets you earn passive rewards by validating a Proof of Stake network.",
        "explanation_fr": "Le staking permet de gagner des récompenses passives en validant un réseau Proof of Stake."
    },
    {
        "q": "What is Bitcoin halving?",
        "q_fr": "C'est quoi le halving Bitcoin ?",
        "options": ["Split Bitcoin in 2", "Halve the miner reward", "Double the supply", "Close the network"],
        "options_fr": ["Diviser Bitcoin en 2", "Réduire de moitié la récompense des mineurs", "Doubler l'offre", "Fermer le réseau"],
        "answer": 1,
        "explanation": "Halving cuts miner rewards in half every 4 years, reducing BTC inflation.",
        "explanation_fr": "Le halving divise par 2 la récompense des mineurs tous les 4 ans, réduisant l'inflation de BTC."
    },
]

XP_PER_CORRECT = 15

def get_random_quiz():
    import random
    return random.choice(QUIZ_BANK)

def check_answer(quiz, answer_index):
    return answer_index == quiz["answer"]
