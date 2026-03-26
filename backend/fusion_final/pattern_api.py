from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route("/pattern-data")
def pattern_data():

    df = pd.read_csv("../structure/pattern.csv")

    pattern_counts = df["predicted_structure"].value_counts().head(8)

    data = {
        "labels": pattern_counts.index.tolist(),
        "values": pattern_counts.values.tolist()
    }

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)