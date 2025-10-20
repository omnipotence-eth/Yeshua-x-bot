import requests
from datetime import datetime, timedelta
from utils.logger import setup_logger
from utils.translator import translator
import os

logger = setup_logger(__name__)

class WorldNewsModule:
    """Generate single top news article from Finance, AI, or Robotics"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY', '')
        self.base_url = "https://newsapi.org/v2/everything"
        
        # Categories for focused news (will pick best one)
        self.categories = {
            'Finance': ['breakthrough finance', 'major investment', 'economic growth', 'fintech innovation'],
            'AI': ['AI breakthrough', 'ChatGPT', 'artificial intelligence innovation', 'OpenAI'],
            'Robotics': ['robotics breakthrough', 'automation innovation', 'robot advancement']
        }
        
        # Chinese-specific search terms
        self.chinese_categories = {
            'Finance': ['Alibaba', 'Tencent', 'China economy innovation'],
            'AI': ['Baidu AI', 'ByteDance AI', 'Chinese AI breakthrough'],
            'Robotics': ['China robotics', 'Chinese automation', 'BYD technology']
        }
    
    def fetch_global_news(self, category, search_terms):
        """Fetch global/Western news for a specific category"""
        if not self.api_key:
            logger.warning("No NEWS_API_KEY found, using mock data")
            return self._get_mock_global_news(category)
        
        try:
            # Try each search term until we get results
            for term in search_terms:
                params = {
                    'q': term,
                    'apiKey': self.api_key,
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'pageSize': 3,
                    'from': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
                }
                
                response = requests.get(self.base_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get('articles', [])
                    
                    if articles:
                        # Filter for positive/innovative news
                        filtered = [a for a in articles if self._is_positive_news(a)]
                        if filtered:
                            article = filtered[0]
                            logger.info(f"Fetched global {category} news: {article['title'][:50]}")
                            return {
                                'category': category,
                                'title': article['title'][:120],
                                'source': article.get('source', {}).get('name', 'News')
                            }
            
            # If no results found, return mock data
            logger.warning(f"No global {category} news found, using mock data")
            return self._get_mock_global_news(category)
            
        except Exception as e:
            logger.error(f"Error fetching global {category} news: {e}")
            return self._get_mock_global_news(category)
    
    def fetch_chinese_news(self, category, search_terms):
        """Fetch China/Asia-specific news for a specific category"""
        if not self.api_key:
            logger.warning("No NEWS_API_KEY found, using mock data")
            return self._get_mock_chinese_news(category)
        
        try:
            # Try each search term until we get results
            for term in search_terms:
                params = {
                    'q': term,
                    'apiKey': self.api_key,
                    'language': 'en',  # Fetch English articles about China
                    'sortBy': 'publishedAt',
                    'pageSize': 3,
                    'from': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
                }
                
                response = requests.get(self.base_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get('articles', [])
                    
                    if articles:
                        # Filter for positive/innovative news
                        filtered = [a for a in articles if self._is_positive_news(a)]
                        if filtered:
                            article = filtered[0]
                            logger.info(f"Fetched Chinese {category} news: {article['title'][:50]}")
                            return {
                                'category': category,
                                'title': article['title'][:120],
                                'source': article.get('source', {}).get('name', 'News')
                            }
            
            # If no results found, return mock data
            logger.warning(f"No Chinese {category} news found, using mock data")
            return self._get_mock_chinese_news(category)
            
        except Exception as e:
            logger.error(f"Error fetching Chinese {category} news: {e}")
            return self._get_mock_chinese_news(category)
    
    def _is_positive_news(self, article):
        """Check if news article is positive/constructive"""
        negative_keywords = ['crash', 'crisis', 'war', 'death', 'killed', 'disaster', 
                            'fraud', 'scandal', 'layoff', 'bankruptcy']
        
        title = article.get('title', '').lower()
        description = article.get('description', '').lower()
        
        # Filter out negative news
        for keyword in negative_keywords:
            if keyword in title or keyword in description:
                return False
        
        return True
    
    def _get_mock_global_news(self, category):
        """Fallback mock data for global news"""
        mock_data = {
            'Finance': {
                'category': 'Finance',
                'title': 'Global markets show resilience amid economic recovery',
                'source': 'Financial Times'
            },
            'AI': {
                'category': 'AI',
                'title': 'OpenAI announces breakthrough in natural language processing',
                'source': 'Tech News'
            },
            'Robotics': {
                'category': 'Robotics',
                'title': 'Tesla unveils advanced humanoid robot for manufacturing',
                'source': 'Innovation Daily'
            }
        }
        return mock_data.get(category, mock_data['Finance'])
    
    def _get_mock_chinese_news(self, category):
        """Fallback mock data for Chinese news"""
        mock_data = {
            'Finance': {
                'category': 'Finance',
                'title': 'Chinese tech stocks rally as economic indicators improve',
                'source': 'Asia Markets'
            },
            'AI': {
                'category': 'AI',
                'title': 'Baidu launches advanced AI language model competing globally',
                'source': 'China Tech'
            },
            'Robotics': {
                'category': 'Robotics',
                'title': 'Chinese manufacturers adopt AI-powered robotics at record pace',
                'source': 'Manufacturing Asia'
            }
        }
        return mock_data.get(category, mock_data['Finance'])
    
    def generate_post(self):
        """Generate single top news article (global for EN, China-focused for ZH)"""
        
        # Fetch ONE best global news article for English version
        best_global_news = None
        for category, search_terms in self.categories.items():
            news_item = self.fetch_global_news(category, search_terms)
            if news_item:
                best_global_news = news_item
                break  # Take the first good result
        
        # Fallback if no news found
        if not best_global_news:
            best_global_news = self._get_mock_global_news('AI')
        
        # Fetch ONE best Chinese/Asian news article for Chinese version
        best_chinese_news = None
        for category, search_terms in self.chinese_categories.items():
            news_item = self.fetch_chinese_news(category, search_terms)
            if news_item:
                best_chinese_news = news_item
                break  # Take the first good result
        
        # Fallback if no news found
        if not best_chinese_news:
            best_chinese_news = self._get_mock_chinese_news('AI')
        
        # Format English tweet (single article)
        english_tweet = f"Breaking: {best_global_news['category']} News\n\n"
        english_tweet += f"{best_global_news['title']}\n\n"
        english_tweet += f"Source: {best_global_news['source']}\n\n"
        english_tweet += "#News #Innovation #Technology"
        
        # Ensure it fits
        if len(english_tweet) > 280:
            max_title = 280 - len(f"Breaking: {best_global_news['category']} News\n\n\n\nSource: {best_global_news['source']}\n\n#News #Innovation #Technology")
            english_tweet = f"Breaking: {best_global_news['category']} News\n\n"
            english_tweet += f"{best_global_news['title'][:max_title]}...\n\n"
            english_tweet += f"Source: {best_global_news['source']}\n\n"
            english_tweet += "#News #Innovation #Technology"
        
        # Format Chinese tweet (single article, translated)
        category_cn = translator.translate(best_chinese_news['category'])
        title_cn = translator.translate(best_chinese_news['title'])
        source_cn = translator.translate(best_chinese_news['source'])
        
        chinese_tweet = f"突发: {category_cn}新闻\n\n"
        chinese_tweet += f"{title_cn}\n\n"
        chinese_tweet += f"来源: {source_cn}\n\n"
        chinese_tweet += "#新闻 #创新 #技术"
        
        # Ensure it fits
        if len(chinese_tweet) > 280:
            max_title = 280 - len(f"突发: {category_cn}新闻\n\n\n\n来源: {source_cn}\n\n#新闻 #创新 #技术")
            chinese_tweet = f"突发: {category_cn}新闻\n\n"
            chinese_tweet += f"{title_cn[:max_title]}...\n\n"
            chinese_tweet += f"来源: {source_cn}\n\n"
            chinese_tweet += "#新闻 #创新 #技术"
        
        return english_tweet, chinese_tweet

# Global instance
news_module = WorldNewsModule()
