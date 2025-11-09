# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from hashtag_generator import generate_hashtags

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # allow same-origin JS calls; adjust if deploying securely

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/hashtags", methods=["POST"])
def api_hashtags():
    data = request.get_json() or {}
    text = data.get("text", "")
    top_n = data.get("top_n", 8)
    try:
        top_n = int(top_n)
    except Exception:
        top_n = 8
    hashtags = generate_hashtags(text, top_n=top_n)
    return jsonify({"hashtags": hashtags})

if __name__ == "__main__":
    # DEV server
    app.run(host="0.0.0.0", port=5000, debug=True)
