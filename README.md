# python-url-shortener
# ✅ Step-by-Step Guide to Implement a Flask URL Shortener in VS Code with SQLite

This guide will show you how to set up, code, run, and test a Flask-based URL Shortener using VS Code with SQLite.

## 🔹 1️⃣ Install Prerequisites

Before starting, make sure you have:

- **Python 3.x** installed (`python --version`)
- **VS Code** installed with the following extensions:
  - Python Extension
  - Docker Extension (if using Docker)
- **pip** installed (`pip --version`)

---

## 🔹 2️⃣ Set Up the Project in VS Code

### 📌 Create a New Project Folder

1. Open **VS Code**
2. Click **File → Open Folder**
3. Select or create a folder: `url-shortener`
4. Open a **Terminal** in VS Code (`Ctrl + ~`)

### 📌 Create Required Files

Inside your `url-shortener` folder, create these files:

```
📂 url-shortener
 ├── app.py
 ├── database.py
 ├── models.py
 ├── utils.py
 ├── requirements.txt
 ├── .gitignore
 ├── README.md
```

---

## 🔹 3️⃣ Install Required Packages

Run this command in the VS Code Terminal:

```sh
pip install flask flask-sqlalchemy flask-cors
```

---

## 🔹 4️⃣ Write the Code

### 📜 `app.py` – Main Flask API

```python
from flask import Flask, request, jsonify
from database import db, init_db
from models import URL
from utils import generate_short_code

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///short_urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    init_db()

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
    app.run(debug=True)
```

### 📜 `database.py` – Database Setup

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    from app import app
    with app.app_context():
        db.create_all()
```

### 📜 `models.py` – Database Model

```python
from database import db

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
```

### 📜 `utils.py` – Short URL Generator

```python
import random
import string

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))
```

### 📜 `requirements.txt` – Dependencies

```
flask
flask-sqlalchemy
flask-cors
```

---

## 🔹 5️⃣ Running the Project

📌 Open **VS Code Terminal** (`Ctrl + ~`)

Run the following command:

```sh
python app.py
```

---

## 🔹 6️⃣ Test the API (Using Postman/cURL)

### **Shorten a URL**

```sh
curl -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d '{"url": "https://example.com"}'
```

### **Retrieve Original URL**

```sh
curl -X GET http://localhost:5000/abc123
```

---

## 🔹 7️⃣ (Optional) Running in Docker

### 📜 `Dockerfile`

```dockerfile
FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

### 📌 Build & Run the Container

```sh
docker build -t url-shortener .
docker run -p 5000:5000 url-shortener
```

---


