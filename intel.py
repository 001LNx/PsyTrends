import os
from dotenv import load_dotenv
import tweepy
import praw
import requests
import pandas as pd
from datetime import datetime
import time

load_dotenv()

# Simple sentiment analyzer (no torch required)
def simple_sentiment_score(text):
    positive_words = ['good', 'great', 'excellent', 'innovation', 'growth', 'success', 'trending', 'popular']
    negative_words = ['bad', 'crisis', 'risk', 'decline', 'loss', 'problem', 'disaster', 'threat']
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count + neg_count == 0:
        return 0.5  # neutral
    return pos_count / (pos_count + neg_count)

class TwitterTrendsFetcher:
    def __init__(self):
        self.api_key = os.getenv('TWITTER_API_KEY', 'demo')
        self.api_secret = os.getenv('TWITTER_API_SECRET', 'demo')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN', 'demo')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', 'demo')
        self.client = None
        # Check if credentials are configured (not demo/placeholder)
        has_real_credentials = (
            self.api_key and not any(x in self.api_key for x in ['demo', 'your_']) and
            self.api_secret and not any(x in self.api_secret for x in ['demo', 'your_'])
        )
        if has_real_credentials:
            try:
                self.client = tweepy.Client(
                    consumer_key=self.api_key,
                    consumer_secret=self.api_secret,
                    access_token=self.access_token,
                    access_token_secret=self.access_token_secret
                )
            except Exception as e:
                print(f"Twitter API initialization failed: {e}")

    def get_trends(self, woeid):
        if not self.client:
            # Return mock data for demo
            import random
            base_volume = 50000 + random.randint(0, 100000)
            return [
                {'keyword': '#technology', 'volume': base_volume},
                {'keyword': '#innovation', 'volume': base_volume - 20000},
                {'keyword': '#ai', 'volume': base_volume - 40000},
                {'keyword': '#politics', 'volume': base_volume - 30000},
                {'keyword': '#climate', 'volume': base_volume - 50000}
            ]
        try:
            # Using v1.1 API if available
            trends = self.client.get_place_trends(id=woeid)
            if trends.data:
                return [{'keyword': trend['name'], 'volume': trend.get('tweet_volume', 0)} for trend in trends.data[0]['trends']]
            return []
        except Exception as e:
            print(f"Error fetching Twitter trends: {e}")
            # Fallback to mock data
            return self.get_trends(woeid) if self.client else []

class RedditTrendsFetcher:
    def __init__(self):
        self.client_id = os.getenv('REDDIT_CLIENT_ID', 'demo')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET', 'demo')
        self.user_agent = os.getenv('REDDIT_USER_AGENT', 'demo')
        self.reddit = None
        if not any(v == 'demo' or 'your_' in v for v in [self.client_id, self.client_secret, self.user_agent]):
            try:
                self.reddit = praw.Reddit(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    user_agent=self.user_agent
                )
            except Exception as e:
                print(f"Reddit API initialization failed: {e}")

    def get_trends(self, subreddit='all', limit=100):
        if not self.reddit:
            # Return mock data for demo
            return [
                {'keyword': 'technology', 'volume': 85000},
                {'keyword': 'science', 'volume': 75000},
                {'keyword': 'politics', 'volume': 65000},
                {'keyword': 'business', 'volume': 55000},
                {'keyword': 'environment', 'volume': 45000}
            ]
        try:
            hot_posts = list(self.reddit.subreddit(subreddit).hot(limit=limit))
            keywords = {}
            for post in hot_posts:
                title_words = post.title.lower().split()
                for word in title_words:
                    if len(word) > 3:  # simple filter
                        keywords[word] = keywords.get(word, 0) + 1
            return [{'keyword': k, 'volume': v} for k, v in keywords.items()]
        except Exception as e:
            print(f"Error fetching Reddit trends: {e}")
            return []

class TikTokTrendsFetcher:
    def __init__(self):
        # TikTok doesn't have official public API for trends
        # Using unofficial endpoint or placeholder
        pass

    def get_trends(self):
        # Placeholder: return empty or mock data
        print("TikTok trends fetcher not implemented (no public API)")
        return []

class FacebookTrendsFetcher:
    def __init__(self):
        self.app_id = os.getenv('FACEBOOK_APP_ID')
        self.app_secret = os.getenv('FACEBOOK_APP_SECRET')
        # Facebook Graph API for trending topics
        pass

    def get_trends(self):
        # Placeholder: Facebook trending topics require access token and specific endpoints
        print("Facebook trends fetcher not implemented")
        return []

class DataCollector:
    def __init__(self):
        self.twitter = TwitterTrendsFetcher()
        self.reddit = RedditTrendsFetcher()
        self.tiktok = TikTokTrendsFetcher()
        self.facebook = FacebookTrendsFetcher()
        self.countries = {
            'USA': 23424977,
            'Canada': 23424775,
            'UK': 23424975,
            'France': 23424819,
            'Germany': 23424829,
            'Italy': 23424853,
            'Japan': 23424856,
            'China': 23424781,
            'Russia': 23424936,
            'Mexico': 23424900
        }

    def collect_data(self):
        data = []
        timestamp = datetime.now()
        for country, woeid in self.countries.items():
            # Twitter
            trends = self.twitter.get_trends(woeid)
            for trend in trends:
                data.append({
                    'timestamp': timestamp,
                    'country': country,
                    'platform': 'Twitter',
                    'keyword': trend['keyword'],
                    'volume': trend['volume']
                })
            # Reddit (global, but assign to country? For now, global)
            if country == 'USA':  # Only once
                trends = self.reddit.get_trends()
                for trend in trends:
                    data.append({
                        'timestamp': timestamp,
                        'country': 'Global',
                        'platform': 'Reddit',
                        'keyword': trend['keyword'],
                        'volume': trend['volume']
                    })
            # TikTok and Facebook placeholders
        if not data:
            # Return empty DataFrame with correct structure
            data = [{
                'timestamp': timestamp,
                'country': 'N/A',
                'platform': 'Demo',
                'keyword': 'sample',
                'volume': 0
            }]
        df = pd.DataFrame(data)
        return df
    def process_data(self, df):
        # Clean keywords: lowercase, remove special chars
        df['keyword'] = df['keyword'].str.lower().str.replace(r'[^\w\s]', '', regex=True)
        # Remove duplicates within same timestamp/country/platform
        df = df.drop_duplicates(subset=['timestamp', 'country', 'platform', 'keyword'])
        # Add sentiment score
        df['sentiment_score'] = df['keyword'].apply(lambda x: simple_sentiment_score(x))
        # Aggregate by keyword, country, date
        df['date'] = df['timestamp'].dt.date
        aggregated = df.groupby(['date', 'country', 'keyword']).agg({
            'volume': 'sum',
            'sentiment_score': 'mean'
        }).reset_index()
        return aggregated

    def save_data(self, df, filename='trends_data.csv'):
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def generate_synthetic_history(self, num_days=14):
        """Generate synthetic historical data for forecasting demo"""
        import random
        data = []
        base_date = datetime.now() - pd.Timedelta(days=num_days)
        
        # Use fewer keywords but with more consistent data
        sample_keywords = [
            'technology', 'innovation', 'ai', 'politics', 'climate'
        ]
        
        for day in range(num_days):
            current_date = base_date + pd.Timedelta(days=day)
            # Generate data for ALL countries to ensure each has history
            for country in self.countries.keys():
                for keyword in sample_keywords:
                    # Add some trend: make each day slightly different
                    base_volume = random.randint(50000, 150000)
                    trend = (day * 1000)  # increasing trend over time
                    noise = random.randint(-10000, 10000)
                    volume = max(1000, base_volume + trend + noise)
                    
                    data.append({
                        'date': current_date.date(),
                        'country': country,
                        'keyword': keyword,
                        'volume': volume,
                        'sentiment_score': simple_sentiment_score(keyword)
                    })
        return pd.DataFrame(data)

    def collect_and_process(self, include_history=True):
        df = self.collect_data()
        
        # Process current data
        current_df = self.process_data(df)
        
        if include_history:
            # Add synthetic historical data for better forecasting
            history_df = self.generate_synthetic_history(num_days=7)
            # Remove demo row from current
            current_df = current_df[current_df['keyword'] != 'sample']
            # Combine historical and current
            df = pd.concat([history_df, current_df], ignore_index=True)
        else:
            df = current_df
        
        self.save_data(df)
        return df

if __name__ == "__main__":
    collector = DataCollector()
    df = collector.collect_and_process()
    print(df.head())