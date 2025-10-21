#!/usr/bin/env python3
"""
Yeshua X Bot - Automated posting bot for inspirational and market updates
"""

import sys
import argparse
from utils.logger import setup_logger
from scheduler import bot_scheduler
import config

logger = setup_logger(__name__)

def validate_config():
    """Validate that required configuration is present"""
    required_vars = [
        'TWITTER_API_KEY',
        'TWITTER_API_SECRET',
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET',
        'TWITTER_BEARER_TOKEN'
    ]
    
    missing = []
    for var in required_vars:
        if not getattr(config, var):
            missing.append(var)
    
    if missing:
        logger.error(f"Missing required environment variables: {', '.join(missing)}")
        logger.error("Please copy .env.example to .env and fill in your credentials")
        return False
    
    return True

def test_modules():
    """Test all modules by generating sample posts"""
    logger.info("Testing all modules...")
    
    from modules.bible_verse import bible_module
    from modules.combined_markets import combined_markets_module
    from modules.world_news import news_module
    
    # Test Bible Verse
    try:
        logger.info("Testing Bible Verse module...")
        verse_text, reference = bible_module.get_verse()
        english = bible_module.format_tweet(verse_text, reference)
        logger.info(f"✓ Bible Verse module working")
        logger.info(f"  Preview: {english[:100]}...")
    except Exception as e:
        logger.error(f"✗ Bible Verse module failed: {e}")
    
    # Test Combined Markets
    try:
        logger.info("Testing Combined Markets module...")
        english, chinese = combined_markets_module.generate_post()
        logger.info(f"✓ Combined Markets module working")
        logger.info(f"  English preview: {english[:100]}...")
        if config.ENABLE_CHINESE_POSTS:
            logger.info(f"  Chinese preview: {chinese[:100]}...")
    except Exception as e:
        logger.error(f"✗ Combined Markets module failed: {e}")
    
    # Test World News
    try:
        logger.info("Testing World News module...")
        english, chinese = news_module.generate_post()
        logger.info(f"✓ World News module working")
        logger.info(f"  English preview: {english[:100]}...")
        if config.ENABLE_CHINESE_POSTS:
            logger.info(f"  Chinese preview: {chinese[:100]}...")
    except Exception as e:
        logger.error(f"✗ World News module failed: {e}")
    
    logger.info("Module testing complete!")

def run_bot():
    """Main entry point to run the bot"""
    logger.info("=" * 60)
    logger.info("YESHUA X BOT")
    logger.info("=" * 60)
    logger.info("")
    
    # Validate configuration
    if not validate_config():
        logger.error("Configuration validation failed. Exiting...")
        sys.exit(1)
    
    logger.info(f"✓ Configuration validated")
    logger.info(f"✓ Texas timezone: {config.TEXAS_TZ}")
    logger.info(f"✓ Beijing timezone: {config.BEIJING_TZ}")
    logger.info(f"✓ Chinese posts enabled: {config.ENABLE_CHINESE_POSTS}")
    logger.info(f"✓ Dry run mode: {config.DRY_RUN}")
    logger.info("")
    
    # Start the scheduler
    try:
        bot_scheduler.start()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user. Goodbye!")
    except Exception as e:
        logger.error(f"Bot error: {e}")
        sys.exit(1)

def main():
    """Parse arguments and run appropriate command"""
    parser = argparse.ArgumentParser(
        description='Yeshua X Bot - Automated posting bot for inspirational and market updates'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test all modules without posting'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run in dry-run mode (no actual posts)'
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        config.DRY_RUN = True
        logger.info("Running in DRY RUN mode - no tweets will be posted")
    
    if args.test:
        test_modules()
    else:
        run_bot()

if __name__ == '__main__':
    main()

