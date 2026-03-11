# 🏆 BinanceQuest AI — OpenClaw Skill

> **Duolingo meets Binance Academy** — A gamified crypto education assistant powered by OpenClaw AI.

![BinanceQuest AI](https://img.shields.io/badge/OpenClaw-Skill-F0B90B?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge)
![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?style=for-the-badge)
![Binance](https://img.shields.io/badge/Binance-API-F0B90B?style=for-the-badge)

---

## 🎯 What is BinanceQuest AI?

BinanceQuest AI is an **OpenClaw-powered skill** that turns crypto education into a gamified experience — inspired by Duolingo, built on Binance Academy.

Available as:
- 🤖 **Telegram Bot** — `@BinanceQuestAI_bot`
- 🌐 **Web App** — [binancequest-web.vercel.app](https://binancequest-web.vercel.app)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎓 **Gamified Quizzes** | Interactive quizzes based on Binance Academy content |
| 💰 **Live Prices** | Real-time crypto prices via official Binance API |
| 🤖 **AI Assistant** | OpenClaw-powered assistant answers any crypto question |
| 📰 **Market Analysis** | Daily AI-generated market briefing |
| ⚖️ **Portfolio Tracker** | Track and rebalance your crypto portfolio with AI |
| ☀️ **Daily Quiz** | Automated quiz every morning at 9:00 AM |
| 🇫🇷🇬🇧 **Bilingual** | Full French & English support |

---

## 🚀 OpenClaw Skill Setup

### Prerequisites
- [OpenClaw](https://openclaw.ai) installed and running
- Telegram Bot token (from [@BotFather](https://t.me/BotFather))
- Anthropic API key (from [console.anthropic.com](https://console.anthropic.com))

### Install as OpenClaw Skill

1. Clone this repository into your OpenClaw skills folder:
```bash
cd ~/.openclaw/skills
git clone https://github.com/Loreano8/binancequest-bot binancequest
```

2. Add your API keys in OpenClaw dashboard → Settings → API Keys:
```
TELEGRAM_TOKEN=your_telegram_bot_token
ANTHROPIC_API_KEY=your_anthropic_api_key
```

3. Restart OpenClaw:
```bash
openclaw gateway restart
```

4. The skill is now active! Talk to your bot on Telegram.

---

## 🐍 Standalone Python Setup

If you prefer to run without OpenClaw:

### Installation
```bash
git clone https://github.com/Loreano8/binancequest-bot
cd binancequest-bot
pip install -r requirements.txt
```

### Configuration
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Run
```bash
python binancequest_bot_final.py
```

---

## 📁 Project Structure

```
binancequest-bot/
├── binancequest_bot_final.py  # Main bot logic
├── skill.md                   # OpenClaw skill definition
├── openclaw.skill.yaml        # OpenClaw skill configuration
├── requirements.txt           # Python dependencies
├── Procfile                   # Railway deployment
├── .env.example               # Environment variables template
└── README.md                  # This file
```

---

## 🔧 Environment Variables

| Variable | Description |
|----------|-------------|
| `TELEGRAM_TOKEN` | Your Telegram bot token from @BotFather |
| `ANTHROPIC_API_KEY` | Your Anthropic/OpenClaw API key |

---

## 🌐 Deployment

### Railway (Recommended)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

1. Fork this repository
2. Connect to Railway
3. Add environment variables
4. Deploy!

### OpenClaw (Self-hosted)
Follow the OpenClaw Skill Setup instructions above.

---

## 🏆 Hackathon

Built for the **OpenClaw × Binance Social Contest** — *Build the Future of Crypto AI*.

- **Category**: Crypto Education & Marketing
- **Tech Stack**: OpenClaw AI, Python, Telegram Bot API, Binance API
- **Live Demo**: [@BinanceQuestAI_bot](https://t.me/BinanceQuestAI_bot)

---

## 📄 License

MIT License — free to use and modify.

---

*Powered by OpenClaw AI × Binance Academy*
