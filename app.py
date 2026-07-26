import os
from flask import Flask, render_template, request
import joblib
from scipy.sparse import hstack
from dotenv import load_dotenv
from preprocess import clean_text
from youtube_api import extract_video_id, fetch_video_details, fetch_comments

load_dotenv()

app = Flask(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

model = joblib.load("models/sentiment_model.pkl")
tfidf = joblib.load("models/tfidf.pkl")
scaler = joblib.load("models/scaler.pkl")


def predict_comments(comments):
    cleaned = [clean_text(c) for c in comments]
    lengths = [[len(c)] for c in cleaned]

    tfidf_features = tfidf.transform(cleaned)
    scaled_lengths = scaler.transform(lengths)

    final_features = hstack([tfidf_features, scaled_lengths])
    return model.predict(final_features)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    url = request.form.get("youtube_url", "").strip()
    video_id = extract_video_id(url)

    if not video_id:
        return render_template("index.html", error="Invalid YouTube URL. Please check and try again.")

    video_details = fetch_video_details(video_id, YOUTUBE_API_KEY)
    if not video_details:
        return render_template("index.html", error="Could not fetch video details. Check the URL or API key.")

    comments = fetch_comments(video_id, YOUTUBE_API_KEY, max_comments=500)
    if not comments:
        return render_template("index.html", error="No comments found, or comments are disabled on this video.")

    predictions = predict_comments(comments)

    total = len(predictions)
    positive = sum(1 for p in predictions if p == 2)
    neutral = sum(1 for p in predictions if p == 1)
    negative = sum(1 for p in predictions if p == 0)

    result = {
        "total": total,
        "positive_pct": round((positive / total) * 100, 2),
        "neutral_pct": round((neutral / total) * 100, 2),
        "negative_pct": round((negative / total) * 100, 2),
    }

    return render_template("result.html", result=result, video=video_details)


if __name__ == "__main__":
    app.run(debug=True)