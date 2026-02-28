import requests
import random
import os
from dotenv import load_dotenv
from utils.logger import setup_logger
from utils.translator import translator

# Load environment variables
load_dotenv()

logger = setup_logger(__name__)

# Complete list of Bible books with chapter counts
# Format: (book_name, total_chapters)
BIBLE_BOOKS = [
    # Old Testament
    ("Genesis", 50), ("Exodus", 40), ("Leviticus", 27), ("Numbers", 36), ("Deuteronomy", 34),
    ("Joshua", 24), ("Judges", 21), ("Ruth", 4), ("1 Samuel", 31), ("2 Samuel", 24),
    ("1 Kings", 22), ("2 Kings", 25), ("1 Chronicles", 29), ("2 Chronicles", 36),
    ("Ezra", 10), ("Nehemiah", 13), ("Esther", 10), ("Job", 42),
    ("Psalms", 150), ("Proverbs", 31), ("Ecclesiastes", 12), ("Song of Solomon", 8),
    ("Isaiah", 66), ("Jeremiah", 52), ("Lamentations", 5), ("Ezekiel", 48), ("Daniel", 12),
    ("Hosea", 14), ("Joel", 3), ("Amos", 9), ("Obadiah", 1), ("Jonah", 4),
    ("Micah", 7), ("Nahum", 3), ("Habakkuk", 3), ("Zephaniah", 3), ("Haggai", 2),
    ("Zechariah", 14), ("Malachi", 4),
    # New Testament
    ("Matthew", 28), ("Mark", 16), ("Luke", 24), ("John", 21), ("Acts", 28),
    ("Romans", 16), ("1 Corinthians", 16), ("2 Corinthians", 13), ("Galatians", 6),
    ("Ephesians", 6), ("Philippians", 4), ("Colossians", 4), ("1 Thessalonians", 5),
    ("2 Thessalonians", 3), ("1 Timothy", 6), ("2 Timothy", 4), ("Titus", 3),
    ("Philemon", 1), ("Hebrews", 13), ("James", 5), ("1 Peter", 5), ("2 Peter", 3),
    ("1 John", 5), ("2 John", 1), ("3 John", 1), ("Jude", 1), ("Revelation", 22)
]

# Popular inspiring verses as fallback (if random verse fails)
FALLBACK_VERSES = [
    "Philippians 4:13", "Jeremiah 29:11", "Proverbs 3:5-6", "Isaiah 41:10",
    "Romans 8:28", "Psalm 23:1", "Matthew 6:33", "Joshua 1:9", "John 3:16"
]

class BibleVerseModule:
    """Generate inspiring Bible verse posts"""
    
    def __init__(self):
        # bible-api.com configuration (free, KJV translation)
        self.api_url = "https://bible-api.com"
    
    def get_random_reference(self):
        """Generate a random Bible verse reference"""
        # Select random book and chapter
        book_name, total_chapters = random.choice(BIBLE_BOOKS)
        chapter = random.randint(1, total_chapters)
        
        # Most verses have 1-30 verses per chapter, use safe range
        verse = random.randint(1, 20)
        
        reference = f"{book_name} {chapter}:{verse}"
        return reference
    
    def get_verse(self, reference=None):
        """Fetch a Bible verse from bible-api.com (KJV version)"""
        if not reference:
            reference = self.get_random_reference()
        
        try:
            # Request from bible-api.com (simple URL format)
            url = f"{self.api_url}/{reference}"
            params = {"translation": "kjv"}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            verse_text = data['text'].strip()
            verse_reference = data['reference']
            
            # If verse is too short or empty, try again with fallback
            if len(verse_text) < 20:
                logger.warning(f"Verse too short ({len(verse_text)} chars), using fallback")
                reference = random.choice(FALLBACK_VERSES)
                return self.get_verse(reference)
            
            # If verse is too long, use fallback
            if len(verse_text) > 500:
                logger.warning(f"Verse too long ({len(verse_text)} chars), using fallback")
                reference = random.choice(FALLBACK_VERSES)
                return self.get_verse(reference)
            
            logger.info(f"Fetched verse: {verse_reference} ({len(verse_text)} chars)")
            return verse_text, verse_reference
        
        except Exception as e:
            logger.warning(f"Error fetching verse ({reference}): {e}. Using fallback.")
            # Try fallback verse
            if reference not in FALLBACK_VERSES:
                try:
                    fallback_ref = random.choice(FALLBACK_VERSES)
                    return self.get_verse(fallback_ref)
                except Exception:
                    pass
            
            # Ultimate fallback
            return "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.", "John 3:16"
    
    def format_tweet(self, verse_text, reference):
        """Format verse as a simple tweet (just scripture and reference)"""
        # Clean up the verse text
        verse_text = verse_text.replace('\n', ' ').strip()
        
        # Simple format: just the verse and reference (KJV)
        tweet = f"\"{verse_text}\"\n\n{reference} (KJV)"
        
        # Ensure it fits Twitter's character limit
        if len(tweet) > 270:
            # Truncate verse text if needed
            max_verse_length = 270 - len(f"\"\"\n\n{reference} (KJV)")
            verse_text = verse_text[:max_verse_length-3] + "..."
            tweet = f"\"{verse_text}\"\n\n{reference} (KJV)"
        
        return tweet
    
    def generate_post(self):
        """Generate both English and Chinese posts"""
        verse_text, reference = self.get_verse()
        english_tweet = self.format_tweet(verse_text, reference)
        
        # Translate to Chinese (simple format)
        chinese_verse = translator.translate(verse_text)
        chinese_reference = translator.translate(reference)
        chinese_tweet = f"\"{chinese_verse}\"\n\n{chinese_reference} (KJV)"
        
        # Ensure Chinese tweet fits limit
        if len(chinese_tweet) > 280:
            max_length = 280 - len(f"\"\"\n\n{chinese_reference} (KJV)")
            chinese_verse = chinese_verse[:max_length-3] + "..."
            chinese_tweet = f"\"{chinese_verse}\"\n\n{chinese_reference} (KJV)"
        
        return english_tweet, chinese_tweet

# Global instance
bible_module = BibleVerseModule()

