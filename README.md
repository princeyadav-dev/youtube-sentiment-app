# SentimentScope — YouTube Comment Sentiment Analyzer

Paste any YouTube video link and get an instant Positive / Neutral / Negative
sentiment breakdown of its comments, along with video tags and stats.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Add your YouTube Data API v3 key to `.env`
3. Run: `python app.py`
4. Open `http://127.0.0.1:5000` in your browser

## Model
LinearSVC classifier trained on TF-IDF (10,000 features) + comment length,
trained on a Kaggle YouTube comments dataset (17,874 rows).