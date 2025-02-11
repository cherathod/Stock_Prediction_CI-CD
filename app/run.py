from app import create_app, db
from flask import Flask, render_template, jsonify
import feedparser # type: ignore
from app.routes.prediction_routes import prediction_bp  # Ensure correct import path

app = create_app()

# Function to get live notifications from MoneyControl RSS Feed
def get_moneycontrol_news():
    rss_url = "https://www.moneycontrol.com/rss/marketnews.xml"  # Change as needed
    feed = feedparser.parse(rss_url)
    news_list = [{"title": entry.title, "link": entry.link} for entry in feed.entries[:5]]  # Get top 5 news
    return news_list

# Check if blueprint is already registered to prevent duplicate registration
if "prediction_routes" not in [bp.name for bp in app.blueprints.values()]:
    app.register_blueprint(prediction_bp, url_prefix="/stock_prediction")

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Notifications Route
@app.route('/get_notifications')
def get_notifications():
    return jsonify(get_moneycontrol_news())

# Initialize DB within the application context
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)