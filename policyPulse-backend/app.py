from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # 👈 Important for allowing cross-origin requests

# Load your dataset
df = pd.read_csv("all_states_schemes_cleaned.csv")

@app.route("/recommend", methods=["GET"])
def recommend():
    state = request.args.get("state", "")
    keyword = request.args.get("keyword", "")
    
    filtered = df.copy()
    
    if state:
        filtered = filtered[filtered["State"].str.contains(state, case=False, na=False)]
    
    if keyword:
        keyword = keyword.lower()
        filtered = filtered[
            filtered["Scheme Name"].str.lower().str.contains(keyword) |
            filtered["Eligibility"].str.lower().str.contains(keyword) |
            filtered["Benefit"].str.lower().str.contains(keyword)
        ]

    # Replace NaN with empty string before converting to JSON
    cleaned = filtered.fillna("")
    return jsonify(cleaned.head(10).to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)
