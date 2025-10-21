import requests
from datetime import datetime, timedelta
from utils.logger import setup_logger
from utils.translator import translator
import os

logger = setup_logger(__name__)

class WorldNewsModule:
    """Generate single top AI breakthrough article"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY', '')
        self.base_url = "https://newsapi.org/v2/everything"
        
        # AI breakthrough search terms for US/Global audience (Texas)
        self.us_ai_terms = [
            'OpenAI breakthrough',
            'ChatGPT advancement', 
            'Google AI innovation',
            'Anthropic Claude',
            'Microsoft AI',
            'artificial intelligence breakthrough',
            'AI model release',
            'machine learning breakthrough'
        ]
        
        # AI breakthrough search terms for Chinese audience (Beijing)
        self.chinese_ai_terms = [
            'Baidu AI breakthrough',
            'ByteDance AI innovation',
            'Alibaba AI',
            'Tencent AI',
            'DeepSeek AI',
            'Chinese AI breakthrough',
            'China artificial intelligence',
            'Huawei AI innovation'
        ]
    
    def fetch_us_ai_news(self):
        """Fetch US/Global AI breakthrough news for Texas timezone"""
        if not self.api_key:
            logger.warning("No NEWS_API_KEY found, using mock data")
            return self._get_mock_us_ai_news()
        
        try:
            # Try each search term until we get results
            for term in self.us_ai_terms:
                params = {
                    'q': term,
                    'apiKey': self.api_key,
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'pageSize': 5,
                    'from': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
                }
                
                response = requests.get(self.base_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get('articles', [])
                    
                    if articles:
                        # Filter for positive/innovative AI news
                        filtered = [a for a in articles if self._is_ai_breakthrough(a)]
                        if filtered:
                            article = filtered[0]
                            logger.info(f"[US] Fetched AI news: {article['title'][:50]}")
                            return {
                                'title': article['title'][:150],
                                'source': article.get('source', {}).get('name', 'Tech News')
                            }
            
            # If no results found, return mock data
            logger.warning("No US AI news found, using mock data")
            return self._get_mock_us_ai_news()
            
        except Exception as e:
            logger.error(f"Error fetching US AI news: {e}")
            return self._get_mock_us_ai_news()
    
    def fetch_chinese_ai_news(self):
        """Fetch Chinese AI breakthrough news for Beijing timezone"""
        if not self.api_key:
            logger.warning("No NEWS_API_KEY found, using mock data")
            return self._get_mock_chinese_ai_news()
        
        try:
            # Try each search term until we get results
            for term in self.chinese_ai_terms:
                params = {
                    'q': term,
                    'apiKey': self.api_key,
                    'language': 'en',  # Fetch English articles about Chinese AI
                    'sortBy': 'publishedAt',
                    'pageSize': 5,
                    'from': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
                }
                
                response = requests.get(self.base_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get('articles', [])
                    
                    if articles:
                        # Filter for positive/innovative AI news
                        filtered = [a for a in articles if self._is_ai_breakthrough(a)]
                        if filtered:
                            article = filtered[0]
                            logger.info(f"[CN] Fetched AI news: {article['title'][:50]}")
                            return {
                                'title': article['title'][:150],
                                'source': article.get('source', {}).get('name', 'Tech News')
                            }
            
            # If no results found, return mock data
            logger.warning("No Chinese AI news found, using mock data")
            return self._get_mock_chinese_ai_news()
            
        except Exception as e:
            logger.error(f"Error fetching Chinese AI news: {e}")
            return self._get_mock_chinese_ai_news()
    
    def _is_ai_breakthrough(self, article):
        """Check if article is about AI breakthroughs (positive/innovative)"""
        # AI/tech keywords that indicate breakthroughs
        ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'gpt', 'llm', 
                      'neural network', 'deep learning', 'chatbot', 'model']
        
        # Positive breakthrough indicators
        positive_keywords = ['breakthrough', 'innovation', 'advancement', 'new', 'launch', 
                           'unveil', 'release', 'announce', 'improve', 'upgrade', 'revolutionize']
        
        # Negative keywords to filter out
        negative_keywords = ['crash', 'crisis', 'war', 'death', 'killed', 'disaster', 
                           'fraud', 'scandal', 'layoff', 'lawsuit', 'controversy', 'fail']
        
        title = article.get('title', '').lower()
        description = article.get('description', '').lower() if article.get('description') else ''
        
        # Must contain AI keywords
        has_ai = any(keyword in title or keyword in description for keyword in ai_keywords)
        if not has_ai:
            return False
        
        # Filter out negative news
        has_negative = any(keyword in title or keyword in description for keyword in negative_keywords)
        if has_negative:
            return False
        
        # Prefer articles with positive breakthrough indicators
        has_positive = any(keyword in title or keyword in description for keyword in positive_keywords)
        
        return has_positive or has_ai  # Return true if AI-related and no negative keywords
    
    def _get_mock_us_ai_news(self):
        """Fallback mock data for US AI news"""
        return {
            'title': 'OpenAI unveils GPT-5 with revolutionary reasoning capabilities and multimodal understanding',
            'source': 'TechCrunch'
        }
    
    def _get_mock_chinese_ai_news(self):
        """Fallback mock data for Chinese AI news"""
        return {
            'title': 'Baidu launches ERNIE 4.0 AI model, surpassing GPT-4 in Chinese language tasks',
            'source': 'South China Morning Post'
        }
    
    def generate_post(self):
        """Generate AI breakthrough articles (US for English, Chinese for Chinese)"""
        
        # Fetch US/Global AI news for English (Texas timezone)
        us_ai_news = self.fetch_us_ai_news()
        
        # Fetch Chinese AI news for Chinese (Beijing timezone)
        chinese_ai_news = self.fetch_chinese_ai_news()
        
        # Format English tweet (US AI breakthrough)
        english_tweet = f"🚀 AI Breakthrough\n\n"
        english_tweet += f"{us_ai_news['title']}\n\n"
        english_tweet += f"Source: {us_ai_news['source']}\n\n"
        english_tweet += "#AI #ArtificialIntelligence #Innovation"
        
        # Ensure it fits
        if len(english_tweet) > 280:
            max_title = 280 - len(f"🚀 AI Breakthrough\n\n\n\nSource: {us_ai_news['source']}\n\n#AI #ArtificialIntelligence #Innovation")
            english_tweet = f"🚀 AI Breakthrough\n\n"
            english_tweet += f"{us_ai_news['title'][:max_title]}...\n\n"
            english_tweet += f"Source: {us_ai_news['source']}\n\n"
            english_tweet += "#AI #ArtificialIntelligence #Innovation"
        
        # Format Chinese tweet (Chinese AI breakthrough, translated)
        title_cn = translator.translate(chinese_ai_news['title'])
        source_cn = translator.translate(chinese_ai_news['source'])
        
        chinese_tweet = f"🚀 人工智能突破\n\n"
        chinese_tweet += f"{title_cn}\n\n"
        chinese_tweet += f"来源: {source_cn}\n\n"
        chinese_tweet += "#人工智能 #AI #创新"
        
        # Ensure it fits
        if len(chinese_tweet) > 280:
            max_title = 280 - len(f"🚀 人工智能突破\n\n\n\n来源: {source_cn}\n\n#人工智能 #AI #创新")
            chinese_tweet = f"🚀 人工智能突破\n\n"
            chinese_tweet += f"{title_cn[:max_title]}...\n\n"
            chinese_tweet += f"来源: {source_cn}\n\n"
            chinese_tweet += "#人工智能 #AI #创新"
        
        return english_tweet, chinese_tweet

# Global instance
news_module = WorldNewsModule()
