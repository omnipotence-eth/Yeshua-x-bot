# 🙏 Yeshua X Bot

An automated X (Twitter) bot that posts daily spiritual content and market updates in English and Chinese, powered by AI insights.

## 📊 What It Posts

### 1. **Bible Verse** 📖
- Daily inspiration from the King James Version (KJV)
- Covers all 66 books of the Bible
- AI-generated spiritual insights and practical applications

### 2. **Combined Markets** 💹
- **Traditional Markets**: S&P 500, Nasdaq, Gold
- **Crypto Markets**: Bitcoin, Ethereum, BNB
- Fear & Greed Index for market sentiment
- AI-powered market analysis and investor insights

### 3. **World News** 📰
- Single top article from Finance, AI, or Robotics
- Global news for English audience
- China-focused news for Chinese audience
- AI-generated context and deeper analysis

---

## ⏰ Posting Schedule

### **Texas Time (English 3-tweet threads)**
- **7:00 AM** - Bible Verse
- **8:00 AM** - Combined Markets
- **9:00 AM** - World News

### **Beijing Time (Chinese 2-tweet threads)**
- **7:00 AM** - Bible Verse
- **8:00 AM** - Combined Markets
- **9:00 AM** - World News

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
│   ├── combined_markets.py     # Finance + Crypto markets
│   └── world_news.py           # Single top news article
├── utils/
│   ├── ai_thread_generator.py  # Groq AI thread generation
│   ├── cache.py                # API response caching
│   ├── logger.py               # Logging system
│   ├── translator.py           # Chinese translation
│   └── twitter_client.py       # X API integration
├── config.py                   # Configuration settings
├── main.py                     # Entry point
├── scheduler.py                # Job scheduling
├── requirements.txt            # Dependencies
├── .env                        # Environment variables (not tracked)
└── [deployment files]          # Docker, Railway, Render configs
```

---

## 🚀 Quick Start

### **1. Clone the Repository**
```bash
git clone <your-repo-url>
cd "Yeshua X Bot"
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Set Up Environment Variables**

Create a `.env` file in the project root:

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

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

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
TOP_CRYPTO_ASSETS = ['bitcoin', 'ethereum', 'binancecoin']

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

This is a personal project, but suggestions are welcome! Open an issue or submit a pull request.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Credits

- **Bible API**: [bible-api.com](https://bible-api.com)
- **News API**: [newsapi.org](https://newsapi.org)
- **CoinGecko API**: [coingecko.com](https://www.coingecko.com)
- **Groq AI**: [groq.com](https://groq.com)
- **X (Twitter) API**: [developer.twitter.com](https://developer.twitter.com)

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help

---

**Built with ❤️ for spreading inspiration and knowledge**
