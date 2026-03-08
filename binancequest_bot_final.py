"""
BinanceQuest AI — Telegram Bot
================================
Fonctionnalités :
- 🎓 Quiz éducatif (Binance Academy)
- 🤖 Assistant IA libre (Claude API)
- 📅 Quiz quotidien automatique
- ⚖️ Rééquilibrage de portefeuille
- 📰 News & opportunités du marché

Installation :
    pip install python-telegram-bot anthropic requests

Configuration :
    Remplacez TELEGRAM_TOKEN et ANTHROPIC_API_KEY par vos vraies clés.

Lancement :
    python binancequest_bot.py
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

# ─── CONFIG ───────────────────────────────────────────────────────────────────
import os
TELEGRAM_TOKEN    = os.environ.get("TELEGRAM_TOKEN")   # ⚠️ Révoquez l'ancien et mettez le nouveau
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")    # console.anthropic.com
DAILY_QUIZ_HOUR   = 9
DAILY_QUIZ_MINUTE = 0

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
client = Anthropic(api_key=ANTHROPIC_API_KEY)


# ─── LANGUE / LANGUAGE ────────────────────────────────────────────────────────
def get_lang(uid):
    """Get language from persistent user_data"""
    return get_user(uid).get('lang', 'fr')

def set_lang(uid, lang):
    """Save language in persistent user_data"""
    get_user(uid)['lang'] = lang

def t(uid, fr, en):
    return en if get_lang(uid) == 'en' else fr

def detect_lang(text):
    en_words = ['what', 'how', 'why', 'who', 'when', 'where', 'is', 'are', 'the', 'bitcoin', 'crypto', 'help', 'price', 'start']
    fr_words = ['quoi', 'comment', 'pourquoi', 'qui', 'quand', 'est', 'sont', 'le', 'la', 'les', 'bonjour', 'merci', 'prix']
    text_lower = text.lower()
    en_score = sum(1 for w in en_words if w in text_lower)
    fr_score = sum(1 for w in fr_words if w in text_lower)
    return 'en' if en_score > fr_score else 'fr'

# ─── DONNÉES ÉDUCATIVES ───────────────────────────────────────────────────────
QUIZ_BANK = [
    {"q": "Que signifie DeFi ?", "options": ["Digital Finance","Decentralized Finance","Deferred Finance","Defined Finance"], "answer": 1, "explanation": "DeFi = Finance Décentralisée. Des services financiers sans banque, sur la blockchain."},
    {"q": "Qui a créé Bitcoin ?", "options": ["Elon Musk","Vitalik Buterin","Satoshi Nakamoto","CZ"], "answer": 2, "explanation": "Satoshi Nakamoto est le pseudonyme du créateur anonyme de Bitcoin en 2009."},
    {"q": "Quel est le token natif de Binance ?", "options": ["BTC","ETH","USDT","BNB"], "answer": 3, "explanation": "BNB (Binance Coin) est le token officiel de l'écosystème Binance."},
    {"q": "Que veut dire 'HODL' en crypto ?", "options": ["Vendre rapidement","Garder ses cryptos longtemps","Acheter en masse","Analyser le marché"], "answer": 1, "explanation": "HODL vient d'une faute de frappe de 'HOLD'. Stratégie de garder ses cryptos sans paniquer."},
    {"q": "Combien de Bitcoin existeront au maximum ?", "options": ["10 millions","21 millions","100 millions","Illimité"], "answer": 1, "explanation": "Bitcoin est limité à 21 millions d'unités, ce qui le rend rare et déflationniste."},
    {"q": "Qu'est-ce qu'un wallet crypto ?", "options": ["Un exchange","Un portefeuille numérique","Un type de blockchain","Un token"], "answer": 1, "explanation": "Un wallet stocke vos clés privées qui donnent accès à vos cryptos."},
    {"q": "Que mesure le RSI ?", "options": ["Le prix futur","La vitesse du réseau","Les conditions de surachat/survente","Le volume"], "answer": 2, "explanation": "RSI > 70 = suracheté, RSI < 30 = survendu. Utile pour anticiper des retournements."},
    {"q": "Qu'est-ce que le staking ?", "options": ["Vendre ses cryptos","Bloquer ses cryptos pour valider le réseau","Acheter des NFT","Faire du trading"], "answer": 1, "explanation": "Le staking permet de gagner des récompenses passives en validant un réseau Proof of Stake."},
    {"q": "Binance a été fondé en quelle année ?", "options": ["2009","2013","2017","2020"], "answer": 2, "explanation": "Binance a été fondé en 2017 par Changpeng Zhao (CZ)."},
    {"q": "Qu'est-ce qu'un NFT ?", "options": ["Une crypto comme Bitcoin","Un token non fongible (unique)","Un type de wallet","Une stablecoin"], "answer": 1, "explanation": "NFT = Non-Fungible Token. Actif numérique unique, souvent utilisé pour l'art digital."},
    {"q": "Que signifie 'bull market' ?", "options": ["Marché en baisse","Marché en hausse","Marché stable","Marché fermé"], "answer": 1, "explanation": "Bull market = marché haussier. Les prix augmentent significativement."},
    {"q": "C'est quoi le halving Bitcoin ?", "options": ["Diviser Bitcoin en 2","Réduire de moitié la récompense des mineurs","Doubler l'offre","Fermer le réseau"], "answer": 1, "explanation": "Le halving divise par 2 la récompense des mineurs tous les ~4 ans, réduisant l'inflation de BTC."},
]

LESSONS = [
    {"title": "₿ Bitcoin", "content": "Bitcoin est la 1ère cryptomonnaie (2009). Limité à 21M d'unités, décentralisé, sécurisé par la blockchain. Satoshi Nakamoto en est le créateur anonyme."},
    {"title": "🔶 Binance & BNB", "content": "Binance est le plus grand exchange crypto au monde, fondé par CZ en 2017. BNB est son token natif — frais, IEO, staking et bien plus."},
    {"title": "⛓️ Blockchain", "content": "Registre numérique distribué entre des milliers d'ordinateurs. Chaque transaction est regroupée en blocs, chaînés et immuables. Transparent et sécurisé."},
    {"title": "📊 Spot vs Futures", "content": "Spot : vous achetez l'actif réellement. Futures : vous spéculez sur son prix futur avec du levier. Les futures amplifient gains ET pertes — risque élevé !"},
    {"title": "🏦 DeFi", "content": "Finance Décentralisée = services financiers sans banque. Les smart contracts automatisent tout : prêts, emprunts, échanges. Accessible 24h/24 à tous."},
    {"title": "🥩 Staking", "content": "Bloquez vos cryptos pour aider à valider le réseau Proof of Stake. En échange, vous recevez des récompenses régulières. Binance Earn simplifie le staking."},
    {"title": "📈 Analyse Technique", "content": "Étude des graphiques pour anticiper les mouvements. Indicateurs clés : RSI, moyennes mobiles, bandes de Bollinger, supports & résistances."},
    {"title": "🔒 Sécurité Crypto", "content": "Règles d'or : activez le 2FA, utilisez un hardware wallet pour les grosses sommes, ne partagez JAMAIS votre clé privée, méfiez-vous des arnaques."},
]

# ─── STOCKAGE EN MÉMOIRE (remplacer par une DB en production) ─────────────────
user_data = {}

def get_user(uid):
    if uid not in user_data:
        user_data[uid] = {"xp": 0, "streak": 0, "chat_history": [], "portfolio": {}}
    return user_data[uid]

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def xp_to_level(xp):
    if xp < 50: return 1
    elif xp < 150: return 2
    elif xp < 300: return 3
    elif xp < 500: return 4
    else: return 5

def level_label(level):
    return ["","🌱 Débutant","⚡ Intermédiaire","🔥 Avancé","💎 Expert","🏆 Master"][level]

def get_crypto_prices():
    """Récupère les prix via l'API officielle Binance"""
    symbols = {"BTCUSDT":"bitcoin","ETHUSDT":"ethereum","BNBUSDT":"binancecoin","SOLUSDT":"solana","XRPUSDT":"ripple"}
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=8)
        data = r.json()
        result = {}
        for item in data:
            sym = item.get("symbol","")
            if sym in symbols:
                key = symbols[sym]
                result[key] = {
                    "usd": float(item["lastPrice"]),
                    "usd_24h_change": float(item["priceChangePercent"])
                }
        return result if result else None
    except:
        return None

def ask_claude(system, messages):
    try:
        r = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=system,
            messages=messages
        )
        return r.content[0].text
    except Exception as e:
        return f"❌ Erreur IA : {e}"

def main_keyboard(uid=0):
    lang = get_lang(uid)
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎓 Quiz", callback_data="menu_quiz"),
         InlineKeyboardButton("📖 " + ("Lesson" if lang=="en" else "Leçon"), callback_data="menu_lesson")],
        [InlineKeyboardButton("💰 " + ("Prices" if lang=="en" else "Prix"), callback_data="menu_prix"),
         InlineKeyboardButton("📰 News", callback_data="menu_news")],
        [InlineKeyboardButton("⚖️ " + ("Portfolio" if lang=="en" else "Portefeuille"), callback_data="menu_portfolio"),
         InlineKeyboardButton("🏅 " + ("Profile" if lang=="en" else "Profil"), callback_data="menu_profil")],
        [InlineKeyboardButton("🤖 " + ("Ask AI" if lang=="en" else "Poser une question à l'IA"), callback_data="menu_ia")],
        [InlineKeyboardButton("🇫🇷 Français", callback_data="lang_fr"),
         InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
    ])

# ─── COMMANDES ────────────────────────────────────────────────────────────────
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid)
    name = update.effective_user.first_name
    lang = get_lang(uid)
    text = (
        f"🏆 *{'Welcome to' if lang=='en' else 'Bienvenue sur'} BinanceQuest AI, {name} !*\n\n"
        f"{'Your crypto education assistant based on Binance Academy.' if lang=='en' else 'Ton assistant crypto éducatif basé sur Binance Academy.'}\n\n"
        f"*{'Level' if lang=='en' else 'Niveau'} :* {level_label(xp_to_level(user['xp']))}\n"
        f"*XP :* {user['xp']} ⚡\n\n"
        f"{'What would you like to do?' if lang=='en' else 'Que veux-tu faire ?'}"
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_keyboard(uid))

async def cmd_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(QUIZ_BANK)
    context.user_data["current_quiz"] = q
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(opt, callback_data=f"quiz_{i}")] for i, opt in enumerate(q["options"])])
    text = f"🎯 *Question Quiz*\n\n{q['q']}"
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def cmd_lecon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lesson = random.choice(LESSONS)
    text = f"📖 *Leçon du jour : {lesson['title']}*\n\n{lesson['content']}\n\n_Des questions ? Écris-les directement !_"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🎯 Quiz", callback_data="menu_quiz"), InlineKeyboardButton("📖 Autre leçon", callback_data="menu_lesson")]])
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def cmd_prix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prices = get_crypto_prices()
    if not prices:
        text = "❌ Impossible de récupérer les prix. Réessaie dans quelques instants."
    else:
        def fmt(cid, name, sym):
            d = prices.get(cid, {})
            p, c = d.get("usd", 0), d.get("usd_24h_change", 0)
            return f"{'🟢' if c >= 0 else '🔴'} *{name}* ({sym}) : ${p:,.2f} ({c:+.2f}%)"
        text = (
            f"💰 *Prix Crypto en Direct*\n_Mis à jour à l'instant_\n\n"
            f"{fmt('bitcoin','Bitcoin','BTC')}\n"
            f"{fmt('ethereum','Ethereum','ETH')}\n"
            f"{fmt('binancecoin','BNB','BNB')}\n"
            f"{fmt('solana','Solana','SOL')}\n"
            f"{fmt('ripple','XRP','XRP')}\n\n"
            f"_Source : Binance API_"
        )
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Actualiser", callback_data="menu_prix"), InlineKeyboardButton("📰 News", callback_data="menu_news")]])
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def cmd_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prices = get_crypto_prices()
    price_ctx = ""
    if prices:
        btc = prices.get("bitcoin", {})
        eth = prices.get("ethereum", {})
        bnb = prices.get("binancecoin", {})
        price_ctx = f"BTC ${btc.get('usd',0):,.0f} ({btc.get('usd_24h_change',0):+.1f}%), ETH ${eth.get('usd',0):,.0f} ({eth.get('usd_24h_change',0):+.1f}%), BNB ${bnb.get('usd',0):,.0f} ({bnb.get('usd_24h_change',0):+.1f}%)"

    if update.message:
        await update.message.reply_text("📰 Analyse du marché en cours... ⏳")
    else:
        await update.callback_query.answer("Chargement...")

    analysis = ask_claude(
        "Tu es BinanceQuest AI, expert crypto. Donne un briefing concis du marché : 1) Sentiment général 2) Points d'attention 3) Opportunité éducative à surveiller. Factuel, pédagogique, jamais alarmiste. Pas de conseils financiers. Max 250 mots.",
        [{"role": "user", "content": f"Analyse le marché crypto. Prix actuels : {price_ctx}"}]
    )
    text = f"📰 *News & Opportunités du Marché*\n\n{analysis}\n\n_⚠️ Ceci n'est pas un conseil financier._"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("💰 Prix", callback_data="menu_prix"), InlineKeyboardButton("🔄 Nouvelle analyse", callback_data="menu_news")]])
    await context.bot.send_message(update.effective_chat.id, text, parse_mode="Markdown", reply_markup=keyboard)

async def cmd_portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid)
    portfolio = user.get("portfolio", {})

    if not portfolio:
        text = ("⚖️ *Mon Portefeuille*\n\nTon portefeuille est vide !\n\nAjoute tes cryptos :\n`/ajout BTC 0.5`\n`/ajout ETH 2`\n`/ajout BNB 10`\n\n_Je t'aiderai à analyser et rééquilibrer !_")
        if update.message:
            await update.message.reply_text(text, parse_mode="Markdown")
        else:
            await update.callback_query.edit_message_text(text, parse_mode="Markdown")
        return

    prices = get_crypto_prices()
    coin_ids = {"BTC":"bitcoin","ETH":"ethereum","BNB":"binancecoin","SOL":"solana","XRP":"ripple"}
    total, lines = 0, []
    for coin, qty in portfolio.items():
        cid = coin_ids.get(coin.upper())
        price = prices.get(cid, {}).get("usd", 0) if prices and cid else 0
        value = price * qty
        total += value
        lines.append(f"• *{coin.upper()}* : {qty} × ${price:,.2f} = *${value:,.2f}*")

    text = f"⚖️ *Mon Portefeuille*\n\n" + "\n".join(lines) + f"\n\n💼 *Valeur totale : ${total:,.2f}*"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🤖 Analyser & Rééquilibrer", callback_data="portfolio_rebalance")],[InlineKeyboardButton("💰 Prix", callback_data="menu_prix")]])
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def cmd_ajout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid)
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("⚠️ Format : `/ajout BTC 0.5`", parse_mode="Markdown")
        return
    try:
        coin, qty = args[0].upper(), float(args[1])
        user["portfolio"][coin] = qty
        await update.message.reply_text(f"✅ *{qty} {coin}* ajouté !\n\nTape /portfolio pour voir ton bilan.", parse_mode="Markdown")
    except:
        await update.message.reply_text("❌ Format invalide. Ex : `/ajout BTC 0.5`", parse_mode="Markdown")

async def cmd_profil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid)
    level = xp_to_level(user["xp"])
    badges = "".join(b for b, t in [("🌱",20),("⚡",60),("🔥",150),("💎",300),("🏆",500)] if user["xp"] >= t) or "Aucun encore"
    text = (f"🏅 *Ton Profil BinanceQuest*\n\n*Niveau :* {level_label(level)}\n*XP :* {user['xp']} ⚡\n*Streak :* {user['streak']} jours 🔥\n*Badges :* {badges}\n\n_Continue à apprendre !_")
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(text, parse_mode="Markdown")

async def handle_free_question(update, context, question):
    uid = update.effective_user.id
    user = get_user(uid)
    history = user["chat_history"][-6:]
    messages = history + [{"role": "user", "content": question}]
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    reply = ask_claude(
        f"You are BinanceQuest AI, a crypto education assistant based on Binance Academy. " + ("Respond in English." if get_lang(uid)=="en" else "Réponds en français.") + " Be clear, educational and encouraging. Use emojis sparingly. Never give direct financial advice. Max 200 words.",
        messages
    )
    user["chat_history"] += [{"role":"user","content":question},{"role":"assistant","content":reply}]
    user["chat_history"] = user["chat_history"][-20:]
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🎯 Quiz", callback_data="menu_quiz"), InlineKeyboardButton("🏠 Menu", callback_data="menu_home")]])
    await update.message.reply_text(f"🤖 {reply}", reply_markup=keyboard)

async def handle_rebalance(update, context):
    uid = update.effective_user.id
    user = get_user(uid)
    portfolio = user.get("portfolio", {})
    if not portfolio:
        await update.callback_query.edit_message_text("⚠️ Portefeuille vide. Ajoute des cryptos avec `/ajout BTC 0.5`", parse_mode="Markdown")
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
        lines.append(f"{coin}: {qty} unités, ${value:.2f}, {change:+.1f}% 24h")
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    analysis = ask_claude(
        "Tu es BinanceQuest AI, expert en gestion de portefeuille crypto. Analyse le portefeuille et donne des suggestions éducatives de rééquilibrage : diversification, risques de concentration, principes DCA. Pas de conseils financiers directs. Pédagogique. Max 250 mots.",
        [{"role":"user","content":f"Portefeuille (total ${total:.2f}) :\n" + "\n".join(lines) + "\nDonne une analyse éducative et suggestions de rééquilibrage."}]
    )
    text = f"⚖️ *Analyse de ton Portefeuille*\n\n{analysis}\n\n_⚠️ Ceci est éducatif, pas un conseil financier._"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("💰 Prix", callback_data="menu_prix"), InlineKeyboardButton("🏠 Menu", callback_data="menu_home")]])
    await context.bot.send_message(update.effective_chat.id, text, parse_mode="Markdown", reply_markup=keyboard)

# ─── CALLBACKS ────────────────────────────────────────────────────────────────
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    data = update.callback_query.data
    uid = update.effective_user.id
    routes = {
        "menu_quiz": cmd_quiz, "menu_lesson": cmd_lecon,
        "menu_prix": cmd_prix, "menu_news": cmd_news,
        "menu_portfolio": cmd_portfolio, "menu_profil": cmd_profil,
    }
    if data == "lang_fr":
        set_lang(uid, 'fr')
        await update.callback_query.edit_message_text("🇫🇷 *Langue : Français activé !*\n\nTape /start pour le menu.", parse_mode="Markdown")
        return
    elif data == "lang_en":
        set_lang(uid, 'en')
        await update.callback_query.edit_message_text("🇬🇧 *Language: English activated!*\n\nType /start for the menu.", parse_mode="Markdown")
        return
    elif data in routes:
        await routes[data](update, context)
    elif data == "menu_home":
        lang = get_lang(uid)
        await update.callback_query.edit_message_text("🏠 " + ("Type /start for the main menu." if lang=="en" else "Tape /start pour revenir au menu."))
    elif data == "menu_ia":
        await update.callback_query.edit_message_text("🤖 *Assistant IA*\n\nPose ta question directement dans le chat !\n_Ex : C'est quoi le halving ?_", parse_mode="Markdown")
    elif data == "portfolio_rebalance":
        await handle_rebalance(update, context)
    elif data.startswith("quiz_"):
        q = context.user_data.get("current_quiz")
        if not q:
            await update.callback_query.edit_message_text("❌ Quiz expiré. Lance-en un nouveau avec /quiz")
            return
        chosen = int(data.split("_")[1])
        correct = chosen == q["answer"]
        user = get_user(update.effective_user.id)
        if correct:
            user["xp"] += 15
        if correct:
            result_line = "Bonne reponse !"
        else:
            result_line = "Mauvaise reponse. Bonne reponse : *" + q["options"][q["answer"]] + "*"
        text = (
            f"{result_line}\n\n"
            f"Explication : {q['explanation']}\n\n"
            f"XP : {user['xp']} | {level_label(xp_to_level(user['xp']))}"
        )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Autre question", callback_data="menu_quiz"), InlineKeyboardButton("📖 Leçon", callback_data="menu_lesson")],[InlineKeyboardButton("🏠 Menu", callback_data="menu_home")]])
        await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.startswith("/"):
        return
    text = update.message.text.strip()
    uid = update.effective_user.id
    # Auto-detect language
    detected = detect_lang(text)
    if detected == 'en':
        set_lang(uid, 'en')
    await handle_free_question(update, context, text)

# ─── QUIZ QUOTIDIEN ───────────────────────────────────────────────────────────
async def daily_quiz_job(context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(QUIZ_BANK)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(opt, callback_data=f"quiz_{i}")] for i, opt in enumerate(q["options"])])
    for uid in list(user_data.keys()):
        try:
            await context.bot.send_message(uid, f"☀️ *Quiz du jour BinanceQuest !*\n\n🎯 {q['q']}", parse_mode="Markdown", reply_markup=keyboard)
        except Exception as e:
            logger.warning(f"Impossible d'envoyer à {uid}: {e}")

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    for cmd, handler in [("start",cmd_start),("quiz",cmd_quiz),("lecon",cmd_lecon),("prix",cmd_prix),("news",cmd_news),("portfolio",cmd_portfolio),("ajout",cmd_ajout),("profil",cmd_profil)]:
        app.add_handler(CommandHandler(cmd, handler))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.job_queue.run_daily(daily_quiz_job, time=time(hour=DAILY_QUIZ_HOUR, minute=DAILY_QUIZ_MINUTE))
    print("🚀 BinanceQuest AI Bot démarré !")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
