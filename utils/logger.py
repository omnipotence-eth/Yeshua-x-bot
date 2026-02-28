import logging
import sys
from datetime import datetime
import config

def setup_logger(name):
    """Set up logger with consistent formatting"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Console handler with UTF-8 encoding for Chinese characters
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except (AttributeError, OSError):
            pass  # reconfigure not available or failed; continue with default
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger

def log_tweet(content, language='en', dry_run=False):
    """Log tweet content before posting"""
    logger = setup_logger('tweet_logger')
    status = "DRY RUN" if dry_run else "POSTING"
    logger.info(f"[{status}] [{language.upper()}] Tweet: {content[:100]}...")

