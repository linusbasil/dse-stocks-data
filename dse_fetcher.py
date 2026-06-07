import requests
import urllib3
from bs4 import BeautifulSoup
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_dse_prices():
    url = "https://www.dse.co.tz/market-statistics"
    headers = {"User-Agent": "Mozilla/5.0"}
    prices = {}

    try:
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        
        table = soup.find("table")
        if table:
            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    symbol = cols[0].text.strip()
                    price = cols[1].text.strip()
                    if symbol and price:
                        prices[symbol] = price
    except Exception as e:
        print(f"Error fetching DSE: {e}")

    return prices

prices = fetch_dse_prices()

if prices:
    with open("dse_prices.json", "w") as f:
        json.dump(prices, f, indent=2)
    print(f"✅ Saved {len(prices)} prices")
else:
    print("❌ No prices found")
