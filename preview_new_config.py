#!/usr/bin/env python3
"""
Preview the new optimized bot configuration
Shows exactly what will be posted WITHOUT actually posting to X
"""

from modules.bible_verse import bible_module
from modules.combined_markets import combined_markets_module
from modules.world_news import news_module
from utils.ai_thread_generator import ai_thread_generator

def print_header(title):
    """Print section header"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def print_thread(tweets, title):
    """Print a thread"""
    print(f"\n{title}:")
    print("-"*80)
    for i, tweet in enumerate(tweets, 1):
        print(f"\n[Tweet {i}] ({len(tweet)} chars)")
        print(tweet)
    print(f"\nTotal: {len(tweets)} tweets")

# ============================================================================
# CONFIGURATION SUMMARY
# ============================================================================
print_header("YESHUA X BOT - NEW OPTIMIZED CONFIGURATION")
print("\nDaily Schedule:")
print("  Texas Time (English 3-tweet threads):")
print("    7:00 AM - Bible Verse (KJV)")
print("    8:00 AM - US Markets (S&P, Dow, Nasdaq + Top Crypto)")
print("    9:00 AM - AI Breakthroughs (US/Global AI News)")
print("\n  Beijing Time (Chinese 2-tweet threads):")
print("    7:00 AM - 圣经经文 (Same verse, translated)")
print("    8:00 AM - 中国市场 (Shanghai, Hang Seng, Alibaba + Crypto)")
print("    9:00 AM - AI突破 (Chinese AI News)")
print("\nDaily Tweet Count:")
print("  - Texas: 3 content × 3 tweets = 9 tweets/day")
print("  - Beijing: 3 content × 2 tweets = 6 tweets/day")
print("  - TOTAL: 15 tweets/day = 450 tweets/month")
print("  - FREE TIER LIMIT: 500 tweets/month")
print("  - STATUS: Within limits! (50 tweet buffer)")

# ============================================================================
# 1. BIBLE VERSE
# ============================================================================
print_header("1. BIBLE VERSE")
print("\nFetching Bible verse from bible-api.com (KJV)...")

try:
    # Generate the same verse for both English and Chinese
    verse_text, reference = bible_module.get_verse()
    english_main = bible_module.format_tweet(verse_text, reference)
    
    # Translate the SAME verse to Chinese (don't generate a new one)
    from utils.translator import translator
    chinese_verse = translator.translate(verse_text)
    chinese_reference = translator.translate(reference)
    chinese_main = f'"{chinese_verse}"\n\n{chinese_reference} (KJV)'
    
    # Ensure Chinese tweet fits limit
    if len(chinese_main) > 280:
        max_length = 280 - len(f'"\n\n{chinese_reference} (KJV)')
        chinese_verse = chinese_verse[:max_length-3] + "..."
        chinese_main = f'"{chinese_verse}"\n\n{chinese_reference} (KJV)'
    
    print(f"Verse: {reference}")
    print(f"Text: {verse_text[:100]}...")
    
    # English 3-tweet thread
    print("\nGenerating English AI thread (2 replies)...")
    english_replies = ai_thread_generator.generate_bible_thread(verse_text, reference)
    english_replies = english_replies[:2]
    english_thread = [english_main] + english_replies
    
    print_thread(english_thread, "TEXAS (English 3-tweet thread)")
    
    # Chinese 2-tweet thread (using SAME verse, translated)
    print("\nGenerating Chinese AI thread (1 reply)...")
    chinese_replies = ai_thread_generator.generate_bible_thread(verse_text, reference, language='zh')
    chinese_replies = chinese_replies[:1]
    chinese_thread = [chinese_main] + chinese_replies
    
    print_thread(chinese_thread, "BEIJING (Chinese 2-tweet thread)")
    
    print("\n[OK] Bible verse preview complete")

except Exception as e:
    print(f"\n[ERROR] Bible verse failed: {e}")

# ============================================================================
# 2. COMBINED MARKETS
# ============================================================================
print_header("2. COMBINED MARKETS")
print("\nFetching US & Chinese market data from yfinance, CoinGecko, Alternative.me...")

try:
    english, chinese = combined_markets_module.generate_post()
    
    print("[OK] Market data fetched successfully")
    
    # English 3-tweet thread
    print("\nGenerating English AI thread (2 replies)...")
    english_replies = ai_thread_generator.generate_financial_thread(english, "Market analysis")
    english_replies = english_replies[:2]
    english_thread = [english] + english_replies
    
    print_thread(english_thread, "TEXAS (English 3-tweet thread)")
    
    # Chinese 2-tweet thread
    print("\nGenerating Chinese AI thread (1 reply)...")
    chinese_replies = ai_thread_generator.generate_financial_thread(chinese, "Market analysis", language='zh')
    chinese_replies = chinese_replies[:1]
    chinese_thread = [chinese] + chinese_replies
    
    print_thread(chinese_thread, "BEIJING (Chinese 2-tweet thread)")
    
    print("\n[OK] Combined markets preview complete")

except Exception as e:
    print(f"\n[ERROR] Combined markets failed: {e}")

# ============================================================================
# 3. WORLD NEWS
# ============================================================================
print_header("3. AI BREAKTHROUGHS (AI-Only News)")
print("\nFetching AI breakthrough news from NewsAPI...")

try:
    english, chinese = news_module.generate_post()
    
    print("[OK] News article fetched successfully")
    
    # English 3-tweet thread
    print("\nGenerating English AI thread (2 replies)...")
    english_replies = ai_thread_generator.generate_news_thread(english, "News context")
    english_replies = english_replies[:2]
    english_thread = [english] + english_replies
    
    print_thread(english_thread, "TEXAS (English 3-tweet thread)")
    
    # Chinese 2-tweet thread
    print("\nGenerating Chinese AI thread (1 reply)...")
    chinese_replies = ai_thread_generator.generate_news_thread(chinese, "News context", language='zh')
    chinese_replies = chinese_replies[:1]
    chinese_thread = [chinese] + chinese_replies
    
    print_thread(chinese_thread, "BEIJING (Chinese 2-tweet thread)")
    
    print("\n[OK] World news preview complete")

except Exception as e:
    print(f"\n[ERROR] World news failed: {e}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print(" PREVIEW COMPLETE!")
print("="*80)

print("\nYour bot is configured to post:")
print("\n1. BIBLE VERSE")
print("   - Daily inspiration from KJV (same verse for both languages)")
print("   - Texas: 3-tweet thread with spiritual insights (English)")
print("   - Beijing: 2-tweet thread with AI context (Chinese, translated)")

print("\n2. COMBINED MARKETS")
print("   - Texas: S&P 500, Dow Jones, Nasdaq + BTC, ETH, BNB, SOL")
print("   - Beijing: Shanghai, Hang Seng, Alibaba + BTC, ETH, BNB")
print("   - Fear & Greed Index for both")
print("   - Texas: 3-tweet thread with AI market analysis")
print("   - Beijing: 2-tweet thread with AI insights (translated)")

print("\n3. AI BREAKTHROUGHS (AI-only content)")
print("   - Texas: US/Global AI news (OpenAI, Google, Microsoft, Anthropic)")
print("   - Beijing: Chinese AI news (Baidu, ByteDance, Alibaba, Tencent)")
print("   - Texas: 3-tweet thread with deeper AI context")
print("   - Beijing: 2-tweet thread with AI analysis (translated)")

print("\nAPIs Used:")
print("  - bible-api.com (Free, KJV)")
print("  - NewsAPI.org (100 requests/day)")
print("  - yfinance (Unlimited)")
print("  - CoinGecko (Free tier)")
print("  - Alternative.me (Free, Fear & Greed)")
print("  - Groq AI (Free $5/month, Llama 3.3)")
print("  - Google Translator (Free)")

print("\nDaily Tweet Count:")
print("  Texas (English):  9 tweets")
print("  Beijing (Chinese): 6 tweets")
print("  -------------------------")
print("  TOTAL:            15 tweets/day")
print("  Monthly:          450 tweets/month")
print("  FREE TIER:        500 tweets/month")
print("  BUFFER:           50 tweets")

print("\nStatus: Ready for deployment!")
print("="*80 + "\n")

