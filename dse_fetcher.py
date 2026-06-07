import requests
from bs4 import BeautifulSoup
import json
import re
import os

SUPABASE_URL = "https://ghluqfrinjosvwxnggup.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")

def fetch_stocks():
    url = "https://www.mansamarkets.com/tanzania"
    headers = {"User-Agent": "Mozilla/5.0"}
    stocks = []
    try:
        r = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        for table in soup.find_all("table"):
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) < 3:
                    continue
                link = cols[1].find("a")
                if not link:
                    continue
                href = link.get("href", "")
                ticker = href.split("/")[-1].upper()
                symbol = ticker + " PLC"
                price = re.sub(r'[^\d.]', '', cols[2].text.strip())
                change = re.sub(r'[^\d.\-]', '', cols[3].text.strip()) if len(cols) > 3 else "0"
                volume = re.sub(r'[^\d]', '', cols[4].text.strip()) if len(cols) > 4 else "0"
                if not price:
                    continue
                stocks.append({
                    "symbol": symbol,
                    "price": float(price),
                    "change_percent": float(change) if change else 0,
                    "volume": int(volume) if volume else 0
                })
                print("OK " + symbol + " " + price)
    except Exception as e:
        print("ERR " + str(e))
    return stocks

def push(stocks):
    h = {
        "apikey": SUPABASE_KEY,
        "Auth
