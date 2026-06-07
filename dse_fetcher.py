import requests
import json
import os

API_KEY = os.environ.get("MANSA_API_KEY", "")

def fetch_dse_prices():
    url = "https://www.mansaapi.com/api/v1/stocks"
    prices = {}

    # Try different auth methods
    headers_options = [
        {"X-API-Key": API_KEY},
        {"Authorization": f"Bearer {API_KEY}"},
        {"Authorization": f"Token {API_KEY}"},
        {"api-key": API_KEY},
    ]

    for headers in headers_options:
        try:
            response = requests.get(
                url,
                headers=headers,
                params={"exchange": "DSE"},
                timeout=15
            )
            print(f"Tried {list(headers.keys())[0]}: Status {response.status_code}")
            print(f"Response: {response.text[:200]}")

            if response.status_code == 200:
                data = response.json()
                for stock in data.get("stocks", []):
                    symbol = stock.get("ticker", "")
                    price = stock.get("price", "")
                    if symbol and price:
                        prices[symbol] = str(price)
                        print(f"✅ {symbol}: {price}")
                break

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
