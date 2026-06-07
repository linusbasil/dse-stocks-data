import requests, json, re, os
from bs4 import BeautifulSoup

URL = 'https://ghluqfrinjosvwxnggup.supabase.co'
KEY = os.environ.get('SUPABASE_SERVICE_KEY', '')

def fetch():
    stocks = []
    try:
        r = requests.get('https://www.mansamarkets.com/tanzania', headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) < 3:
                    continue
                a = cols[1].find('a')
                if not a:
                    continue
                sym = a.get('href','').split('/')[-1].upper() + ' PLC'
                price = re.sub(r'[^\d.]', '', cols[2].text)
                chg = re.sub(r'[^\d.\-]', '', cols[3].text) if len(cols) > 3 else '0'
                vol = re.sub(r'[^\d]', '', cols[4].text) if len(cols) > 4 else '0'
                if price:
                    stocks.append({'symbol':sym,'price':float(price),'change_percent':float(chg or 0),'volume':int(vol or 0)})
                    print('OK '+sym+' '+price)
    except Exception as e:
        print('ERR '+str(e))
    return stocks

def push(stocks):
    h = {'apikey':KEY,'Authorization':'Bearer '+KEY,'Content-Type':'application/json','Prefer':'resolution=merge-duplicates'}
    ok = 0
    for s in stocks:
        try:
            res = requests.post(URL+'/rest/v1/dse_stocks', headers=h, json=s, timeout=10)
            if res.status_code in [200,201]:
                ok += 1
            else:
                print('FAIL '+s['symbol']+' '+res.text[:60])
        except Exception as e:
            print('ERR '+str(e))
    return ok

stocks = fetch()
if stocks:
    with open('dse_prices.json','w') as f:
        json.dump({s['symbol']:str(s['price']) for s in stocks},f,indent=2)
    print('JSON '+str(len(stocks)))
    print('Supabase '+str(push(stocks)))
else:
    print('No data')
