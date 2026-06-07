import json
import urllib.request
import time
from datetime import datetime

# Correct Yahoo Finance symbols for DSE stocks (using .TZ suffix where available)
# If a symbol is not found on Yahoo, it will be skipped – you can add/remove as needed.
SYMBOLS = {
    "CRDB": "CRDB.TZ",
    "NMB": "NMB.TZ",
    "VODA": "VODA.TZ",
    "TBL": "TBL.TZ",
    "TPCC": "TPCC.TZ",
    "DCB": "DCB.TZ",
    "DSE": "DSE.TZ",
    "KCB": "KCB.TZ",
    "TOL": "TOL.TZ",
    "TCC": "TCC.TZ",
    "SWISS": "SWISS.TZ",
    "NICO": "NICO.TZ",
    "MKCB": "MKCB.TZ",
    "EABL": "EABL.TZ",
    "JHL": "JHL.TZ",
    "MCC": "MCC.TZ",
    "NMG": "NMG.TZ",
    "NICOL": "NICOL.TZ",
    "PCC": "PCC.TZ",
    "TCCIA": "TCCIA.TZ",
    "TICL": "TICL.TZ",
    "TPC": "TPC.TZ",
    "TCCL": "TCCL.TZ"
}

def fetch_yahoo_price(yahoo_symbol, retries=2):
    """Fetch current price from Yahoo Finance with retry and delay."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}"
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                result = data.get('chart', {}).get('result')
                if result and len(result) > 0:
                    meta = result[0].get('meta')
                    if meta:
                        price = meta.get('regularMarketPrice')
                        if price is not None:
                            return round(price, 2)
        except Exception as e:
            if attempt == retries - 1:
                print(f"⚠️ Failed {yahoo_symbol}: {e}")
            else:
                time.sleep(2)  # wait before retry
    return None

def main():
    prices = {}
    for friendly, yahoo in SYMBOLS.items():
        print(f"Fetching {friendly} ({yahoo})...")
        price = fetch_yahoo_price(yahoo)
        if price is not None:
            prices[friendly] = price
        else:
            print(f"⚠️ Could not fetch {friendly} – skipping")
        time.sleep(1.5)  # delay between different stocks to avoid rate limiting

    if not prices:
        print("❌ No prices fetched – keeping existing dse_prices.json")
        return

    data = {
        "date": datetime.now().date().isoformat(),
        "prices": prices
    }

    with open("dse_prices.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ dse_prices.json updated with {len(prices)} live prices")
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
