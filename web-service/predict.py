import joblib
import pandas as pd
import time
from datetime import datetime

from flask import Flask, request, jsonify

model_path = "model.joblib"

def preprocess(data):
    # convert unix to datetime
    data["dt"] = data.Timestamp.apply(lambda x: datetime.fromtimestamp(x))

    # generate datetime features
    data["month"] = data.dt.apply(lambda v: v.month)
    data["day"] = data.dt.apply(lambda v: v.day)
    data["weekday"] = data.dt.apply(lambda v: v.weekday())
    data["hour"] = data.dt.apply(lambda v: v.hour)

    # drop non-significant columns
    data = data.drop(["Timestamp", "dt"], axis=1)

    # seet the target
    target = "Close"
    x = data.drop(target, axis=1)
    y = data[target]

    return x, y

def predict(dct):

    with open(model_path, 'rb') as f:
        pipe = joblib.load(f)

    data = pd.DataFrame.from_dict(dct, orient="index").T
    x,y = preprocess(data)
    preds = pipe.predict(x)

    return preds

app = Flask("bitcoin-price-prediction")

@app.route("/predict", methods=["POST"])
def predict_endpoint():
    dct = request.get_json()
    pred = predict(dct)

    result = {
        "predicted_price": float(pred[0])
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)
