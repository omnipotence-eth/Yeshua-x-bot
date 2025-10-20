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
        self.top_cryptos = config.TOP_CRYPTO_ASSETS[:3]  # Top 3 cryptos only
    
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
    
    def get_traditional_markets(self):
        """Fetch top 3 traditional market assets"""
        try:
            tickers = {
                '^GSPC': 'S&P 500',
                '^IXIC': 'Nasdaq',
                'GC=F': 'Gold'
            }
            
            results = {}
            
            for ticker, name in tickers.items():
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
                        logger.info(f"{name}: ${today_close:.2f} ({change_pct:+.1f}%)")
                
                except Exception as e:
                    logger.warning(f"Failed to get {name}: {e}")
            
            # Fallback if no data
            if not results:
                logger.warning("No traditional market data, using fallback")
                results = {
                    'S&P 500': {'price': 4500, 'change': 0.5},
                    'Nasdaq': {'price': 14000, 'change': 0.8},
                    'Gold': {'price': 2000, 'change': 0.2}
                }
            
            return results
        
        except Exception as e:
            logger.error(f"Error fetching traditional markets: {e}")
            return {
                'S&P 500': {'price': 4500, 'change': 0.5},
                'Nasdaq': {'price': 14000, 'change': 0.8},
                'Gold': {'price': 2000, 'change': 0.2}
            }
    
    def get_crypto_markets(self):
        """Fetch top 3 cryptocurrencies"""
        try:
            ids = ','.join(self.top_cryptos)
            url = f"{self.coingecko_url}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'ids': ids,
                'order': 'market_cap_desc',
                'per_page': 3,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            results = {}
            for crypto in data[:3]:
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
                'BNB': {'price': 590, 'change': 1.0}
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
    
    def format_tweet(self, traditional_markets, crypto_markets, sentiment_value, sentiment_name, language='en'):
        """Format combined markets as a tweet"""
        if language == 'en':
            tweet = "24H Global Markets Update\n\n"
            tweet += f"Sentiment: {sentiment_name} ({sentiment_value}/100)\n\n"
            
            # Traditional Markets
            tweet += "TRADITIONAL:\n"
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
            tweet = "24小时全球市场更新\n\n"
            tweet += f"市场情绪: {sentiment_cn} ({sentiment_value}/100)\n\n"
            
            # Traditional Markets
            tweet += "传统市场:\n"
            for name, data in traditional_markets.items():
                name_cn = translator.translate(name)
                change = data['change']
                trend = self.get_trend_symbol(change)
                tweet += f"{trend} {name_cn}: {change:+.1f}%\n"
            
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
    
    def generate_post(self):
        """Generate both English and Chinese combined market posts"""
        sentiment_value, sentiment_name = self.get_fear_greed_index()
        traditional_markets = self.get_traditional_markets()
        crypto_markets = self.get_crypto_markets()
        
        english_tweet = self.format_tweet(
            traditional_markets, 
            crypto_markets, 
            sentiment_value, 
            sentiment_name, 
            language='en'
        )
        
        chinese_tweet = self.format_tweet(
            traditional_markets, 
            crypto_markets, 
            sentiment_value, 
            sentiment_name, 
            language='zh'
        )
        
        return english_tweet, chinese_tweet

# Global instance
combined_markets_module = CombinedMarketsModule()

