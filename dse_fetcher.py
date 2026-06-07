import requests
import json
import os

API_KEY = os.environ.get("MANSA_API_KEY", "")

def fetch_dse_prices():
    url = "https://www.mansaapi.com/api/v1/stocks"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"exchange": "DSE"}
    prices = {}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        print(f"Status code: {response.status_code}")
        data = response.json()

        for stock in data.get("stocks", []):
            symbol = stock.get("ticker", "")
            price = stock.get("price", "")
            if symbol and price:
                prices[symbol] = str(price)
                print(f"✅ {symbol}: {price}")

    except Exception as e:
        print(f"❌ Error: {e}")

    return prices

prices = fetch_dse_prices()

if prices:
    with open("dse_prices.json", "w") as f:
        json.dump(prices, f, indent=2)
    print(f"\n✅ Saved {len(prices)} prices")
else:
    print("❌ No prices found")
