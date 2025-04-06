from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load CSV and clean column names just in case
df = pd.read_csv("perfumes_dataset.csv")
df.columns = df.columns.str.strip()  # remove any trailing spaces from headers

@app.route("/")
def home():
    return "Perfume API is running."

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    if not data or "feelings" not in data:
        return jsonify({"error": "No feelings provided"}), 400

    selected_feelings = [f.lower() for f in data["feelings"]]

    # Fix: handle blank or missing values in 'Feeling Tags' safely
    matches = df[df["Feeling Tags"].fillna("").str.lower().apply(
        lambda tags: any(feel in tags for feel in selected_feelings)
    )]

    return jsonify(matches.to_dict(orient="records"))
