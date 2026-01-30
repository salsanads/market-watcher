# 📊 Market Watcher Discord Bot

[![GitHub Workflow Status](https://github.com/salsanads/market-watcher/actions/workflows/watcher.yml/badge.svg?branch=main)](https://github.com/salsanads/market-watcher/actions/workflows/watcher.yml)
![Python Version](https://img.shields.io/badge/python-3.13-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![Scheduled: Daily](https://img.shields.io/badge/schedule-daily-orange)

A configurable Python Discord bot that posts **daily foreign exchange rates** and **stock prices** to a **Discord** channel.

Built to run as a one-shot scheduled job using GitHub Actions — no servers, no background workers, no idle costs.

## ✨ Features
- Configurable base currency (default: `IDR`)
- Multiple currency pairs via a single config
- Configurable market symbols using Yahoo Finance (`yfinance`)
- Scheduled execution via GitHub Actions (cron)
- Sends one Discord message and exits cleanly
- Can be run locally with a `.env` file
- Free, serverless, and easy to maintain

## 📬 Message Format
```
📊 Daily Market Update
Friday, 30 January 2026

💱 FX Rates
1 USD = 16,756 IDR
1 SGD = 13,238 IDR
1 MYR = 4,270 IDR
1 AUD = 11,814 IDR
1 EUR = 20,021 IDR
1 GBP = 23,108 IDR

📈 Stocks
^JKSE: 8,329.15
TLKM.JK: 3,680.00
META: 738.31
```

## 🌍 Environments
The workflow uses GitHub Actions Environments.

Defined environments:
- `staging` (for testing, manual runs supported via `workflow_dispatch`)
- `production` (default, for cron job)

## ⚙️ Configuration
All configuration is provided via **GitHub Actions Environments** (and via `.env` for local development).

### 🔐 Secrets
(GitHub → Settings → Secrets and variables → Actions → Secrets)

or

(GitHub → Settings → Environments → `{environment}` → Secrets)

| Variable | Required	| Description |
|---|:---:|---|
| `DISCORD_TOKEN`	| ✅ | Discord bot token |
| `DISCORD_CHANNEL_ID` | ✅ | Target Discord channel ID |

### 🔐 Secrets
(GitHub → Settings → Secrets and variables → Actions → Variables)

or

(GitHub → Settings → Environments → `{environment}` → Variables)

| Variable | Required | Description | Example |
|---|:---:|---|---|
| `BASE_CURRENCY` |	❌ | Base currency for FX rates (default: `IDR`) | `IDR`
| `CURRENCIES` | ✅ | Comma-separated currency list without spaces | `USD,SGD,EUR`
| `SYMBOLS` | ✅ | Comma-separated market symbol list without spaces (see the symbol format below) | `^JKSE,TLKM.JK,META`
| `TIMEZONE` |	❌ | Timezone for the date in Discord message (default: `Asia/Singapore`) | `Asia/Singapore`

## 📈 Market Symbols (`SYMBOLS` variable)
Symbols must follow `yfinance` or Yahoo Finance conventions.

Example:
```bash
SYMBOLS=^JKSE,TLKM.JK,META,AAPL,TSLA
```

### Common formats
| Market | Example |
|---|---|
| Indexes | `^GSPC`, `^JKSE` |
| US stocks | `AAPL`, `META`, `TSLA` |
| Indonesia stocks | `BBCA.JK`, `TLKM.JK` |
| Other exchanges | Use exchange suffix (e.g. `.L`, `.HK`) |

### 🔎 How to find symbols
Most symbols available on Yahoo Finance will work. Search on Yahoo Finance and use the ticker shown: https://finance.yahoo.com.

## 🕒 Scheduling
The bot runs via GitHub Actions on a cron schedule.

Default schedule:
```yml
schedule:
  - cron: '30 2 * * *'
```
- Runs daily at **10:30 UTC+8**
- The schedule can be adjusted directly in the workflow file
- Manual runs supported via `workflow_dispatch`

## 🧪 Local Development
Local development uses a `.env` file.

1. Copy the example file:
```bash
cp env.example .env
```

2. Fill in required values:
```bash
DISCORD_TOKEN=your_bot_token
DISCORD_CHANNEL_ID=your_channel_id
```

3. Customize configuration:
```bash
BASE_CURRENCY=IDR
CURRENCIES=USD,SGD,MYR,AUD,EUR,GBP
SYMBOLS=^JKSE,TLKM.JK,META
TIMEZONE=Asia/Singapore
```

4. Install dependencies and run:
```bash
pip install -r requirements.txt
python bot_action.py
```

## 🚀 How It Works
1. GitHub Actions starts the workflow
2. Python script fetches:
    - Exchange rates from `open.er-api.com`
    - Market prices using `yfinance`
3. Bot logs into Discord
4. Sends one message
5. Bot shuts down gracefully

No persistent service, no open ports, no background workers.

## 📜 License
MIT License
