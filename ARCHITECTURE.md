# Yeshua X Bot — Architecture & Interview Walkthrough

**Purpose:** Full professional reference so you can confidently explain every file and walk an interviewer through the architecture. What matters is that you understand what the code does; this document gives you that understanding in one place.

**Author:** Tremayne Timms · **Repository:** [github.com/omnipotence-eth/Yeshua-x-bot](https://github.com/omnipotence-eth/Yeshua-x-bot)

---

## 1. What This Project Is

- **Type:** A **scheduled social media automation bot** for X (Twitter).
- **Behavior:** One long-running Python process that uses a **job scheduler** to trigger posts at fixed times in two time zones. No manual trigger per post.
- **Content:** Three content types, each once per time zone per day:
  1. **Bible verse** (KJV) + AI-generated spiritual insight.
  2. **Markets** — US indices + crypto (Texas) or Chinese indices + crypto (Beijing), plus Fear & Greed and AI analysis.
  3. **AI news** — One AI-breakthrough headline (US/global for Texas, Chinese AI for Beijing) + AI-generated context.
- **Form:** Posts are **threads** (one root tweet + replies). Texas = 3-tweet threads (English). Beijing = 2-tweet threads (Chinese). Total 15 tweets/day (450/month), under X’s 500/month free tier.
- **Stack in one line:** Python runtime + APScheduler (cron-style jobs) + REST APIs (X, NewsAPI, Bible API, CoinGecko, Alternative.me, yfinance) + LLM (Groq) for thread replies + deep-translator for EN→ZH + optional file cache + Docker/PaaS deployment.

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│  main.py                                                                  │
│  Entry point. Parses CLI (--test, --dry-run). Validates config.          │
│  Either runs test_modules() or run_bot() → bot_scheduler.start().        │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  scheduler.py — BotScheduler                                             │
│  BlockingScheduler with 6 cron jobs:                                     │
│    • 3 jobs on Texas time (7:00, 8:00, 9:00) → English 3-tweet threads  │
│    • 3 jobs on Beijing time (7:00, 8:00, 9:00) → Chinese 2-tweet threads│
│  Each job: call content module → get main tweet (+ Chinese if Beijing)   │
│  → call AI thread generator → post thread via twitter_client.            │
└─────────────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────┐   ┌──────────────────┐   ┌──────────────────┐
│ modules/     │   │ modules/          │   │ modules/          │
│ bible_verse  │   │ combined_markets  │   │ world_news        │
│ (KJV verse)  │   │ (US or CN + crypto)│   │ (AI news only)   │
└──────────────┘   └──────────────────┘   └──────────────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  utils/                                                                   │
│  • ai_thread_generator — Groq LLM: verse/market/news follow-up tweets   │
│  • translator — EN → zh-CN (deep-translator Google)                       │
│  • twitter_client — Tweepy: post_tweet, post_thread, rate-limit aware   │
│  • logger — UTF-8-safe logging; log_tweet() for pre-post log             │
│  • cache — file-based cache (available; not yet used by modules)          │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  config.py                                                                │
│  Single source of config: os.getenv() for all secrets and flags;         │
│  pytz timezones (Texas, Beijing); schedule hours; API URLs; constants.   │
└─────────────────────────────────────────────────────────────────────────┘
```

**Data flow for one post (e.g. Texas Bible verse at 7:00):**  
Scheduler fires → `bible_module.get_verse()` → `bible_module.format_tweet()` → `ai_thread_generator.generate_bible_thread()` → list of 3 tweets → `twitter_client.post_thread()` (main tweet, then two replies with 2s delay). Same pattern for markets and news; for Beijing, content is either translated (verse) or generated in Chinese (markets/news) and thread length is 2.

---

## 3. File-by-File Reference

Use this section when an interviewer says “walk me through the repo” or “what does this file do?”

---

### Root / entry

| File | Purpose |
|------|--------|
| **main.py** | **Entry point.** Defines CLI (argparse): `--test` runs `test_modules()` (calls each content module, logs previews, no scheduler, no posts); `--dry-run` sets `config.DRY_RUN` so no tweets are posted. Otherwise runs `run_bot()`: validates required env vars via `validate_config()`, logs config, then calls `bot_scheduler.start()`. No business logic here—orchestration only. |
| **config.py** | **Single configuration module.** Loads env with `python-dotenv`. Reads X API credentials, optional NewsAPI/CoinGecko keys, flags (ENABLE_CHINESE_POSTS, DRY_RUN, LOG_LEVEL), pytz timezones (TEXAS_TZ, BEIJING_TZ), schedule map (hour/minute per content type), tweet limit (280), API base URLs, and top crypto ids. All secrets from `os.getenv()`; no defaults for credentials. |
| **scheduler.py** | **Job scheduler and post orchestration.** Defines `BotScheduler`: holds an APScheduler `BlockingScheduler` (default timezone Texas). `setup_schedules()` registers 6 cron jobs (CronTrigger, hour/minute, timezone): 3 for Texas (7/8/9 AM), 3 for Beijing (7/8/9 AM). Texas jobs call `post_*_texas()` methods; Beijing jobs call `post_*_beijing()`. Each method: (1) get content from the right module (English or Chinese), (2) get AI reply tweets from `ai_thread_generator`, (3) slice to 2 replies (Texas) or 1 reply (Beijing), (4) call `twitter_client.post_thread()`. `start()` logs the schedule and starts the scheduler (blocking). |

---

### modules/ — content generation

| File | Purpose |
|------|--------|
| **modules/bible_verse.py** | **Bible verse content.** `BibleVerseModule`: `get_random_reference()` picks random book/chapter/verse from `BIBLE_BOOKS`; `get_verse(reference)` calls bible-api.com (KJV), returns `(verse_text, reference)`. If API fails or verse too short/long, retries with `FALLBACK_VERSES` or returns John 3:16. `format_tweet(verse_text, reference)` produces one tweet string (quoted verse + reference, 280-cap). `generate_post()` returns (english_tweet, chinese_tweet) using translator. Exposes singleton `bible_module`. |
| **modules/combined_markets.py** | **Markets content (traditional + crypto).** `CombinedMarketsModule`: holds US tickers (S&P, Dow, Nasdaq), Chinese tickers (Shanghai, Hang Seng, Alibaba), and top cryptos. `get_fear_greed_index()` calls Alternative.me FNG API. `get_us_markets()` / `get_chinese_markets()` use yfinance for 2-day history and compute % change. `get_crypto_markets(limit)` uses CoinGecko markets API. `format_tweet(..., language)` builds one tweet (EN or ZH) with sentiment, traditional names, crypto lines, hashtags; truncates to 280. `generate_us_post()` / `generate_chinese_post()` compose data and call `format_tweet`. `generate_post()` returns (english, chinese). Exposes `combined_markets_module`. |
| **modules/world_news.py** | **AI-breakthrough news only.** `WorldNewsModule`: uses NewsAPI key from env; has `us_ai_terms` and `chinese_ai_terms` search lists. `fetch_us_ai_news()` / `fetch_chinese_ai_news()` call NewsAPI with each term until results exist; filter with `_is_ai_breakthrough()` (AI + positive keywords, no negative). On failure or no key, return mock dict (title, source). `generate_post()` fetches US and Chinese AI news, formats English and Chinese tweets (with translator for Chinese title/source), enforces 280. Exposes `news_module`. |
| **modules/__init__.py** | Package marker; no exports used elsewhere. |

---

### utils/ — shared services

| File | Purpose |
|------|--------|
| **utils/twitter_client.py** | **X (Twitter) API.** `TwitterClient`: in `_initialize_client()` builds Tweepy Client (v2) with bearer + OAuth credentials from config, and Tweepy API (v1.1) for media. `post_tweet(content, language, image_path)` truncates to 280, logs via `log_tweet`, and in non–dry-run calls `client.create_tweet` (optionally with media). `post_thread(tweets, language)` posts first tweet, then each reply with `in_reply_to_tweet_id` and 2s sleep. Handles TooManyRequests and Forbidden. Dry-run returns fake IDs and skips API. Exposes `twitter_client`. |
| **utils/ai_thread_generator.py** | **LLM-generated reply tweets.** `AIThreadGenerator`: reads `GROQ_API_KEY`; if present, initializes Groq client (Llama 3.3 70B). `generate_thread(main_tweet, data_context, max_tweets)` calls Groq with a prompt asking for numbered follow-up tweets; parses lines, strips numbering, enforces 280. `generate_bible_thread(verse_text, reference, language)` uses a Bible-specific prompt; for `zh`, generates in English then translates with `translator`. `generate_financial_thread`, `generate_news_thread` wrap `generate_thread` with context; for `zh` translate replies. All return list of reply strings (no main tweet). Exposes `ai_thread_generator`. |
| **utils/translator.py** | **EN → Simplified Chinese.** `ChineseTranslator` uses `deep_translator.GoogleTranslator(source='en', target='zh-CN')`. `translate(text)` returns translated string or original on error. `translate_with_limit(text, char_limit)` truncates to 280 after translate. Exposes `translator`. |
| **utils/logger.py** | **Logging.** `setup_logger(name)` creates a logger with level from config, adds a StreamHandler to stdout, optional UTF-8 reconfigure for stdout (wrapped in try/except). Formatter: timestamp, name, level, message. `log_tweet(content, language, dry_run)` logs a short pre-post line. No file logging; console only. |
| **utils/cache.py** | **File-based cache.** `SimpleCache(cache_dir=".cache")`: `get(key, max_age_minutes)` returns value if file exists and not expired; `set(key, value)` writes JSON with timestamp; `clear()` / `clear_old(max_age_hours)` for maintenance. Key is sanitized to filename. **Not currently used by any module**; available to reduce API calls (e.g. verse or market data per day). Exposes `cache`. |
| **utils/__init__.py** | Package marker. |

---

### Supporting / scripts

| File | Purpose |
|------|--------|
| **preview_new_config.py** | **Offline preview.** No scheduler, no posting. Calls the three modules to generate content, prints English and Chinese tweets and schedule info to stdout. Uses `print()` for user-facing output. Safe to run without posting. |
| **test_all_posts.py** | **Live test.** Imports scheduler and runs the same six post paths (Texas Bible, Texas markets, Texas news, Beijing Bible, Beijing markets, Beijing news) once, with optional confirmation. Respects DRY_RUN. Use to verify full pipeline against real X API. |

---

### Deployment and environment

| File | Purpose |
|------|--------|
| **.env.example** | Template for environment variables: X API keys, NewsAPI, Groq, optional CoinGecko, DRY_RUN, ENABLE_CHINESE_POSTS, LOG_LEVEL. User copies to `.env` and fills values; `.env` is gitignored. |
| **requirements.txt** | Python dependencies: tweepy, requests, python-dotenv, schedule, pytz, deep-translator, APScheduler, beautifulsoup4, yfinance, matplotlib, pillow, groq. |
| **runtime.txt** | Optional; used by some PaaS to select Python version. |
| **Dockerfile** | Multi-stage not used. Base `python:3.11-slim`, install deps from requirements.txt, copy app, create non-root user `botuser`, CMD `python main.py`. |
| **.dockerignore** | Excludes `.env`, `.git`, `__pycache__`, `.cache`, most `.md` (except README), preview/test scripts, deploy configs so the image stays small and secret-free. |
| **docker-compose.yml** | Single service running the image with `env_file: .env`. |
| **fly.toml** | Fly.io app config (app name, build, env). |
| **Procfile** | `web: python main.py` for Heroku-style platforms. |
| **railway.json** | Railway deployment config. |
| **render.yaml** | Render service definition. |
| **deploy.sh** / **deploy.ps1** | Shell scripts for deploy (e.g. build and push); not required for the app to run. |

---

### Documentation (no code behavior)

| File | Purpose |
|------|--------|
| **README.md** | User-facing: what the bot does, schedule, tech stack, project structure, quick start, env setup, API keys, deployment links. |
| **INTERVIEW_OVERVIEW.md** | One-page technical summary: project type, what it does, technologies, APIs, architecture bullets, talking points. |
| **ARCHITECTURE.md** | This file: full architecture and file-by-file reference for interviews. |
| **AUDIT_REPORT.md** | Safety and code-quality audit summary. |
| **AUDIT_SUMMARY.md** | Historical audit of fixes (verse consistency, encoding, markets, news, AI translation). |
| **DEPLOYMENT.md** | Short index of deployment guides and options. |
| **DEPLOY_NOW.md**, **FLY_DEPLOYMENT.md**, **DEPLOYMENT_SUMMARY.md** | Fly.io and deployment step-by-step. |
| **X_BIO.md** | Suggested X profile bio and variants. |
| **LICENSE** | MIT. |

---

## 4. Design Decisions You Can Explain

- **Why one process and a blocking scheduler?** Simple operational model: one container or process, no queue or worker pool. APScheduler cron jobs are sufficient for fixed daily times; no need for a message queue.
- **Why two time zones in one process?** Both Texas and Beijing run in the same process via different CronTriggers and timezones (pytz). Single deployment, single set of env vars.
- **Why Texas = 3 tweets, Beijing = 2?** To keep daily total (15) under 500/month and to slightly shorten Chinese threads for readability; the scheduler slices AI reply lists to 2 (Texas) or 1 (Beijing).
- **Why same content types but different data for Texas vs Beijing?** Markets and news are region-specific (US vs Chinese indices; US/global AI vs Chinese AI). Bible is the same content idea; verse is chosen independently per job (no shared “today’s verse” cache in current code).
- **Why Groq for replies?** Fast, free-tier friendly LLM for generating short, on-topic follow-up tweets; prompts are tailored per content type (verse, financial, news).
- **Why translate to Chinese instead of generating in Chinese?** AI quality and consistency are better in English; translation is a single, predictable step and keeps prompts simpler.
- **Why config in one file?** Single place to look for env vars and constants; no secrets in code; easy to override via environment in Docker/PaaS.
- **Why optional cache in utils but not used?** Available for future use (e.g. one verse or one market snapshot per day to align Texas and Beijing or to reduce API calls); current design does not depend on it.

---

## 5. How to Answer “Walk Me Through Your Architecture”

**Short version (1–2 minutes):**  
“It’s a scheduled Twitter bot: one Python process, one scheduler with six cron jobs—three for US time (English, 3-tweet threads) and three for Beijing time (Chinese, 2-tweet threads). Each job pulls content from one of three modules—Bible verse, combined markets, or AI news—then uses Groq to generate reply tweets and the Twitter client to post the thread. Config and secrets come from the environment; there’s no database. I can walk through any file you’re interested in.”

**Then, if they point to a file:**  
Use **Section 3** of this document to say what that file is responsible for, what it imports, and how it fits in (e.g. “scheduler.py is where the six jobs are registered and where we call the content modules and the AI generator, then post the thread”).

**If they ask “how does a tweet get posted?”:**  
“The scheduler fires at the scheduled time, calls the right module to get the main tweet—and for Beijing, the Chinese version. Then it calls the AI thread generator to get one or two follow-up tweets, optionally translated. That list goes to the Twitter client, which posts the first tweet, then posts each reply with the previous tweet’s ID and a short delay to avoid rate limits.”

**If they ask “where are secrets?”:**  
“Only in the environment. config.py reads everything with os.getenv(); we have .env.example in the repo and .env in .gitignore. The Dockerfile doesn’t copy .env; we pass env at runtime.”

---

## 6. Summary

- **main.py** — Entry and CLI; validates config and starts the scheduler.
- **config.py** — Single source of configuration from environment.
- **scheduler.py** — Six cron jobs; each builds content (modules), AI replies (utils), and posts a thread (twitter_client).
- **modules/** — bible_verse (KJV + format), combined_markets (US/CN + crypto + format), world_news (AI news + format).
- **utils/** — twitter_client (Tweepy, post thread), ai_thread_generator (Groq, reply tweets), translator (EN→ZH), logger (stdout, UTF-8-safe), cache (file cache, unused).
- **Deployment** — Dockerfile + .dockerignore; Fly/Railway/Render configs; env from host or platform.

Using this document, you can confidently explain every file and the end-to-end flow from “scheduler fires” to “thread posted on X.”
