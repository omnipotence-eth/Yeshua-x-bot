import os
from groq import Groq
from utils.logger import setup_logger

logger = setup_logger(__name__)

class AIThreadGenerator:
    """Generate engaging X/Twitter threads using Groq AI"""
    
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY', '')
        
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
            self.enabled = True
            logger.info("AI Thread Generator initialized with Groq API")
        else:
            self.client = None
            self.enabled = False
            logger.warning("No GROQ_API_KEY found - AI threads disabled")
    
    def generate_thread(self, main_tweet, data_context, max_tweets=2):
        """
        Generate a thread from a main tweet
        
        Args:
            main_tweet: The main tweet content
            data_context: Additional data/context about the topic
            max_tweets: Maximum number of follow-up tweets (default: 2)
        
        Returns:
            List of follow-up tweets (main tweet not included) or empty list if disabled
        """
        if not self.enabled:
            logger.debug("AI threads disabled, returning empty list")
            return []
        
        try:
            # Create prompt for Groq
            prompt = f"""You are a social media expert creating engaging Twitter/X threads.

MAIN TWEET:
{main_tweet}

CONTEXT/DATA:
{data_context}

Create {max_tweets} follow-up tweets that:
1. Provide interesting insights or explanations
2. Are concise and engaging (under 280 characters each)
3. Use clear, simple language
4. Don't use emojis
5. Add value to the main tweet

Format: Return ONLY the follow-up tweets, one per line, numbered 1., 2., etc.
Do NOT include the main tweet or any hashtags."""

            # Call Groq API
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Latest Llama model
                messages=[
                    {"role": "system", "content": "You are a concise social media expert. Create engaging, informative tweets without emojis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500,
                top_p=0.9
            )
            
            # Parse response
            content = response.choices[0].message.content.strip()
            
            # Extract tweets
            follow_up_tweets = []
            for line in content.split('\n'):
                line = line.strip()
                # Remove numbering like "1.", "2.", etc.
                if line and any(line.startswith(f"{i}.") for i in range(1, 10)):
                    tweet = line.split('.', 1)[1].strip()
                    if tweet and len(tweet) <= 280:
                        follow_up_tweets.append(tweet)
            
            # Limit to max_tweets
            follow_up_tweets = follow_up_tweets[:max_tweets]
            
            logger.info(f"Generated {len(follow_up_tweets)} follow-up tweets")
            return follow_up_tweets
        
        except Exception as e:
            logger.error(f"Error generating AI thread: {e}")
            return []
    
    def generate_financial_thread(self, main_tweet, market_data):
        """Generate a thread for financial market updates"""
        context = f"Market data: {market_data}\n\nProvide insights about market trends, what's driving the changes, and what investors should watch."
        return self.generate_thread(main_tweet, context, max_tweets=2)
    
    def generate_crypto_thread(self, main_tweet, crypto_data):
        """Generate a thread for crypto market updates"""
        context = f"Crypto data: {crypto_data}\n\nProvide insights about crypto market movements, trends, and important factors."
        return self.generate_thread(main_tweet, context, max_tweets=2)
    
    def generate_news_thread(self, main_tweet, news_items):
        """Generate a thread for news updates"""
        context = f"News items: {news_items}\n\nProvide deeper insights or explanations about these news items and their significance."
        return self.generate_thread(main_tweet, context, max_tweets=2)
    
    def generate_bible_thread(self, verse_text, reference):
        """Generate an insightful thread for a Bible verse"""
        if not self.enabled:
            return []
        
        try:
            prompt = f"""You are a Christian faith leader sharing Bible insights.

BIBLE VERSE:
"{verse_text}"
- {reference}

Create 2-3 follow-up tweets (under 280 chars each) that provide:
1. Historical context (who wrote it, why, when)
2. Practical modern application
3. An inspiring closing thought

Be encouraging, accessible, and avoid clichés. No emojis.

Format: Return ONLY the tweets, numbered 1., 2., 3."""

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a thoughtful Bible teacher providing clear, practical insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600,
                top_p=0.9
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract tweets
            follow_up_tweets = []
            for line in content.split('\n'):
                line = line.strip()
                if line and any(line.startswith(f"{i}.") for i in range(1, 10)):
                    tweet = line.split('.', 1)[1].strip()
                    if tweet and len(tweet) <= 280:
                        follow_up_tweets.append(tweet)
            
            logger.info(f"Generated {len(follow_up_tweets)} Bible thread tweets")
            return follow_up_tweets[:3]  # Max 3 replies
        
        except Exception as e:
            logger.error(f"Error generating Bible thread: {e}")
            return []

# Global AI thread generator instance
ai_thread_generator = AIThreadGenerator()

