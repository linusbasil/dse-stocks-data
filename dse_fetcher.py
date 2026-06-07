import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_dse_prices():
    url = "https://www.mansamarkets.com/tanzania"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    prices = {}

    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f"Status: {response.status_code}")
        soup = BeautifulSoup(response.text, "html.parser")

        # Print page snippet for debugging
        print(f"Page preview: {response.text[500:1000]}")

        # Try all tables
        tables = soup.find_all("table")
        print(f"Tables found: {len(tables)}")

        for table in tables:
            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    symbol = cols[0].text.strip()
                    price = cols[1].text.strip()
                    if symbol and price:
                        prices[symbol] = price
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
