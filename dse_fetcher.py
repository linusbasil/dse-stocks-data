import json
import urllib.request
from datetime import datetime

# All active DSE stocks (friendly name -> Yahoo Finance symbol with .TZ suffix)
SYMBOLS = {
    "CRDB": "CRDB.TZ",
    "NMB":  "NMB.TZ",
    "VODA": "VODA.TZ",
    "TBL":  "TBL.TZ",
    "TPCC": "TPCC.TZ",
    "DCB":  "DCB.TZ",
    "DSE":  "DSE.TZ",
    "KCB":  "KCB.TZ",
    "TOL":  "TOL.TZ",
    "TCC":  "TCC.TZ",
    "SWISS":"SWISS.TZ",
    "NICO": "NICO.TZ",
    "MKCB": "MKCB.TZ",
    "EABL": "EABL.TZ",
    "JHL":  "JHL.TZ",
    "MCC":  "MCC.TZ",
    "NMG":  "NMG.TZ",
    "NICOL":"NICOL.TZ",
    "PCC":  "PCC.TZ",
    "TCCIA":"TCCIA.TZ",
    "TICL": "TICL.TZ",
    "TPC":  "TPC.TZ",
    "TCCL": "TCCL.TZ",
    "SWIS": "SWIS.TZ",        # alternative spelling
    "VERTEX": "VERTEX.TZ",
    "USL": "USL.TZ",
    "TTP": "TTP.TZ",
    "NMG": "NMG.TZ",
    "MKCB": "MKCB.TZ",
    "EABL": "EABL.TZ"
}

def fetch_yahoo_price(yahoo_symbol):
    """Fetch current price from Yahoo Finance."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            result = data.get('chart', {}).get('result')
            if result and len(result) > 0:
                meta = result[0].get('meta')
                if meta:
                    return meta.get('regularMarketPrice')
    except Exception as e:
        print(f"⚠️ Error fetching {yahoo_symbol}: {e}")
    return None

def main():
    prices = {}
    for friendly, yahoo in SYMBOLS.items():
        price = fetch_yahoo_price(yahoo)
        if price is not None:
            prices[friendly] = round(price, 2)
        else:
            print(f"⚠️ Could not fetch {friendly} ({yahoo}), skipping")
    
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
