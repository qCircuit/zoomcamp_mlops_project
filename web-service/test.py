import requests

x = {
    "Timestamp":1325317920,
    "Open": 4,
    "High": 4,
    "Low": 4,
    "Close": 4,
    "Volume_(BTC)": 1,
    "Volume_(Currency)": 2,
    "Weighted_Price": 4
}

url = "http://localhost:9696/predict"
response = requests.post(url, json=x)
print(response.json())
