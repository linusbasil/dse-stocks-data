import requests
from bs4 import BeautifulSoup
import json
import re

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
        soup = BeautifulSoup(response.text, "html.parser")

        tables = soup.find_all("table")
        for table in tables:
            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    # Extract ticker (last uppercase word)
                    raw = cols[0].text.strip()
                    match = re.search(r'([A-Z]{2,6})$', raw)
                    symbol = match.group(1) if match else raw

                    # Clean price
                    price = cols[1].text.strip().replace(",", "").replace("TSh", "").strip()

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
