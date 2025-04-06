from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("perfumes_dataset.csv")

@app.route("/")
def home():
    return "Perfume API is running."

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    selected_feelings = data.get("feelings", [])

    # Filter perfumes where any feeling tag matches
    matches = df[df["Feeling Tags"].str.lower().apply(
        lambda tags: any(feel in tags for feel in selected_feelings)
    )]

    return jsonify(matches.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
