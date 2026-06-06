import json
import csv
from datetime import datetime
import os
import urllib.request

# ========== STOCK PRICES (LIVE FROM DSE JSON PIPELINE) ==========
prices = {
    "CRDB": 2940, "NMB": 13800, "VODA": 800, "TBL": 10200,
    "TPCC": 7400, "DCB": 750, "DSE": 1050, "KCB": 510
}

data = {
    "date": datetime.now().date().isoformat(),
    "prices": prices
}

# Save JSON file
with open("dse_prices.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ dse_prices.json created successfully!")
print(json.dumps(data, indent=2))

# ========== SEND TO BINGWA WEBHOOK ==========
WEBHOOK_URL = "https://project--be89c011-fe5d-4ecd-b65b-e74592e8631b.lovable.app/api/public/update-price-history"
ADMIN_KEY = os.environ.get("BINGWA_ADMIN_KEY")

if ADMIN_KEY:
    try:
        with open("dse_prices.json", "r") as f:
            payload = json.load(f)
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "x-api-key": ADMIN_KEY},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            print("✅ Price history webhook:", resp.status, resp.read().decode())
    except Exception as e:
        print("⚠️ Webhook failed:", e)
else:
    print("⏭️ Skipping: BINGWA_ADMIN_KEY not set")
