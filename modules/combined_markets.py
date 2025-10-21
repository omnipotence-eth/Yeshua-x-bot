import requests
import yfinance as yf
from utils.logger import setup_logger
from utils.translator import translator
import config

logger = setup_logger(__name__)

class CombinedMarketsModule:
    """Generate combined 24H traditional finance + crypto market updates"""
    
    def __init__(self):
        self.fear_greed_url = "https://api.alternative.me/fng/"
        self.coingecko_url = config.COINGECKO_API_URL
        
        # US market tickers for Texas timezone
        self.us_tickers = {
            '^GSPC': 'S&P 500',
            '^DJI': 'Dow Jones',
            '^IXIC': 'Nasdaq'
        }
        
        # Chinese market tickers for Beijing timezone
        self.chinese_tickers = {
            '000001.SS': 'Shanghai',
            '^HSI': 'Hang Seng',
            'BABA': 'Alibaba'
        }
        
        # Top crypto assets
        self.top_cryptos = ['bitcoin', 'ethereum', 'binancecoin', 'solana']
    
    def get_fear_greed_index(self):
        """Get Fear & Greed Index as market sentiment"""
        try:
            response = requests.get(self.fear_greed_url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            value = int(data['data'][0]['value'])
            classification = data['data'][0]['value_classification']
            
            logger.info(f"Fear & Greed Index: {value} ({classification})")
            return value, classification
        
        except Exception as e:
            logger.error(f"Error fetching Fear & Greed Index: {e}")
            return 50, "Neutral"
    
    def get_us_markets(self):
        """Fetch top US market assets for Texas timezone"""
        try:
            results = {}
            
            for ticker, name in self.us_tickers.items():
                try:
                    stock = yf.Ticker(ticker)
                    hist = stock.history(period='2d')
                    
                    if len(hist) >= 2:
                        today_close = hist['Close'].iloc[-1]
                        yesterday_close = hist['Close'].iloc[-2]
                        change_pct = ((today_close - yesterday_close) / yesterday_close) * 100
                        
                        results[name] = {
                            'price': today_close,
                            'change': change_pct
                        }
                        logger.info(f"[US] {name}: ${today_close:.2f} ({change_pct:+.1f}%)")
                
                except Exception as e:
                    logger.warning(f"Failed to get {name}: {e}")
            
            # Fallback if no data
            if not results:
                logger.warning("No US market data, using fallback")
                results = {
                    'S&P 500': {'price': 5800, 'change': 0.5},
                    'Dow Jones': {'price': 43000, 'change': 0.3},
                    'Nasdaq': {'price': 18500, 'change': 0.8}
                }
            
            return results
        
        except Exception as e:
            logger.error(f"Error fetching US markets: {e}")
            return {
                'S&P 500': {'price': 5800, 'change': 0.5},
                'Dow Jones': {'price': 43000, 'change': 0.3},
                'Nasdaq': {'price': 18500, 'change': 0.8}
            }
    
    def get_chinese_markets(self):
        """Fetch top Chinese market assets for Beijing timezone"""
        try:
            results = {}
            
            for ticker, name in self.chinese_tickers.items():
                try:
                    stock = yf.Ticker(ticker)
                    hist = stock.history(period='2d')
                    
                    if len(hist) >= 2:
                        today_close = hist['Close'].iloc[-1]
                        yesterday_close = hist['Close'].iloc[-2]
                        change_pct = ((today_close - yesterday_close) / yesterday_close) * 100
                        
                        results[name] = {
                            'price': today_close,
                            'change': change_pct
                        }
                        logger.info(f"[CN] {name}: ${today_close:.2f} ({change_pct:+.1f}%)")
                
                except Exception as e:
                    logger.warning(f"Failed to get {name}: {e}")
            
            # Fallback if no data
            if not results:
                logger.warning("No Chinese market data, using fallback")
                results = {
                    'Shanghai': {'price': 3200, 'change': 0.4},
                    'Hang Seng': {'price': 20500, 'change': 0.6},
                    'Alibaba': {'price': 95, 'change': 1.2}
                }
            
            return results
        
        except Exception as e:
            logger.error(f"Error fetching Chinese markets: {e}")
            return {
                'Shanghai': {'price': 3200, 'change': 0.4},
                'Hang Seng': {'price': 20500, 'change': 0.6},
                'Alibaba': {'price': 95, 'change': 1.2}
            }
    
    def get_crypto_markets(self, limit=4):
        """Fetch top cryptocurrencies"""
        try:
            ids = ','.join(self.top_cryptos[:limit])
            url = f"{self.coingecko_url}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'ids': ids,
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            results = {}
            for crypto in data[:limit]:
                symbol = crypto.get('symbol', 'N/A').upper()
                price = crypto.get('current_price', 0)
                change = crypto.get('price_change_percentage_24h', 0)
                
                results[symbol] = {
                    'price': price,
                    'change': change
                }
                logger.info(f"{symbol}: ${price:,.2f} ({change:+.1f}%)")
            
            return results
        
        except Exception as e:
            logger.error(f"Error fetching crypto data: {e}")
            return {
                'BTC': {'price': 68000, 'change': 2.0},
                'ETH': {'price': 3500, 'change': 1.5},
                'BNB': {'price': 590, 'change': 1.0},
                'SOL': {'price': 180, 'change': 0.8}
            }
    
    def format_price(self, price):
        """Format price based on magnitude"""
        if price >= 1000:
            return f"${price:,.0f}"
        elif price >= 1:
            return f"${price:,.2f}"
        else:
            return f"${price:.4f}"
    
    def get_trend_symbol(self, change):
        """Get trend symbol based on change"""
        if change >= 0:
            return "+"
        else:
            return "-"
    
    def format_tweet(self, traditional_markets, crypto_markets, sentiment_value, sentiment_name, language='en', title='Markets Update'):
        """Format combined markets as a tweet"""
        if language == 'en':
            tweet = f"24H {title}\n\n"
            tweet += f"Sentiment: {sentiment_name} ({sentiment_value}/100)\n\n"
            
            # Traditional Markets
            tweet += "US MARKETS:\n"
            for name, data in traditional_markets.items():
                change = data['change']
                trend = self.get_trend_symbol(change)
                tweet += f"{trend} {name}: {change:+.1f}%\n"
            
            # Crypto Markets
            tweet += "\nCRYPTO:\n"
            for symbol, data in crypto_markets.items():
                change = data['change']
                trend = self.get_trend_symbol(change)
                price = self.format_price(data['price'])
                tweet += f"{trend} {symbol}: {price} ({change:+.1f}%)\n"
            
            tweet += "\n#Markets #Finance #Crypto"
        
        else:  # Chinese
            sentiment_cn = translator.translate(sentiment_name)
            tweet = f"24小时{title}\n\n"
            tweet += f"市场情绪: {sentiment_cn} ({sentiment_value}/100)\n\n"
            
            # Chinese Markets
            tweet += "中国市场:\n"
            for name, data in traditional_markets.items():
                change = data['change']
                trend = self.get_trend_symbol(change)
                # Don't translate Chinese market names
                tweet += f"{trend} {name}: {change:+.1f}%\n"
            
            # Crypto Markets
            tweet += "\n加密货币:\n"
            for symbol, data in crypto_markets.items():
                change = data['change']
                trend = self.get_trend_symbol(change)
                price = self.format_price(data['price'])
                tweet += f"{trend} {symbol}: {price} ({change:+.1f}%)\n"
            
            tweet += "\n#市场 #金融 #加密货币"
        
        # Ensure it fits character limit
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
            logger.warning(f"Combined markets tweet truncated to 280 chars")
        
        return tweet
    
    def generate_us_post(self):
        """Generate US market post for Texas timezone (English)"""
        sentiment_value, sentiment_name = self.get_fear_greed_index()
        us_markets = self.get_us_markets()
        crypto_markets = self.get_crypto_markets(limit=4)  # Top 4 cryptos for US
        
        tweet = self.format_tweet(
            us_markets, 
            crypto_markets, 
            sentiment_value, 
            sentiment_name, 
            language='en',
            title='US Markets Update'
        )
        
        return tweet
    
    def generate_chinese_post(self):
        """Generate Chinese market post for Beijing timezone (Chinese)"""
        sentiment_value, sentiment_name = self.get_fear_greed_index()
        chinese_markets = self.get_chinese_markets()
        crypto_markets = self.get_crypto_markets(limit=3)  # Top 3 cryptos for Chinese
        
        tweet = self.format_tweet(
            chinese_markets, 
            crypto_markets, 
            sentiment_value, 
            sentiment_name, 
            language='zh',
            title='中国市场更新'
        )
        
        return tweet
    
    def generate_post(self):
        """Generate both US and Chinese market posts (for backward compatibility)"""
        english = self.generate_us_post()
        chinese = self.generate_chinese_post()
        return english, chinese

# Global instance
combined_markets_module = CombinedMarketsModule()

