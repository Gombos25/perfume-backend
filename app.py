from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

df = pd.read_csv("perfumes_dataset.csv")

@app.route("/")
def home():
    return "Perfume API is running."

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    if not data or "feelings" not in data:
        return jsonify({"error": "No feelings provided"}), 400

    selected_feelings = [f.lower() for f in data["feelings"]]

    matches = df[df["Feeling Tags"].str.lower().apply(
        lambda tags: any(feel in tags for feel in selected_feelings)
    )]

    return jsonify(matches.to_dict(orient="records"))
