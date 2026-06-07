import requests
from bs4 import BeautifulSoup
import json
import re
import os

SUPABASE_URL = "https://ghluqfrinjosvwxnggup.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")

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
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) >= 3:
                    link = cols[1].find("a")
                    if link:
                        href = link.get("href", "")
                        ticker = href.split("/")[-1].upper()
                        symbol = ticker + " PLC"
                    else:
                        continue
                    price_raw = cols[2].text.strip()
                    price = re.sub(r'[^\d.]', '', price_raw)
                    if symbol and price:
                        prices[symbol] = price
                        print("Fetched " + symbol + ": " + price)
    except Exception as e:
        print("Fetch error: " + str(e))
    return prices

def push_to_supabase(prices):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": "Bearer " + SUPABASE_KEY,
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }
    url = SUPABASE_URL + "/rest/v1/dse_prices"
    success = 0
    for symbol, price in prices.items():
        row = {
            "symbol": symbol,
            "price": float(price),
        }
        try:
            res = requests.post(url, headers=headers, json=row, timeout=10)
            if res.status_code in [200, 201]:
                success += 1
                print("Saved to Supabase: " + symbol)
            else:
                print("Failed " + symbol + ": " + str(res.status_code) + " " + res.text[:100])
        except Exception as e:
            print("Supabase error: " + str(e))
    return success

prices = fetch_dse_prices()

if prices:
    with open("dse_prices.json", "w") as f:
        json.dump(prices, f, indent=2)
    print("Saved " + str(len(prices)) + " prices to JSON")
    pushed = push_to_supabase(prices)
    print("Pushed " + str(pushed) + " prices to Supabase")
else:
    print("No prices found")
