#!/usr/bin/env python3
"""
Test all post types by posting them to X
This will post ALL 6 content types (15 tweets total)
"""

import sys
import os
import argparse
from utils.logger import setup_logger
from utils.twitter_client import twitter_client
from utils.ai_thread_generator import ai_thread_generator
from modules.bible_verse import bible_module
from modules.combined_markets import combined_markets_module
from modules.world_news import news_module
import config

logger = setup_logger(__name__)

def test_all_posts(auto_confirm=False):
    """Test all post types by actually posting to X
    
    Args:
        auto_confirm: If True, skip confirmation prompt (for cloud deployment)
    """
    
    print("="*80)
    print("TESTING ALL POST TYPES - WILL POST TO X!")
    print("="*80)
    print()
    
    # Check if dry run
    if config.DRY_RUN:
        print("⚠️  DRY_RUN mode is ON - tweets will NOT be posted")
        print("   To actually post, set DRY_RUN=false in .env")
    else:
        print("✅ DRY_RUN mode is OFF - tweets WILL BE POSTED")
        
        # Only ask for confirmation if not auto-confirmed (for local testing)
        if not auto_confirm:
            response = input("\n⚠️  This will post 15 tweets to X. Continue? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Test cancelled")
                sys.exit(0)
        else:
            print("🤖 Auto-confirm mode: Proceeding without prompt (cloud deployment)")
    
    print("\nPosting 15 tweets (6 thread types)...")
    print("-"*80)
    
    success_count = 0
    total_count = 6
    
    # ========================================================================
    # 1. TEXAS - BIBLE VERSE (3 tweets)
    # ========================================================================
    print("\n[1/6] Texas - Bible Verse (3-tweet thread)...")
    try:
        verse_text, reference = bible_module.get_verse()
        english_main = bible_module.format_tweet(verse_text, reference)
        english_replies = ai_thread_generator.generate_bible_thread(verse_text, reference)
        english_replies = english_replies[:2]
        english_thread = [english_main] + english_replies
        
        if twitter_client.post_thread(english_thread, language='en'):
            print("   ✅ Posted successfully (3 tweets)")
            success_count += 1
        else:
            print("   ❌ Failed to post")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # ========================================================================
    # 2. TEXAS - US MARKETS (3 tweets)
    # ========================================================================
    print("\n[2/6] Texas - US Markets (3-tweet thread)...")
    try:
        english = combined_markets_module.generate_us_post()
        english_replies = ai_thread_generator.generate_financial_thread(english, "Market analysis")
        english_replies = english_replies[:2]
        english_thread = [english] + english_replies
        
        if twitter_client.post_thread(english_thread, language='en'):
            print("   ✅ Posted successfully (3 tweets)")
            success_count += 1
        else:
            print("   ❌ Failed to post")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # ========================================================================
    # 3. TEXAS - AI NEWS (3 tweets)
    # ========================================================================
    print("\n[3/6] Texas - AI News (3-tweet thread)...")
    try:
        english, _ = news_module.generate_post()
        english_replies = ai_thread_generator.generate_news_thread(english, "News context")
        english_replies = english_replies[:2]
        english_thread = [english] + english_replies
        
        if twitter_client.post_thread(english_thread, language='en'):
            print("   ✅ Posted successfully (3 tweets)")
            success_count += 1
        else:
            print("   ❌ Failed to post")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # ========================================================================
    # 4. BEIJING - BIBLE VERSE (2 tweets)
    # ========================================================================
    print("\n[4/6] Beijing - Bible Verse (2-tweet thread)...")
    try:
        verse_text, reference = bible_module.get_verse()
        
        # Translate to Chinese
        from utils.translator import translator
        chinese_verse = translator.translate(verse_text)
        chinese_reference = translator.translate(reference)
        chinese_main = f'"{chinese_verse}"\n\n{chinese_reference} (KJV)'
        
        if len(chinese_main) > 280:
            max_length = 280 - len(f'"\n\n{chinese_reference} (KJV)')
            chinese_verse = chinese_verse[:max_length-3] + "..."
            chinese_main = f'"{chinese_verse}"\n\n{chinese_reference} (KJV)'
        
        chinese_replies = ai_thread_generator.generate_bible_thread(verse_text, reference, language='zh')
        chinese_replies = chinese_replies[:1]
        chinese_thread = [chinese_main] + chinese_replies
        
        if twitter_client.post_thread(chinese_thread, language='zh'):
            print("   ✅ Posted successfully (2 tweets)")
            success_count += 1
        else:
            print("   ❌ Failed to post")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # ========================================================================
    # 5. BEIJING - CHINESE MARKETS (2 tweets)
    # ========================================================================
    print("\n[5/6] Beijing - Chinese Markets (2-tweet thread)...")
    try:
        chinese = combined_markets_module.generate_chinese_post()
        chinese_replies = ai_thread_generator.generate_financial_thread(chinese, "Market analysis", language='zh')
        chinese_replies = chinese_replies[:1]
        chinese_thread = [chinese] + chinese_replies
        
        if twitter_client.post_thread(chinese_thread, language='zh'):
            print("   ✅ Posted successfully (2 tweets)")
            success_count += 1
        else:
            print("   ❌ Failed to post")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # ========================================================================
    # 6. BEIJING - AI NEWS (2 tweets)
    # ========================================================================
    print("\n[6/6] Beijing - AI News (2-tweet thread)...")
    try:
        _, chinese = news_module.generate_post()
        chinese_replies = ai_thread_generator.generate_news_thread(chinese, "News context", language='zh')
        chinese_replies = chinese_replies[:1]
        chinese_thread = [chinese] + chinese_replies
        
        if twitter_client.post_thread(chinese_thread, language='zh'):
            print("   ✅ Posted successfully (2 tweets)")
            success_count += 1
        else:
            print("   ❌ Failed to post")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "="*80)
    print(f"TEST COMPLETE: {success_count}/{total_count} thread types posted successfully")
    print("="*80)
    
    if success_count == total_count:
        print("✅ All posts successful!")
        print(f"   Total tweets posted: 15")
        print(f"   Daily limit remaining: {50 - 15} tweets")
    else:
        print(f"⚠️  Some posts failed ({total_count - success_count} failures)")
    
    print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Test all post types by posting to X'
    )
    parser.add_argument(
        '--yes',
        action='store_true',
        help='Auto-confirm without prompting (for cloud deployment)'
    )
    
    args = parser.parse_args()
    test_all_posts(auto_confirm=args.yes)

