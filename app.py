from flask import Flask, request, jsonify
from database import db, init_db
from models import URL
from utils import generate_short_code

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///short_urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.before_request
def create_tables():
    init_db()

@app.route("/")
def home():
    return "Welcome to the URL Shortener!"

@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.json
    long_url = data.get("url")
    if not long_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()
    new_url = URL(long_url=long_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({"short_url": f"http://localhost:5000/{short_code}"})

@app.route("/<short_code>", methods=["GET"])
def redirect_to_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()
    if url_entry:
        return jsonify({"original_url": url_entry.long_url})
    return jsonify({"error": "Short URL not found"}), 404

if __name__ == "__main__":
    app.run(host=True)
