# 🙏 Yeshua X Bot

An automated X (Twitter) bot that posts daily spiritual content and market updates in English and Chinese, powered by AI insights.

**Repository:** [github.com/omnipotence-eth/Yeshua-x-bot](https://github.com/omnipotence-eth/Yeshua-x-bot) · **Author:** [Tremayne Timms](https://github.com/omnipotence-eth) · MIT License

---

### 1. **Bible Verse** 📖
- Daily inspiration from the King James Version (KJV)
- Covers all 66 books of the Bible
- AI-generated spiritual insights and practical applications

### 2. **Combined Markets** 💹
**Texas (US Markets):**
- **US Markets**: S&P 500, Dow Jones, Nasdaq
- **Top Crypto**: Bitcoin, Ethereum, BNB, Solana
- Fear & Greed Index for market sentiment
- AI-powered market analysis

**Beijing (Chinese Markets):**
- **Chinese Markets**: Shanghai Composite, Hang Seng, Alibaba
- **Top Crypto**: Bitcoin, Ethereum, BNB
- Fear & Greed Index for market sentiment
- AI-powered market insights

### 3. **AI Breakthroughs** 🚀
- **ONLY AI breakthroughs and innovations**
- **Texas (English)**: US/Global AI news (OpenAI, Google, Microsoft)
- **Beijing (Chinese)**: Chinese AI news (Baidu, ByteDance, Alibaba)
- AI-generated context and deeper analysis

---

## ⏰ Posting Schedule

### **Texas Time (English 3-tweet threads)**
- **7:00 AM** - Bible Verse (KJV)
- **8:00 AM** - US Markets (S&P, Dow, Nasdaq + Crypto)
- **9:00 AM** - AI Breakthroughs (US/Global AI News)

### **Beijing Time (Chinese 2-tweet threads)**
- **7:00 AM** - 圣经经文 (Same verse, translated)
- **8:00 AM** - 中国市场 (Shanghai, Hang Seng, Alibaba + Crypto)
- **9:00 AM** - AI突破 (Chinese AI News)

---

## 📈 Tweet Count & API Limits

| Metric | Count |
|--------|-------|
| **Daily English tweets** | 9 (3 content × 3 tweets) |
| **Daily Chinese tweets** | 6 (3 content × 2 tweets) |
| **Total per day** | **15 tweets** |
| **Monthly total** | **450 tweets** |
| **X API Free Tier** | 500 tweets/month |
| **Buffer** | 50 tweets ✅ |

**Status**: Well within free tier limits!

---

## 🔧 Technology Stack

### **Core**
- Python 3.11+
- APScheduler (job scheduling)
- Tweepy (X API integration)

### **APIs Used**
- **bible-api.com** - KJV Bible verses (Free)
- **NewsAPI** - World news (100 requests/day free)
- **yfinance** - Traditional market data (Unlimited)
- **CoinGecko** - Cryptocurrency prices (Free tier)
- **Alternative.me** - Fear & Greed Index (Free)
- **Groq AI** - AI insights with Llama 3.3 ($5/month free credits)
- **Google Translator** - Chinese translation (Free)

---

## 📁 Project Structure

```
Yeshua X Bot/
├── modules/
│   ├── bible_verse.py          # Daily Bible verses (KJV)
│   ├── combined_markets.py     # US & Chinese finance + crypto
│   └── world_news.py           # AI breakthrough news (NewsAPI)
├── utils/
│   ├── ai_thread_generator.py  # Groq AI thread generation
│   ├── cache.py                # API response caching
│   ├── logger.py               # Logging (UTF-8 safe)
│   ├── translator.py           # Chinese translation (deep-translator)
│   └── twitter_client.py       # X (Twitter) API client
├── config.py                   # Configuration and env
├── main.py                     # Entry point and CLI
├── scheduler.py                # APScheduler jobs (Texas + Beijing)
├── requirements.txt            # Dependencies
├── .env.example                # Example env (copy to .env)
└── [deployment]                # Dockerfile, fly.toml, railway.json, render.yaml
```

---

## 🚀 Quick Start

### **1. Clone the Repository**
```bash
git clone https://github.com/omnipotence-eth/Yeshua-x-bot.git
cd Yeshua-x-bot
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Set Up Environment Variables**

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your values (never commit `.env` to version control; it is in `.gitignore`):

```env
# X (Twitter) API Credentials
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token

# News API
NEWS_API_KEY=your_newsapi_key

# AI API (Groq)
GROQ_API_KEY=your_groq_api_key

# Bot Settings
DRY_RUN=false
ENABLE_CHINESE_POSTS=true
```

### **4. Get API Keys**

#### **X API (Free Tier)**
1. Go to [developer.twitter.com](https://developer.twitter.com)
2. Create a new app
3. Enable "Read and Write" permissions
4. Copy all 5 credentials to `.env`

#### **NewsAPI**
1. Go to [newsapi.org](https://newsapi.org)
2. Sign up for free (100 requests/day)
3. Copy API key to `.env`

#### **Groq AI**
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for free ($5/month credits)
3. Create API key and copy to `.env`

### **5. Preview (Without Posting)**
```bash
python preview_new_config.py
```

### **6. Test Run (Posts to X)**
```bash
# Make sure DRY_RUN=false in .env
python main.py --test
```

### **7. Deploy**

See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment options and guides (Fly.io, Railway, Render, Docker).

**Quick deploy to Railway:**
```bash
railway up
```

---

## 🎯 Features

### ✅ **Smart Scheduling**
- Posts at optimal times in two timezones
- Texas time for US/Global audience
- Beijing time for Asian audience

### ✅ **AI-Powered Insights**
- Uses Groq's Llama 3.3 model
- Generates contextual analysis for every post
- Adapts tone for spiritual, financial, and news content

### ✅ **Bilingual Support**
- English posts with 3-tweet threads
- Chinese posts with 2-tweet threads
- Automatic translation using Google Translator

### ✅ **API Caching**
- Reduces redundant API calls
- Saves costs and improves speed
- Respects rate limits

### ✅ **Error Handling**
- Fallback data when APIs fail
- Automatic retries with exponential backoff
- Comprehensive logging for debugging

### ✅ **Free Tier Optimized**
- Uses only free or low-cost APIs
- Stays within X's 500 tweets/month limit
- Minimal monthly cost (~$0 with free credits)

---

## 📝 Configuration

Edit `config.py` to customize:

```python
# Posting Schedule
SCHEDULE_CONFIG = {
    'bible_verse': {'hour': 7, 'minute': 0},
    'combined_markets': {'hour': 8, 'minute': 0},
    'world_news': {'hour': 9, 'minute': 0}
}

# Top Crypto Assets (for combined markets post)
TOP_CRYPTO_ASSETS = ['bitcoin', 'ethereum', 'binancecoin', 'solana']

# Tweet Character Limit
TWEET_CHAR_LIMIT = 280
```

---

## 🐳 Docker Deployment

```bash
# Build
docker build -t yeshua-x-bot .

# Run
docker run -d --env-file .env yeshua-x-bot
```

Or use Docker Compose:

```bash
docker-compose up -d
```

---

## 🌐 Cloud Deployment

### **Railway (Recommended)**
```bash
railway up
```

### **Render**
1. Connect GitHub repo
2. Add environment variables
3. Deploy

### **Other Platforms**
- Fly.io (`fly.toml` included)
- Heroku (`Procfile` included)
- Any VPS with Docker support

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides.

---

## 📊 Monitoring

Logs are stored in the console output. Key events logged:

- ✅ Successful posts
- ⚠️ API errors
- 🔄 Retry attempts
- 📊 Rate limit status
- 🔧 Configuration changes

---

## 🛡️ Rate Limiting & Best Practices

### **X API Free Tier**
- **Limit**: 500 tweets/month
- **Bot usage**: 450 tweets/month (90%)
- **Buffer**: 50 tweets for testing/extras

### **NewsAPI**
- **Limit**: 100 requests/day
- **Bot usage**: 6 requests/day (6%)

### **Groq AI**
- **Limit**: $5/month free credits
- **Bot usage**: ~$0.15/month (<3%)

---

## 🤝 Contributing

Suggestions and improvements are welcome. Please open an issue or submit a pull request.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

**Interview / portfolio:** See [INTERVIEW_OVERVIEW.md](INTERVIEW_OVERVIEW.md) for a concise technical overview (technologies, architecture, talking points).

---

## 🙏 Credits

**Author & maintainer:** [Tremayne Timms](https://github.com/omnipotence-eth)

**APIs & services:**
- **Bible API**: [bible-api.com](https://bible-api.com)
- **News API**: [newsapi.org](https://newsapi.org)
- **CoinGecko API**: [coingecko.com](https://www.coingecko.com)
- **Groq AI**: [groq.com](https://groq.com)
- **X (Twitter) API**: [developer.twitter.com](https://developer.twitter.com)

---

## 📞 Contact

For questions or feedback, open an issue on GitHub. Deployment help: [DEPLOYMENT.md](DEPLOYMENT.md).
