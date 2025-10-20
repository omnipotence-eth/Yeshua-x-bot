from deep_translator import GoogleTranslator
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ChineseTranslator:
    """Handle English to Chinese translations"""
    
    def __init__(self):
        self.translator = GoogleTranslator(source='en', target='zh-CN')
    
    def translate(self, text):
        """Translate English text to Simplified Chinese"""
        try:
            translated = self.translator.translate(text)
            logger.info(f"Translated: {text[:50]}... -> {translated[:50]}...")
            return translated
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text  # Return original if translation fails
    
    def translate_with_limit(self, text, char_limit=280):
        """Translate text and ensure it stays within character limit"""
        translated = self.translate(text)
        
        # If translated text exceeds limit, truncate intelligently
        if len(translated) > char_limit:
            translated = translated[:char_limit-3] + "..."
            logger.warning(f"Translated text truncated to {char_limit} chars")
        
        return translated

# Global translator instance
translator = ChineseTranslator()

