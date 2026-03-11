"""
BinanceQuest AI — Telegram Bot (FR/EN)
"""

import logging
import random
import requests
from datetime import time
from anthropic import Anthropic
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

import os
TELEGRAM_TOKEN    = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
DAILY_QUIZ_HOUR   = 9
DAILY_QUIZ_MINUTE = 0

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
client = Anthropic(api_key=ANTHROPIC_API_KEY)

# ─── STOCKAGE ─────────────────────────────────────────────────────────────────
user_data = {}

def get_user(uid, telegram_lang=None):
    if uid not in user_data:
        # Auto-detect from Telegram language code
        lang = "en" if (telegram_lang and telegram_lang.startswith("en")) else "fr"
        user_data[uid] = {"xp": 0, "streak": 0, "chat_history": [], "portfolio": {}, "lang": lang}
    return user_data[uid]

# ─── LANGUE ───────────────────────────────────────────────────────────────────
def get_lang(uid):
    return get_user(uid).get("lang", "fr")

def set_lang(uid, lang):
    get_user(uid)["lang"] = lang

def detect_lang(text):
    en_words = ["what","how","why","who","when","where","is","are","the","bitcoin","crypto","help","price","start"]
    fr_words = ["quoi","comment","pourquoi","qui","quand","est","sont","le","la","les","bonjour","merci","prix"]
    text_lower = text.lower()
    en_score = sum(1 for w in en_words if w in text_lower)
    fr_score = sum(1 for w in fr_words if w in text_lower)
    return "en" if en_score > fr_score else "fr"

# ─── DONNÉES ÉDUCATIVES ───────────────────────────────────────────────────────
QUIZ_BANK = [
    {"q": "What does DeFi stand for?", "q_fr": "Que signifie DeFi ?",
     "options": ["Digital Finance","Decentralized Finance","Deferred Finance","Defined Finance"],
     "options_fr": ["Finance Digitale","Finance Décentralisée","Finance Différée","Finance Définie"],
     "answer": 1, "explanation": "DeFi = Decentralized Finance. Financial services without banks, on the blockchain.", "explanation_fr": "DeFi = Finance Décentralisée. Des services financiers sans banque, sur la blockchain."},
    {"q": "Who created Bitcoin?", "q_fr": "Qui a créé Bitcoin ?",
     "options": ["Elon Musk","Vitalik Buterin","Satoshi Nakamoto","CZ"],
     "options_fr": ["Elon Musk","Vitalik Buterin","Satoshi Nakamoto","CZ"],
     "answer": 2, "explanation": "Satoshi Nakamoto is the anonymous creator of Bitcoin in 2009.", "explanation_fr": "Satoshi Nakamoto est le pseudonyme du créateur anonyme de Bitcoin en 2009."},
    {"q": "What is Binance's native token?", "q_fr": "Quel est le token natif de Binance ?",
     "options": ["BTC","ETH","USDT","BNB"],
     "options_fr": ["BTC","ETH","USDT","BNB"],
     "answer": 3, "explanation": "BNB (Binance Coin) is the official token of the Binance ecosystem.", "explanation_fr": "BNB (Binance Coin) est le token officiel de l'écosystème Binance."},
    {"q": "What does HODL mean in crypto?", "q_fr": "Que veut dire HODL en crypto ?",
     "options": ["Sell quickly","Hold your crypto long-term","Buy in bulk","Analyze the market"],
     "options_fr": ["Vendre rapidement","Garder ses cryptos longtemps","Acheter en masse","Analyser le marché"],
     "answer": 1, "explanation": "HODL comes from a typo of HOLD. Strategy of keeping your crypto without panicking.", "explanation_fr": "HODL vient d'une faute de frappe de HOLD. Stratégie de garder ses cryptos sans paniquer."},
    {"q": "How many Bitcoins will ever exist?", "q_fr": "Combien de Bitcoin existeront au maximum ?",
     "options": ["10 million","21 million","100 million","Unlimited"],
     "options_fr": ["10 millions","21 millions","100 millions","Illimité"],
     "answer": 1, "explanation": "Bitcoin is limited to 21 million units, making it rare and deflationary.", "explanation_fr": "Bitcoin est limité à 21 millions d'unités, ce qui le rend rare et déflationniste."},
    {"q": "What is a crypto wallet?", "q_fr": "Qu'est-ce qu'un wallet crypto ?",
     "options": ["An exchange","A digital wallet","A type of blockchain","A token"],
     "options_fr": ["Un exchange","Un portefeuille numérique","Un type de blockchain","Un token"],
     "answer": 1, "explanation": "A wallet stores your private keys that give access to your crypto.", "explanation_fr": "Un wallet stocke vos clés privées qui donnent accès à vos cryptos."},
    {"q": "What does RSI measure?", "q_fr": "Que mesure le RSI ?",
     "options": ["Future price","Network speed","Overbought/oversold conditions","Volume"],
     "options_fr": ["Prix futur","Vitesse réseau","Conditions de surachat/survente","Volume"],
     "answer": 2, "explanation": "RSI > 70 = overbought, RSI < 30 = oversold. Useful for anticipating reversals.", "explanation_fr": "RSI > 70 = suracheté, RSI < 30 = survendu. Utile pour anticiper des retournements."},
    {"q": "What is staking?", "q_fr": "Qu'est-ce que le staking ?",
     "options": ["Selling your crypto","Locking crypto to validate the network","Buying NFTs","Trading"],
     "options_fr": ["Vendre ses cryptos","Bloquer ses cryptos pour valider le réseau","Acheter des NFTs","Trader"],
     "answer": 1, "explanation": "Staking lets you earn passive rewards by validating a Proof of Stake network.", "explanation_fr": "Le staking permet de gagner des récompenses passives en validant un réseau Proof of Stake."},
    {"q": "When was Binance founded?", "q_fr": "Binance a été fondé en quelle année ?",
     "options": ["2009","2013","2017","2020"],
     "options_fr": ["2009","2013","2017","2020"],
     "answer": 2, "explanation": "Binance was founded in 2017 by Changpeng Zhao (CZ).", "explanation_fr": "Binance a été fondé en 2017 par Changpeng Zhao (CZ)."},
    {"q": "What is an NFT?", "q_fr": "Qu'est-ce qu'un NFT ?",
     "options": ["A crypto like Bitcoin","A non-fungible token (unique)","A type of wallet","A stablecoin"],
     "options_fr": ["Une crypto comme Bitcoin","Un token non-fongible (unique)","Un type de wallet","Un stablecoin"],
     "answer": 1, "explanation": "NFT = Non-Fungible Token. A unique digital asset, often used for digital art.", "explanation_fr": "NFT = Non-Fungible Token. Actif numérique unique, souvent utilisé pour l'art digital."},
    {"q": "What is a bull market?", "q_fr": "Que signifie bull market ?",
     "options": ["Falling market","Rising market","Stable market","Closed market"],
     "options_fr": ["Marché baissier","Marché haussier","Marché stable","Marché fermé"],
     "answer": 1, "explanation": "Bull market = rising market. Prices are increasing significantly.", "explanation_fr": "Bull market = marché haussier. Les prix augmentent significativement."},
    {"q": "What is Bitcoin halving?", "q_fr": "C'est quoi le halving Bitcoin ?",
     "options": ["Split Bitcoin in 2","Halve the miner reward","Double the supply","Close the network"],
     "options_fr": ["Diviser Bitcoin en 2","Réduire de moitié la récompense des mineurs","Doubler l'offre","Fermer le réseau"],
     "answer": 1, "explanation": "Halving cuts miner rewards in half every 4 years, reducing BTC inflation.", "explanation_fr": "Le halving divise par 2 la récompense des mineurs tous les 4 ans, réduisant l'inflation de BTC."},
]

LESSONS = [
    {"title": "Bitcoin", "content": "Bitcoin is the 1st cryptocurrency (2009). Limited to 21M units, decentralized, secured by blockchain. Satoshi Nakamoto is its anonymous creator.", "content_fr": "Bitcoin est la 1ère cryptomonnaie (2009). Limité à 21M d'unités, décentralisé, sécurisé par la blockchain. Satoshi Nakamoto en est le créateur anonyme."},
    {"title": "Binance & BNB", "content": "Binance is the world's largest crypto exchange, founded by CZ in 2017. BNB is its native token — fees, IEO, staking and much more.", "content_fr": "Binance est le plus grand exchange crypto au monde, fondé par CZ en 2017. BNB est son token natif — frais, IEO, staking et bien plus."},
    {"title": "Blockchain", "content": "A distributed digital ledger shared across thousands of computers. Each transaction is grouped into blocks, chained and immutable. Transparent and secure.", "content_fr": "Registre numérique distribué entre des milliers d'ordinateurs. Chaque transaction est regroupée en blocs, chaînés et immuables. Transparent et sécurisé."},
    {"title": "Spot vs Futures", "content": "Spot: you actually buy the asset. Futures: you speculate on its future price with leverage. Futures amplify both gains AND losses — high risk!", "content_fr": "Spot : vous achetez l'actif réellement. Futures : vous spéculez sur son prix futur avec du levier. Les futures amplifient gains ET pertes — risque élevé !"},
    {"title": "DeFi", "content": "Decentralized Finance = financial services without banks. Smart contracts automate everything: loans, borrowing, trading. Accessible 24/7 to everyone.", "content_fr": "Finance Décentralisée = services financiers sans banque. Les smart contracts automatisent tout : prêts, emprunts, échanges. Accessible 24h/24 à tous."},
    {"title": "Staking", "content": "Lock your crypto to help validate the Proof of Stake network. In return, you receive regular rewards. Binance Earn simplifies staking.", "content_fr": "Bloquez vos cryptos pour aider à valider le réseau Proof of Stake. En échange, vous recevez des récompenses régulières. Binance Earn simplifie le staking."},
    {"title": "Technical Analysis", "content": "Study of charts to anticipate price movements. Key indicators: RSI, moving averages, Bollinger Bands, supports and resistances.", "content_fr": "Étude des graphiques pour anticiper les mouvements. Indicateurs clés : RSI, moyennes mobiles, bandes de Bollinger, supports et résistances."},
    {"title": "Crypto Security", "content": "Golden rules: enable 2FA, use a hardware wallet for large sums, NEVER share your private key, beware of scams.", "content_fr": "Règles d'or : activez le 2FA, utilisez un hardware wallet pour les grosses sommes, ne partagez JAMAIS votre clé privée, méfiez-vous des arnaques."},
]

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def xp_to_level(xp):
    if xp < 50: return 1
    elif xp < 150: return 2
    elif xp < 300: return 3
    elif xp < 500: return 4
    else: return 5

def level_label(level, lang="en"):
    fr = ["","Débutant","Intermédiaire","Avancé","Expert","Master"]
    en = ["","Beginner","Intermediate","Advanced","Expert","Master"]
    return (en if lang=="en" else fr)[level]

def get_crypto_prices():
    symbols = {"BTCUSDT":"bitcoin","ETHUSDT":"ethereum","BNBUSDT":"binancecoin","SOLUSDT":"solana","XRPUSDT":"ripple"}
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=8)
        data = r.json()
        result = {}
        for item in data:
            sym = item.get("symbol","")
            if sym in symbols:
                key = symbols[sym]
                result[key] = {"usd": float(item["lastPrice"]), "usd_24h_change": float(item["priceChangePercent"])}
        return result if result else None
    except:
        return None

def ask_claude(system, messages):
    try:
        r = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=1000, system=system, messages=messages)
        return r.content[0].text
    except Exception as e:
        return f"AI Error: {e}"

def main_keyboard(uid=0):
    en = get_lang(uid) == "en"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎯 Quiz", callback_data="menu_quiz"),
         InlineKeyboardButton("📖 " + ("Lesson" if en else "Leçon"), callback_data="menu_lesson")],
        [InlineKeyboardButton("💰 " + ("Prices" if en else "Prix"), callback_data="menu_prix"),
         InlineKeyboardButton("📰 News", callback_data="menu_news")],
        [InlineKeyboardButton("⚖️ " + ("Portfolio" if en else "Portefeuille"), callback_data="menu_portfolio"),
         InlineKeyboardButton("🏅 " + ("Profile" if en else "Profil"), callback_data="menu_profil")],
        [InlineKeyboardButton("🤖 " + ("Ask AI" if en else "Poser une question à l'IA"), callback_data="menu_ia")],
        [InlineKeyboardButton("🇫🇷 Français", callback_data="lang_fr"),
         InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
    ])

# ─── COMMANDES ────────────────────────────────────────────────────────────────
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    tg_lang = update.effective_user.language_code
    user = get_user(uid, tg_lang)
    name = update.effective_user.first_name
    en = get_lang(uid) == "en"
    text = (
        f"BinanceQuest AI - Welcome {name}!\n\n"
        f"{'Crypto education assistant based on Binance Academy.' if en else 'Assistant educatif crypto base sur Binance Academy.'}\n\n"
        f"Level: {level_label(xp_to_level(user['xp']))}\n"
        f"XP: {user['xp']}\n\n"
        f"{'What would you like to do?' if en else 'Que veux-tu faire ?'}"
    )
    await update.message.reply_text(text, reply_markup=main_keyboard(uid))

async def cmd_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    en = get_lang(uid) == "en"
    q = random.choice(QUIZ_BANK)
    context.user_data["current_quiz"] = q
    options = q["options"] if en else q.get("options_fr", q["options"])
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(opt, callback_data=f"quiz_{i}")] for i, opt in enumerate(options)])
    question = q["q"] if en else q["q_fr"]
    text = f"🎯 Quiz\n\n{question}"
    if update.message:
        await update.message.reply_text(text, reply_markup=keyboard)
    else:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

async def cmd_lecon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    en = get_lang(uid) == "en"
    lesson = random.choice(LESSONS)
    content = lesson["content"] if en else lesson["content_fr"]
    text = f"{'Lesson of the day' if en else 'Lecon du jour'}: {lesson['title']}\n\n{content}\n\n{'Questions? Write them!' if en else 'Des questions ? Ecris-les !'}"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🎯 Quiz", callback_data="menu_quiz"), InlineKeyboardButton("📖 " + ("Another lesson" if en else "Autre leçon"), callback_data="menu_lesson")], [InlineKeyboardButton("🏠 Menu", callback_data="menu_home")]])
    if update.message:
        await update.message.reply_text(text, reply_markup=keyboard)
    else:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

async def cmd_prix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    en = get_lang(uid) == "en"
    prices = get_crypto_prices()
    if not prices:
        text = "Unable to fetch prices. Try again shortly." if en else "Impossible de recuperer les prix. Reessaie dans quelques instants."
    else:
        def fmt(cid, name, sym):
            d = prices.get(cid, {})
            p, c = d.get("usd", 0), d.get("usd_24h_change", 0)
            arrow = "+" if c >= 0 else ""
            emoji = "🟢" if c >= 0 else "🔴"
            return f"{emoji} {name} ({sym}): ${p:,.2f} ({arrow}{c:.2f}%)"
        title = "Live Crypto Prices" if en else "Prix Crypto en Direct"
        text = f"{title}\n\n{fmt('bitcoin','Bitcoin','BTC')}\n{fmt('ethereum','Ethereum','ETH')}\n{fmt('binancecoin','BNB','BNB')}\n{fmt('solana','Solana','SOL')}\n{fmt('ripple','XRP','XRP')}\n\nSource: Binance API"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Refresh" if en else "Actualiser", callback_data="menu_prix"), InlineKeyboardButton("News", callback_data="menu_news")]])
    if update.message:
        await update.message.reply_text(text, reply_markup=keyboard)
    else:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

async def cmd_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    en = get_lang(uid) == "en"
    prices = get_crypto_prices()
    price_ctx = ""
    if prices:
        btc = prices.get("bitcoin", {})
        eth = prices.get("ethereum", {})
        bnb = prices.get("binancecoin", {})
        price_ctx = f"BTC ${btc.get('usd',0):,.0f} ({btc.get('usd_24h_change',0):+.1f}%), ETH ${eth.get('usd',0):,.0f} ({eth.get('usd_24h_change',0):+.1f}%), BNB ${bnb.get('usd',0):,.0f} ({bnb.get('usd_24h_change',0):+.1f}%)"

    if update.message:
        await update.message.reply_text("Market analysis in progress..." if en else "Analyse du marche en cours...")
    else:
        await update.callback_query.answer("Loading..." if en else "Chargement...")

    lang_instr = "IMPORTANT: You MUST respond ONLY in English. Never use French words." if en else "IMPORTANT: Tu DOIS répondre UNIQUEMENT en français. N'utilise jamais de mots anglais dans ta réponse."
    analysis = ask_claude(
        f"You are BinanceQuest AI, crypto expert. {lang_instr} Give a concise market briefing: 1) Market sentiment 2) Key points 3) Educational opportunity. Factual, educational, no financial advice. Max 250 words.",
        [{"role": "user", "content": f"Analyze the crypto market. Current prices: {price_ctx}"}]
    )
    title = "Market News" if en else "News Marche"
    warning = "Not financial advice." if en else "Pas un conseil financier."
    text = f"📰 {title}\n\n{analysis}\n\n{warning}"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Prices" if en else "Prix", callback_data="menu_prix"), InlineKeyboardButton("New analysis" if en else "Nouvelle analyse", callback_data="menu_news")]])
    await context.bot.send_message(update.effective_chat.id, text, reply_markup=keyboard)

async def cmd_portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    en = get_lang(uid) == "en"
    user = get_user(uid)
    portfolio = user.get("portfolio", {})

    if not portfolio:
        text = ("Portfolio empty!\n\nAdd your crypto:\n/ajout BTC 0.5\n/ajout ETH 2" if en else "Portefeuille vide!\n\nAjoute tes cryptos:\n/ajout BTC 0.5\n/ajout ETH 2")
        if update.message:
            await update.message.reply_text(text)
        else:
            await update.callback_query.edit_message_text(text)
        return

    prices = get_crypto_prices()
    coin_ids = {"BTC":"bitcoin","ETH":"ethereum","BNB":"binancecoin","SOL":"solana","XRP":"ripple"}
    total, lines = 0, []
    for coin, qty in portfolio.items():
        cid = coin_ids.get(coin.upper())
        price = prices.get(cid, {}).get("usd", 0) if prices and cid else 0
        value = price * qty
        total += value
        lines.append(f"{coin.upper()}: {qty} x ${price:,.2f} = ${value:,.2f}")

    title = "My Portfolio" if en else "Mon Portefeuille"
    total_label = "Total value" if en else "Valeur totale"
    text = f"💼 {title}\n\n" + "\n".join(lines) + f"\n\n{total_label}: ${total:,.2f}"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Analyze & Rebalance" if en else "Analyser & Reequilibrer", callback_data="portfolio_rebalance")]])
    if update.message:
        await update.message.reply_text(text, reply_markup=keyboard)
    else:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

async def cmd_ajout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    en = get_lang(uid) == "en"
    user = get_user(uid)
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Format: /ajout BTC 0.5")
        return
    try:
        coin, qty = args[0].upper(), float(args[1])
        user["portfolio"][coin] = qty
        await update.message.reply_text(f"{qty} {coin} {'added!' if en else 'ajoute!'}\n\n/portfolio")
    except:
        await update.message.reply_text("Invalid format. Ex: /ajout BTC 0.5")

async def cmd_profil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    en = get_lang(uid) == "en"
    user = get_user(uid)
    level = xp_to_level(user["xp"])
    badges = "".join(b for b, t in [("Beginner",20),("Inter",60),("Advanced",150),("Expert",300),("Master",500)] if user["xp"] >= t) or ("None yet" if en else "Aucun encore")
    title = "Your Profile" if en else "Ton Profil"
    text = f"{title} BinanceQuest\n\nLevel: {level_label(level)}\nXP: {user['xp']}\nStreak: {user['streak']} {'days' if en else 'jours'}\nBadges: {badges}\n\n{'Keep learning!' if en else 'Continue a apprendre!'}"
    if update.message:
        await update.message.reply_text(text)
    else:
        await update.callback_query.edit_message_text(text)

async def handle_free_question(update, context, question):
    uid = update.effective_user.id
    en = get_lang(uid) == "en"
    user = get_user(uid)
    history = user["chat_history"][-6:]
    messages = history + [{"role": "user", "content": question}]
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    lang_instr = "IMPORTANT: You MUST respond ONLY in English. Never use French words." if en else "IMPORTANT: Tu DOIS répondre UNIQUEMENT en français. N'utilise jamais de mots anglais dans ta réponse."
    reply = ask_claude(
        f"You are BinanceQuest AI, crypto education assistant based on Binance Academy. {lang_instr} Be clear, educational and encouraging. No direct financial advice. Max 200 words.",
        messages
    )
    user["chat_history"] += [{"role":"user","content":question},{"role":"assistant","content":reply}]
    user["chat_history"] = user["chat_history"][-20:]
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🎯 Quiz", callback_data="menu_quiz"), InlineKeyboardButton("🏠 Menu", callback_data="menu_home")]])
    await update.message.reply_text(reply, reply_markup=keyboard)

async def handle_rebalance(update, context):
    uid = update.effective_user.id
    en = get_lang(uid) == "en"
    user = get_user(uid)
    portfolio = user.get("portfolio", {})
    if not portfolio:
        await update.callback_query.edit_message_text("Empty portfolio. Add crypto with /ajout BTC 0.5")
        return
    prices = get_crypto_prices()
    coin_ids = {"BTC":"bitcoin","ETH":"ethereum","BNB":"binancecoin","SOL":"solana","XRP":"ripple"}
    total, lines = 0, []
    for coin, qty in portfolio.items():
        cid = coin_ids.get(coin.upper())
        price = prices.get(cid, {}).get("usd", 0) if prices and cid else 0
        change = prices.get(cid, {}).get("usd_24h_change", 0) if prices and cid else 0
        value = price * qty
        total += value
        lines.append(f"{coin}: {qty} units, ${value:.2f}, {change:+.1f}% 24h")
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    lang_instr = "IMPORTANT: You MUST respond ONLY in English. Never use French words." if en else "IMPORTANT: Tu DOIS répondre UNIQUEMENT en français. N'utilise jamais de mots anglais dans ta réponse."
    analysis = ask_claude(
        f"You are BinanceQuest AI, crypto portfolio expert. {lang_instr} Analyze the portfolio and give educational rebalancing suggestions: diversification, concentration risks, DCA principles. No direct financial advice. Max 250 words.",
        [{"role":"user","content":f"Portfolio (total ${total:.2f}):\n" + "\n".join(lines)}]
    )
    title = "Portfolio Analysis" if en else "Analyse du Portefeuille"
    warning = "Educational only, not financial advice." if en else "Educatif uniquement, pas un conseil financier."
    text = f"📰 {title}\n\n{analysis}\n\n{warning}"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔄 " + ("Refresh" if en else "Actualiser"), callback_data="menu_prix"), InlineKeyboardButton("📰 News", callback_data="menu_news")], [InlineKeyboardButton("🏠 Menu", callback_data="menu_home")]])
    await context.bot.send_message(update.effective_chat.id, text, reply_markup=keyboard)

# ─── CALLBACKS ────────────────────────────────────────────────────────────────
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    data = update.callback_query.data
    uid = update.effective_user.id
    en = get_lang(uid) == "en"

    if data == "lang_fr":
        set_lang(uid, "fr")
        await update.callback_query.edit_message_text("Langue: Francais active! Tape /start pour le menu.")
        return
    elif data == "lang_en":
        set_lang(uid, "en")
        await update.callback_query.edit_message_text("Language: English activated! Type /start for the menu.")
        return

    routes = {"menu_quiz": cmd_quiz, "menu_lesson": cmd_lecon, "menu_prix": cmd_prix, "menu_news": cmd_news, "menu_portfolio": cmd_portfolio, "menu_profil": cmd_profil}
    if data in routes:
        await routes[data](update, context)
    elif data == "menu_home":
        await update.callback_query.edit_message_text("Type /start for the main menu." if en else "Tape /start pour revenir au menu.")
    elif data == "menu_ia":
        await update.callback_query.edit_message_text("Ask your question directly in the chat!" if en else "Pose ta question directement dans le chat!")
    elif data == "portfolio_rebalance":
        await handle_rebalance(update, context)
    elif data.startswith("quiz_"):
        q = context.user_data.get("current_quiz")
        if not q:
            await update.callback_query.edit_message_text("Quiz expired. Start a new one with /quiz")
            return
        chosen = int(data.split("_")[1])
        correct = chosen == q["answer"]
        user = get_user(uid)
        if correct:
            user["xp"] += 15
        explanation = q["explanation"] if en else q["explanation_fr"]
        result_line = ("Correct!" if correct else f"Wrong. Correct answer: {q['options'][q['answer']]}") if en else ("Bonne reponse!" if correct else f"Mauvaise reponse. Bonne reponse: {q['options'][q['answer']]}")
        text = f"{result_line}\n\nExplanation: {explanation}\n\nXP: {user['xp']} | ⚡ {level_label(xp_to_level(user['xp']))}"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🎯 " + ("Next question" if en else "Autre question"), callback_data="menu_quiz"), InlineKeyboardButton("📖 " + ("Lesson" if en else "Leçon"), callback_data="menu_lesson")], [InlineKeyboardButton("🏠 Menu", callback_data="menu_home")]])
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.startswith("/"):
        return
    text = update.message.text.strip()
    uid = update.effective_user.id
    if detect_lang(text) == "en":
        set_lang(uid, "en")
    await handle_free_question(update, context, text)

# ─── QUIZ QUOTIDIEN ───────────────────────────────────────────────────────────
async def daily_quiz_job(context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(QUIZ_BANK)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(opt, callback_data=f"quiz_{i}")] for i, opt in enumerate(q["options"])])
    for uid in list(user_data.keys()):
        en = get_lang(uid) == "en"
        question = q["q"] if en else q["q_fr"]
        try:
            await context.bot.send_message(uid, f"Daily Quiz BinanceQuest!\n\n{question}", reply_markup=keyboard)
        except Exception as e:
            logger.warning(f"Cannot send to {uid}: {e}")

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    for cmd, handler in [("start",cmd_start),("quiz",cmd_quiz),("lecon",cmd_lecon),("prix",cmd_prix),("news",cmd_news),("portfolio",cmd_portfolio),("ajout",cmd_ajout),("profil",cmd_profil)]:
        app.add_handler(CommandHandler(cmd, handler))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.job_queue.run_daily(daily_quiz_job, time=time(hour=DAILY_QUIZ_HOUR, minute=DAILY_QUIZ_MINUTE))
    print("BinanceQuest AI Bot started!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
