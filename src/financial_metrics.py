import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import tweepy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from transformers import pipeline, DistilBertTokenizer, DistilBertForSequenceClassification
import torch

# Download NLTK data (run once)
nltk.download('punkt')
nltk.download('stopwords')

class FinancialMetrics:
    def __init__(self, symbol, start_date=None, end_date=None):
        self.symbol = symbol.upper()
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)  # Default to 1 year
        if end_date is None:
            end_date = datetime.now()
        self.df = self.fetch_data(start_date, end_date)

    def fetch_data(self, start_date, end_date):
        """Fetch historical data using yfinance."""
        ticker = yf.Ticker(self.symbol)
        df = ticker.history(start=start_date, end=end_date)
        return df

    # ... (Keep existing technical, fundamental, and risk metrics as they are)

    def market_sentiment(self, num_tweets=100, time_window="1h"):
        """
        Perform sophisticated sentiment analysis using Twitter/X data and BERT.
        Returns a sentiment score (-1 to 1, where -1 is very negative, 0 is neutral, 1 is very positive).
        """
        # Initialize Twitter API (replace with your credentials)
        try:
            auth = tweepy.OAuthHandler("YOUR_CONSUMER_KEY", "YOUR_CONSUMER_SECRET")
            auth.set_access_token("YOUR_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN_SECRET")
            api = tweepy.API(auth, wait_on_rate_limit=True)
        except:
            print("Twitter API authentication failed. Falling back to snscrape or skipping.")
            return None

        # Preprocess text function
        def preprocess_text(text):
            # Convert to lowercase
            text = text.lower()
            # Remove URLs, mentions, hashtags, and special characters
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
            text = re.sub(r'@\w+|\#', '', text)
            # Remove punctuation and numbers
            text = re.sub(r'[^\w\s]', '', text)
            # Tokenize and remove stopwords
            stop_words = set(stopwords.words('english'))
            tokens = word_tokenize(text)
            tokens = [token for token in tokens if token not in stop_words]
            return ' '.join(tokens)

        # Load pre-trained DistilBERT model and tokenizer for sentiment analysis
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        tokenizer = DistilBertTokenizer.from_pretrained(model_name)
        model = DistilBertForSequenceClassification.from_pretrained(model_name)
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model=model,
            tokenizer=tokenizer,
            device=0 if torch.cuda.is_available() else -1  # Use GPU if available
        )

        # Fetch recent tweets about the symbol
        try:
            tweets = tweepy.Cursor(api.search_tweets,
                                 q=f"${self.symbol} -filter:retweets",
                                 lang="en",
                                 tweet_mode="extended").items(num_tweets)
            tweet_texts = [tweet.full_text for tweet in tweets]
        except Exception as e:
            print(f"Error fetching tweets: {e}")
            return None

        # Preprocess tweets
        processed_texts = [preprocess_text(text) for text in tweet_texts if text]

        # Analyze sentiment for each tweet
        sentiments = []
        for text in processed_texts:
            if len(text.split()) > 0:  # Ensure text is not empty
                result = sentiment_analyzer(text)[0]
                label = result['label']
                score = result['score']
                # Map labels to numeric scores: 'POSITIVE' -> 1, 'NEGATIVE' -> -1
                sentiment_score = 1.0 if label == 'POSITIVE' else -1.0
                sentiments.append(sentiment_score * score)

        if not sentiments:
            return 0.0  # Neutral if no valid sentiments

        # Aggregate sentiment (average score over time window)
        avg_sentiment = np.mean(sentiments)
        return avg_sentiment

    # ... (Keep other methods as they are)

# Example usage
if __name__ == "__main__":
    metrics = FinancialMetrics("AAPL")
    sentiment = metrics.market_sentiment(num_tweets=50, time_window="1h")
    print(f"Market Sentiment for {metrics.symbol}: {sentiment:.2f}")