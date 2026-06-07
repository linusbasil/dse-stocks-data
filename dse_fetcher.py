import json
import urllib.request
from datetime import datetime

# All active DSE stocks with correct Yahoo Finance symbols (.TZ suffix)
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

def fetch_all_prices():
    """Fetch all symbols in one batch request to avoid rate limiting."""
    # Build comma‑separated list of Yahoo symbols
    yahoo_symbols = ','.join(SYMBOLS.values())
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbols}"
    
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            result = data.get('chart', {}).get('result', [])
            prices = {}
            for item in result:
                meta = item.get('meta', {})
                symbol = meta.get('symbol')      # e.g., "CRDB.TZ"
                price = meta.get('regularMarketPrice')
                if symbol and price is not None:
                    # Find friendly key (without .TZ)
                    for friendly, yahoo in SYMBOLS.items():
                        if yahoo == symbol:
                            prices[friendly] = round(price, 2)
                            break
            return prices
    except Exception as e:
        print(f"❌ Batch fetch failed: {e}")
        return None

def main():
    prices = fetch_all_prices()
    
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
