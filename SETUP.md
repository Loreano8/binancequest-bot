# BinanceQuest AI — Setup Guide

> Gamified crypto education assistant powered by OpenClaw and Binance Academy

---

## What You Need

- Windows, macOS or Linux
- Node.js v22+ → [nodejs.org](https://nodejs.org)
- A Telegram account + bot token from [@BotFather](https://t.me/BotFather)
- An Anthropic API key → [console.anthropic.com](https://console.anthropic.com)

> Binance Public API requires no key ✅

---

## Step 1 — Install OpenClaw

**Windows (PowerShell as Administrator):**
```powershell
iwr -useb https://openclaw.ai/install.ps1 -OutFile install.ps1
powershell -ExecutionPolicy Bypass -File install.ps1
```

**macOS / Linux:**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

---

## Step 2 — Run Onboarding

```bash
openclaw onboard
```

When prompted:
- Choose **QuickStart** mode
- Select **Anthropic** as your AI provider
- Paste your **Anthropic API key**
- Select **claude-sonnet-4-6** as the model
- Select **Telegram** as your channel
- Paste your **Telegram Bot Token**
- Enable **session-memory**
- Open the dashboard when asked

---

## Step 3 — Load BinanceQuest Agent

Copy the agent files to your OpenClaw workspace:

```bash
# macOS / Linux
cp AGENTS.md ~/.openclaw/workspace/AGENTS.md
cp IDENTITY.md ~/.openclaw/workspace/IDENTITY.md

# Windows (PowerShell)
Copy-Item AGENTS.md "$env:USERPROFILE\.openclaw\workspace\AGENTS.md"
Copy-Item IDENTITY.md "$env:USERPROFILE\.openclaw\workspace\IDENTITY.md"
```

---

## Step 4 — Start the Gateway

```bash
openclaw gateway start
```

**Windows alternative:**
```powershell
node "$env:APPDATA\npm\node_modules\openclaw\dist\index.js" gateway --port 18789
```

---

## Step 5 — Pair with Telegram

Send `/start` to your bot on Telegram — it will give you a pairing code.

Then approve it:
```bash
openclaw pairing approve telegram YOUR_PAIRING_CODE
```

---

## You're Live! 🎉

Open Telegram, send `/start` to your bot and start your first crypto quest!

```
🏆 BinanceQuest AI
Learn crypto. Level up. Quest on.

🎯 /quiz     — Start a quiz
📚 /lecon    — Lesson of the day
💰 /prix     — Live crypto prices
📰 /news     — AI market analysis
💼 /portfolio — My portfolio
👤 /profil   — My XP & badges
```

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Main menu |
| `/quiz` | Random crypto quiz (+15 XP) |
| `/lecon` | Lesson from Binance Academy |
| `/prix` | Live prices from Binance API |
| `/news` | AI-powered market briefing |
| `/portfolio` | Portfolio tracker |
| `/ajout BTC 0.5` | Add crypto to portfolio |
| `/retirer BTC` | Remove crypto from portfolio |
| `/reset_portfolio` | Clear entire portfolio |
| `/profil` | View XP, level and badges |

---

## Deploy 24/7 on Railway

For continuous availability without keeping your PC on:

1. Fork this repository
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add environment variables:
   - `TELEGRAM_TOKEN` → your bot token
   - `ANTHROPIC_API_KEY` → your API key
4. Deploy — your bot runs 24/7! 🚀

---

## Security

- Keep your `.env` file private — never commit it to GitHub
- Use read-only API keys where possible
- The `.env.example` file in this repo shows required variables without real values
