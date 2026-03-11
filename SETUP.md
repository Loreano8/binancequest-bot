# BinanceQuest AI — Setup Guide

## Prerequisites
- Python 3.11+
- OpenClaw installed ([openclaw.ai](https://openclaw.ai))
- Telegram account
- Anthropic API key

---

## Option 1 — OpenClaw Setup (Recommended)

### Step 1: Clone the repository
```bash
cd ~/.openclaw/skills
git clone https://github.com/Loreano8/binancequest-bot binancequest
```

### Step 2: Configure API keys
Open OpenClaw Dashboard → Settings → API Keys and add:
```
TELEGRAM_TOKEN=your_telegram_bot_token
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### Step 3: Create your Telegram bot
1. Open Telegram → search `@BotFather`
2. Send `/newbot`
3. Follow instructions to get your token

### Step 4: Restart OpenClaw
```bash
openclaw gateway restart
```

### Step 5: Test your bot
Open Telegram → find your bot → send `/start`

---

## Option 2 — Standalone Python Setup

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure environment
```bash
cp .env.example .env
```
Edit `.env` and add your keys:
```
TELEGRAM_TOKEN=your_token_here
ANTHROPIC_API_KEY=your_key_here
```

### Step 3: Run the bot
```bash
python main.py
```

---

## Option 3 — Deploy on Railway (24/7 hosting)

1. Fork this repository on GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select your forked repo
4. Add environment variables:
   - `TELEGRAM_TOKEN`
   - `ANTHROPIC_API_KEY`
5. Deploy — your bot runs 24/7!

---

## Skills Available

| Skill | File | Description |
|-------|------|-------------|
| Quiz | `skills/quiz.py` | Gamified crypto quizzes |
| Prices | `skills/prices.py` | Live Binance API prices |
| News | `skills/news.py` | AI market analysis |
| Lessons | `skills/lessons.py` | Crypto education lessons |
| Portfolio | `skills/portfolio.py` | Portfolio tracker & rebalancing |
| Daily Quiz | `skills/daily_quiz.py` | Automated morning quiz |

---

## Troubleshooting

**Bot not responding?**
- Check your `TELEGRAM_TOKEN` is correct
- Verify OpenClaw gateway is running: `openclaw gateway status`

**AI not working?**
- Check your `ANTHROPIC_API_KEY` has credits
- Visit [console.anthropic.com](https://console.anthropic.com) to top up

**Language issues?**
- Use 🇫🇷 Français or 🇬🇧 English buttons in the menu
- The bot auto-detects your Telegram language
