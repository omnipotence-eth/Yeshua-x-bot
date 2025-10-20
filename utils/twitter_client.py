import tweepy
import config
import time
from pathlib import Path
from utils.logger import setup_logger, log_tweet

logger = setup_logger(__name__)

class TwitterClient:
    """Handle all Twitter API interactions"""
    
    def __init__(self):
        self.client = None
        self.api = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Twitter API client"""
        try:
            # Twitter API v2 client
            self.client = tweepy.Client(
                bearer_token=config.TWITTER_BEARER_TOKEN,
                consumer_key=config.TWITTER_API_KEY,
                consumer_secret=config.TWITTER_API_SECRET,
                access_token=config.TWITTER_ACCESS_TOKEN,
                access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET,
                wait_on_rate_limit=True
            )
            
            # Twitter API v1.1 (needed for media uploads)
            auth = tweepy.OAuth1UserHandler(
                config.TWITTER_API_KEY,
                config.TWITTER_API_SECRET,
                config.TWITTER_ACCESS_TOKEN,
                config.TWITTER_ACCESS_TOKEN_SECRET
            )
            self.api = tweepy.API(auth, wait_on_rate_limit=True)
            
            logger.info("Twitter client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {e}")
            raise
    
    def upload_media(self, image_path):
        """
        Upload an image to Twitter and return media_id
        
        Args:
            image_path: Path to image file
        
        Returns:
            media_id string or None if failed
        """
        try:
            if config.DRY_RUN:
                logger.info(f"DRY RUN mode - would upload image: {image_path}")
                return "fake_media_id_dry_run"
            
            # Upload using API v1.1
            media = self.api.media_upload(filename=str(image_path))
            logger.info(f"Image uploaded successfully - media_id: {media.media_id_string}")
            return media.media_id_string
        
        except Exception as e:
            logger.error(f"Failed to upload image: {e}")
            return None
    
    def post_tweet(self, content, language='en', image_path=None):
        """
        Post a tweet with optional image
        
        Args:
            content: Tweet text
            language: Language code ('en' or 'zh')
            image_path: Optional path to image file
        
        Returns:
            Tweet ID if successful, None if failed
        """
        if not content:
            logger.warning("Empty content, skipping tweet")
            return None
        
        # Truncate if too long
        if len(content) > config.TWEET_CHAR_LIMIT:
            content = content[:config.TWEET_CHAR_LIMIT-3] + "..."
            logger.warning(f"Tweet truncated to {config.TWEET_CHAR_LIMIT} chars")
        
        log_tweet(content, language, config.DRY_RUN)
        
        if config.DRY_RUN:
            logger.info("DRY RUN mode - tweet not posted")
            return "fake_tweet_id_dry_run"
        
        try:
            # Upload image if provided
            media_ids = None
            if image_path:
                media_id = self.upload_media(image_path)
                if media_id:
                    media_ids = [media_id]
            
            # Post tweet
            response = self.client.create_tweet(text=content, media_ids=media_ids)
            tweet_id = response.data['id']
            logger.info(f"Tweet posted successfully - ID: {tweet_id}")
            return tweet_id
        
        except tweepy.errors.TooManyRequests as e:
            logger.error(f"Rate limit exceeded: {e}")
            return None
        except tweepy.errors.Forbidden as e:
            logger.error(f"Forbidden - check API permissions: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            return None
    
    def post_thread(self, tweets, language='en', image_path=None):
        """
        Post a thread of tweets
        
        Args:
            tweets: List of tweet strings [main_tweet, reply1, reply2, ...]
            language: Language code
            image_path: Optional image for the first tweet
        
        Returns:
            True if all tweets posted successfully
        """
        if not tweets or len(tweets) == 0:
            logger.warning("Empty thread, skipping")
            return False
        
        try:
            # Post main tweet with optional image
            main_tweet_id = self.post_tweet(tweets[0], language, image_path)
            
            if not main_tweet_id:
                logger.error("Failed to post main tweet")
                return False
            
            # Post replies
            previous_tweet_id = main_tweet_id
            
            for i, reply_content in enumerate(tweets[1:], 1):
                if config.DRY_RUN:
                    logger.info(f"DRY RUN mode - would post reply {i}: {reply_content[:50]}...")
                    time.sleep(0.1)  # Simulate delay
                    continue
                
                try:
                    response = self.client.create_tweet(
                        text=reply_content,
                        in_reply_to_tweet_id=previous_tweet_id
                    )
                    previous_tweet_id = response.data['id']
                    logger.info(f"Thread reply {i} posted - ID: {previous_tweet_id}")
                    
                    # Small delay between tweets
                    time.sleep(2)
                
                except Exception as e:
                    logger.error(f"Failed to post thread reply {i}: {e}")
                    return False
            
            logger.info(f"Thread posted successfully ({len(tweets)} tweets)")
            return True
        
        except Exception as e:
            logger.error(f"Failed to post thread: {e}")
            return False
    
    def post_bilingual_tweet(self, english_content, chinese_content):
        """Post both English and Chinese versions"""
        success = True
        
        # Post English version
        if not self.post_tweet(english_content, 'en'):
            success = False
        
        # Post Chinese version if enabled
        if config.ENABLE_CHINESE_POSTS and chinese_content:
            if not self.post_tweet(chinese_content, 'zh'):
                success = False
        
        return success

# Global Twitter client instance
twitter_client = TwitterClient()

