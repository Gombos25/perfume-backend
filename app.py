from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import openai
import os

app = Flask(__name__)
CORS(app)

# Load perfume dataset
csv_path = "perfumes_dataset.csv"
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()

# Set your OpenAI API Key (use environment variable or paste here for testing)
openai.api_key = os.environ.get("")
# openai.api_key = "your-real-key-here"  # ← Uncomment and paste your key here if needed

# Tags to match against
feeling_tags = [
    "fresh", "romantic", "warm", "sweet", "clean",
    "citrus", "woody", "powdery", "musky", "spicy"
]

@app.route("/")
def home():
    return "Perfume AI backend is running."

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    user_input = data.get("input", "").strip()

    if not user_input:
        return jsonify({"error": "No input provided."}), 400

    # Prompt GPT to interpret user's feeling
    prompt = (
        f"The user wrote: '{user_input}'.\n"
        f"Which of these perfume feeling tags best match it: {feeling_tags}?\n"
        f"Return them as a Python list, e.g., ['clean', 'romantic']."
    )

    try:
        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a perfume AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        tag_output = gpt_response["choices"][0]["message"]["content"]
        print("GPT Tags:", tag_output)  # for debugging

        gpt_tags = eval(tag_output)

        # Filter perfumes by tag match
        matches = df[df["Feeling Tags"].fillna("").str.lower().apply(
            lambda tags: any(tag in tags for tag in gpt_tags)
        )]

        return jsonify(matches.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
