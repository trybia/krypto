import falcon
import json
import requests

def pobierz():
    urls = {
        'BTCPLN_Bitbay': 'https://bitbay.net/API/Public/BTCPLN/ticker.json',
        'LTCPLN_Bitbay': 'https://bitbay.net/API/Public/LTCPLN/ticker.json',
        'ETHPLN_Bitbay': 'https://bitbay.net/API/Public/ETHPLN/ticker.json',
        'BCCPLN_Bitbay': 'https://bitbay.net/API/Public/BCCPLN/ticker.json',
        'BTCPLN_BitMarket': 'https://www.bitmarket.pl/json/BTCPLN/ticker.json',
        'LTCPLN_BitMarket': 'https://www.bitmarket.pl/json/LTCPLN/ticker.json',
        'BCCPLN_BitMarket': 'https://www.bitmarket.pl/json/BCCPLN/ticker.json',
        'BTC-EUR_Gdax': 'https://api.gdax.com/products/BTC-EUR/ticker',
        'LTC-EUR_Gdax': 'https://api.gdax.com/products/LTC-EUR/ticker',
        'ETH-EUR_Gdax': 'https://api.gdax.com/products/ETH-EUR/ticker',
        'XXBTZEUR_Kraken': 'https://api.kraken.com/0/public/Ticker?pair=XBTEUR',
        'XLTCZEUR_Kraken': 'https://api.kraken.com/0/public/Ticker?pair=LTCEUR',
        'XETHZEUR_Kraken': 'https://api.kraken.com/0/public/Ticker?pair=ETHEUR',
        'BCHEUR_Kraken': 'https://api.kraken.com/0/public/Ticker?pair=BCHEUR',
        'BCH-USD_Gdax': 'https://api.gdax.com/products/BCH-USD/ticker',
        'BTC-USD_Gdax': 'https://api.gdax.com/products/BTC-USD/ticker',
        'ETH-USD_Gdax': 'https://api.gdax.com/products/ETH-USD/ticker',
        'LTC-USD_Gdax': 'https://api.gdax.com/products/LTC-USD/ticker',
        'DASHPLN_Bitbay': 'https://bitbay.net/API/Public/DASHPLN/ticker.json',
        

    }

    kursy={}

    for kurs in urls.keys():
        r = requests.get(url=urls[kurs])

        # print(kurs, r.text)
        result = json.loads(r.text)
        # kursy[kurs]=int(result['last'])
        if "Bitbay" in kurs or "BitMarket" in kurs:
            wartosc = result['last']
        elif "Gdax" in kurs:
            wartosc = result['price']
        elif "Kraken" in kurs:
            # print(result)
            wartosc = result['result'][kurs.split("_")[0]]['c'][0]
        kursy[kurs] = wartosc


    return kursy


class KursyGen(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.body = parsuj(pobierz())

def parsuj(kursy):
    html = '<table>'

    for kurs in kursy:
        html += '<tr><td>' +kurs+ '</td><td>' +str(kursy[kurs]) + '</td></tr>'

    html += '</table>'

    return html



# falcon.API instances are callable WSGI apps
api = application = falcon.API()

# Resources are represented by long-lived class instances
handler = KursyGen()

# things will handle all requests to the '/things' URL path
api.add_route('/', handler)