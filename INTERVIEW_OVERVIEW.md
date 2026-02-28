# Yeshua X Bot — Project Overview for Interviews

**Author:** [Tremayne Timms](https://github.com/omnipotence-eth)  
**License:** MIT  
**Repository:** [github.com/omnipotence-eth/Yeshua-x-bot](https://github.com/omnipotence-eth/Yeshua-x-bot)  
**Purpose:** One-page technical overview for portfolio discussions and technical interviews.

---

## What It Does

**Yeshua X Bot** is an automated X (Twitter) bot that posts daily content in two languages and two time zones:

1. **Bible verse** — KJV verse + AI-generated spiritual insight (same verse in English and Chinese).
2. **Markets** — US indices + crypto (Texas) and Chinese indices + crypto (Beijing), with sentiment and AI analysis.
3. **AI news** — AI-breakthrough headlines only: US/global for Texas, Chinese AI for Beijing, with AI-generated context.

Posts are **threads**: 3-tweet threads in English (Texas time), 2-tweet threads in Chinese (Beijing time). Total: 15 tweets/day (450/month), under X’s 500/month free tier.

---

## Technologies Used

| Layer | Technology | Role |
|-------|------------|------|
| **Language** | Python 3.11+ | Runtime and application logic |
| **Scheduling** | APScheduler | Cron-style jobs for Texas and Beijing time zones |
| **Social API** | Tweepy | X (Twitter) API: post threads, rate-limit awareness |
| **AI** | Groq (Llama 3.3) | Thread replies and analysis for verse, markets, and news |
| **Translation** | deep-translator | English → Chinese for verses and AI replies |
| **Data** | requests, yfinance | HTTP calls; Yahoo Finance for indices |
| **Config** | python-dotenv, pytz | Env vars; Texas (America/Chicago) and Beijing (Asia/Shanghai) |
| **Deployment** | Docker, Fly.io, Railway, Render | Container and PaaS options |

---

## External APIs & Services

- **bible-api.com** — KJV verse of the day (free).
- **NewsAPI** — AI-related news (US/global and Chinese sources).
- **CoinGecko** — Crypto prices (free tier).
- **Alternative.me** — Fear & Greed Index.
- **yfinance** — US and Chinese equity indices.
- **Groq** — LLM for thread generation (free-tier credits).
- **X (Twitter) API** — Posting and account (free tier: 500 tweets/month).

---

## Architecture (High Level)

```
main.py          → CLI, --test, config validation, starts scheduler
scheduler.py     → APScheduler: 6 cron jobs (3 Texas, 3 Beijing)
config.py        → Env-based config (keys, timezones, schedule, limits)

modules/
  bible_verse.py      → Random KJV verse + formatted tweet
  combined_markets.py → US vs Chinese market data + formatted threads
  world_news.py       → AI-only news (US/global vs Chinese), one article per post

utils/
  twitter_client.py       → Tweepy client, post_thread(), rate limits
  ai_thread_generator.py   → Groq: verse/market/news threads (EN + ZH via translator)
  translator.py            → deep-translator (Google backend)
  logger.py                → UTF-8-safe logging (Windows-friendly)
  cache.py                 → Optional response caching for APIs
```

Data flow per post type: **fetch data (or use cache) → format main tweet → generate AI replies (Groq) → translate if Chinese → post thread via Tweepy.**

---

## Design Decisions

- **Same verse for EN and ZH** — One verse per day; Chinese is translated from that verse (and AI reply translated) so both audiences see the same content.
- **Timezone-specific content** — Texas: US indices + US/global AI news; Beijing: Chinese indices + Chinese AI news.
- **AI-only news** — NewsAPI filtered to AI breakthroughs only; different query sets for US vs Chinese markets.
- **Free-tier first** — X 500/month, NewsAPI free tier, Groq free credits; no paid keys required for core flow.
- **Secrets** — All keys from environment (e.g. `.env`); no credentials in repo; `.env` in `.gitignore`.

---

## Talking Points for Interviews

1. **Scheduling** — Single process, two time zones (pytz), 6 cron jobs; clear separation of “what to post” (modules) vs “when” (scheduler).
2. **APIs** — Multiple third-party APIs; error handling and fallbacks (e.g. mock data when keys missing); optional caching.
3. **AI integration** — Groq for thread generation; prompts tailored per content type; Chinese output via translation pipeline.
4. **i18n** — Bilingual (EN/ZH), same logical content; translation applied to verse and AI replies; character limits (280) enforced.
5. **Deployment** — Dockerfile and PaaS configs (Fly, Railway, Render); env-based config; suitable for one-command deploy.
6. **Open source** — MIT license; README, `.env.example`, no committed secrets; ready for public GitHub.

---

## Repo Layout (Relevant to This Overview)

- **Entry:** `main.py` (run bot or `python main.py --test`).
- **Preview (no post):** `preview_new_config.py`.
- **Config:** `config.py` + `.env` (use `.env.example` as template).
- **Docs:** `README.md`, `DEPLOYMENT.md`, this file.

---

*Yeshua X Bot — [Tremayne Timms](https://github.com/omnipotence-eth). Built for daily inspiration and market/AI news, optimized for free tiers and clear structure for portfolio and interviews.*
