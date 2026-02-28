import os
from dotenv import load_dotenv
import pytz

load_dotenv()

# X API Credentials
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

# Optional API Keys
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY')

# Bot Configuration
ENABLE_CHINESE_POSTS = os.getenv('ENABLE_CHINESE_POSTS', 'true').lower() == 'true'
DRY_RUN = os.getenv('DRY_RUN', 'false').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Timezone Configuration
TEXAS_TZ = pytz.timezone('America/Chicago')
BEIJING_TZ = pytz.timezone('Asia/Shanghai')

# Schedule Times (24-hour format) - Texas & Beijing 7:00, 8:00, 9:00 AM
SCHEDULE_CONFIG = {
    'bible_verse': {'hour': 7, 'minute': 0},
    'combined_markets': {'hour': 8, 'minute': 0},
    'world_news': {'hour': 9, 'minute': 0},
}

# Twitter API Rate Limits (Free Tier: 500 tweets/month)
MAX_TWEETS_PER_DAY = 50
TWEET_CHAR_LIMIT = 280

# API Endpoints
BIBLE_API_URL = "https://bible-api.com"
NEWS_API_URL = "https://newsapi.org/v2"
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

# Top crypto assets for combined markets posts
TOP_CRYPTO_ASSETS = ['bitcoin', 'ethereum', 'binancecoin', 'solana']

