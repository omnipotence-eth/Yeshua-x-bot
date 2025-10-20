from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import config
from utils.logger import setup_logger
from utils.twitter_client import twitter_client
from utils.ai_thread_generator import ai_thread_generator
from modules.bible_verse import bible_module
from modules.combined_markets import combined_markets_module
from modules.world_news import news_module

logger = setup_logger(__name__)

class BotScheduler:
    """Manage all scheduled posts for the bot (3 content types, 2 timezones)"""
    
    def __init__(self):
        self.scheduler = BlockingScheduler(timezone=str(config.TEXAS_TZ))
        self.setup_schedules()
    
    # ========================================================================
    # TEXAS TIME ZONE (ENGLISH POSTS - 3-tweet threads)
    # ========================================================================
    
    def post_bible_verse_texas(self):
        """Post Bible verse - Texas time (English 3-tweet thread)"""
        logger.info("[TEXAS] Posting Bible verse...")
        try:
            # Generate verse
            verse_text, reference = bible_module.get_verse()
            english_main = bible_module.format_tweet(verse_text, reference)
            
            # Generate AI thread (2 replies)
            english_replies = ai_thread_generator.generate_bible_thread(verse_text, reference)
            english_replies = english_replies[:2]  # Only 2 replies for 3-tweet thread
            
            # Post English thread (main + 2 replies)
            english_thread = [english_main] + english_replies
            twitter_client.post_thread(english_thread, language='en')
            
            logger.info("[TEXAS] Bible verse posted successfully")
        except Exception as e:
            logger.error(f"[TEXAS] Error posting Bible verse: {e}")
    
    def post_combined_markets_texas(self):
        """Post combined markets - Texas time (English 3-tweet thread)"""
        logger.info("[TEXAS] Posting combined markets...")
        try:
            # Generate combined markets post
            english, _ = combined_markets_module.generate_post()
            
            # Generate AI thread (2 replies)
            market_context = "Analyze these market movements and provide insights"
            english_replies = ai_thread_generator.generate_financial_thread(english, market_context)
            english_replies = english_replies[:2]  # Only 2 replies for 3-tweet thread
            
            # Post English thread (main + 2 replies)
            english_thread = [english] + english_replies
            twitter_client.post_thread(english_thread, language='en')
            
            logger.info("[TEXAS] Combined markets posted successfully")
        except Exception as e:
            logger.error(f"[TEXAS] Error posting combined markets: {e}")
    
    def post_world_news_texas(self):
        """Post world news - Texas time (English 3-tweet thread)"""
        logger.info("[TEXAS] Posting world news...")
        try:
            # Generate news post
            english, _ = news_module.generate_post()
            
            # Generate AI thread (2 replies)
            news_context = "Provide deeper insights and context about this news story"
            english_replies = ai_thread_generator.generate_news_thread(english, news_context)
            english_replies = english_replies[:2]  # Only 2 replies for 3-tweet thread
            
            # Post English thread (main + 2 replies)
            english_thread = [english] + english_replies
            twitter_client.post_thread(english_thread, language='en')
            
            logger.info("[TEXAS] World news posted successfully")
        except Exception as e:
            logger.error(f"[TEXAS] Error posting world news: {e}")
    
    # ========================================================================
    # BEIJING TIME ZONE (CHINESE POSTS - 2-tweet threads)
    # ========================================================================
    
    def post_bible_verse_beijing(self):
        """Post Bible verse - Beijing time (Chinese 2-tweet thread)"""
        logger.info("[BEIJING] Posting Bible verse...")
        try:
            # Generate verse
            verse_text, reference = bible_module.get_verse()
            _, chinese_main = bible_module.generate_post()
            
            # Generate AI thread (1 reply for Chinese)
            chinese_replies = ai_thread_generator.generate_bible_thread(verse_text, reference)
            chinese_replies = chinese_replies[:1]  # Only 1 reply for 2-tweet thread
            
            # Post Chinese thread (main + 1 reply)
            chinese_thread = [chinese_main] + chinese_replies
            twitter_client.post_thread(chinese_thread, language='zh')
            
            logger.info("[BEIJING] Bible verse posted successfully")
        except Exception as e:
            logger.error(f"[BEIJING] Error posting Bible verse: {e}")
    
    def post_combined_markets_beijing(self):
        """Post combined markets - Beijing time (Chinese 2-tweet thread)"""
        logger.info("[BEIJING] Posting combined markets...")
        try:
            # Generate combined markets post
            _, chinese = combined_markets_module.generate_post()
            
            # Generate AI thread (1 reply for Chinese)
            market_context = "Analyze these market movements"
            chinese_replies = ai_thread_generator.generate_financial_thread(chinese, market_context)
            chinese_replies = chinese_replies[:1]  # Only 1 reply for 2-tweet thread
            
            # Post Chinese thread (main + 1 reply)
            chinese_thread = [chinese] + chinese_replies
            twitter_client.post_thread(chinese_thread, language='zh')
            
            logger.info("[BEIJING] Combined markets posted successfully")
        except Exception as e:
            logger.error(f"[BEIJING] Error posting combined markets: {e}")
    
    def post_world_news_beijing(self):
        """Post world news - Beijing time (Chinese 2-tweet thread)"""
        logger.info("[BEIJING] Posting world news...")
        try:
            # Generate news post
            _, chinese = news_module.generate_post()
            
            # Generate AI thread (1 reply for Chinese)
            news_context = "Provide context about this news story"
            chinese_replies = ai_thread_generator.generate_news_thread(chinese, news_context)
            chinese_replies = chinese_replies[:1]  # Only 1 reply for 2-tweet thread
            
            # Post Chinese thread (main + 1 reply)
            chinese_thread = [chinese] + chinese_replies
            twitter_client.post_thread(chinese_thread, language='zh')
            
            logger.info("[BEIJING] World news posted successfully")
        except Exception as e:
            logger.error(f"[BEIJING] Error posting world news: {e}")
    
    # ========================================================================
    # SCHEDULER SETUP
    # ========================================================================
    
    def setup_schedules(self):
        """Set up all scheduled jobs"""
        
        logger.info("Setting up Texas timezone schedules (English 3-tweet threads)...")
        
        # Texas Time Zone - 7:00 AM, 8:00 AM, 9:00 AM
        self.scheduler.add_job(
            self.post_bible_verse_texas,
            CronTrigger(hour=7, minute=0, timezone=config.TEXAS_TZ),
            id='texas_bible_verse',
            name='Texas - Bible Verse (7:00 AM)'
        )
        
        self.scheduler.add_job(
            self.post_combined_markets_texas,
            CronTrigger(hour=8, minute=0, timezone=config.TEXAS_TZ),
            id='texas_combined_markets',
            name='Texas - Combined Markets (8:00 AM)'
        )
        
        self.scheduler.add_job(
            self.post_world_news_texas,
            CronTrigger(hour=9, minute=0, timezone=config.TEXAS_TZ),
            id='texas_world_news',
            name='Texas - World News (9:00 AM)'
        )
        
        logger.info("Setting up Beijing timezone schedules (Chinese 2-tweet threads)...")
        
        # Beijing Time Zone - 7:00 AM, 8:00 AM, 9:00 AM
        self.scheduler.add_job(
            self.post_bible_verse_beijing,
            CronTrigger(hour=7, minute=0, timezone=config.BEIJING_TZ),
            id='beijing_bible_verse',
            name='Beijing - Bible Verse (7:00 AM)'
        )
        
        self.scheduler.add_job(
            self.post_combined_markets_beijing,
            CronTrigger(hour=8, minute=0, timezone=config.BEIJING_TZ),
            id='beijing_combined_markets',
            name='Beijing - Combined Markets (8:00 AM)'
        )
        
        self.scheduler.add_job(
            self.post_world_news_beijing,
            CronTrigger(hour=9, minute=0, timezone=config.BEIJING_TZ),
            id='beijing_world_news',
            name='Beijing - World News (9:00 AM)'
        )
        
        logger.info(f"Scheduled {len(self.scheduler.get_jobs())} jobs")
    
    def print_schedule(self):
        """Print all scheduled jobs"""
        logger.info("=" * 70)
        logger.info("SCHEDULED JOBS")
        logger.info("=" * 70)
        
        jobs = self.scheduler.get_jobs()
        for job in jobs:
            logger.info(f"  • {job.name}")
            logger.info(f"    ID: {job.id}")
            logger.info("")
        
        logger.info("=" * 70)
        logger.info("DAILY TWEET COUNT:")
        logger.info("  Texas (English 3-tweet threads): 9 tweets/day")
        logger.info("  Beijing (Chinese 2-tweet threads): 6 tweets/day")
        logger.info("  TOTAL: 15 tweets/day = 450 tweets/month")
        logger.info("  FREE TIER LIMIT: 500 tweets/month")
        logger.info("  STATUS: Within limits! ✓")
        logger.info("=" * 70)
    
    def start(self):
        """Start the scheduler"""
        logger.info("Starting bot scheduler...")
        self.print_schedule()
        
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Scheduler stopped by user")
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
            raise

# Global scheduler instance
bot_scheduler = BotScheduler()
