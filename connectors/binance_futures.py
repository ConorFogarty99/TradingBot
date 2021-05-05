import logging
import requests

logger = logging.getLogger()


class BinanceFuturesClient:
    # Using a bool to define if we are assessing the testnet or the real site
    def __init__(self, testnet):
        if testnet:
            self.base_url = "https://testnet.binancefuture.com"
        else:
            self.base_url = "https://fapi.binance.com"

            self.prices = dict()

        logger.info("Binance Futures Client successfully initialized")

    # Generic make request method for re-usability
    def make_req(self, method, endpoint, data):
        if method == "GET":
            res = requests.get(self.base_url + endpoint, params=data)
        else:
            raise ValueError()

        # If the response code is 200 we return the json
        # Otherwise we log an error and return nothing
        if res.status_code == 200:
            return res.json()
        else:
            logger.error("Error while making {} request to {}: {} :: Code = {}".format(method,endpoint, res.json(), res.status_code))
            return None

    def get_contracts(self):
        exchange_info = self.make_req("GET", "/fapi/v1/exchangeInfo", None)

        contracts = dict()

        if exchange_info is not None:
            for contract_data in exchange_info['symbols']:
                contracts[contract_data['pair']] = contract_data

        return contracts

    def get_historical_candles(self, symbol, interval):
        data = dict()
        data['symbol'] = symbol
        data['interval'] = interval
        data['limit'] = 1000

        raw_candles = self.make_req("GET", "fapi/v1/klines", data)

        candles = []

        if raw_candles is not None:
            for c in raw_candles:
                candles.append([c[0], float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5])])

        return candles

    def get_bid_ask(self, symbol):
        data = dict()
        data['symbols'] = symbol
        ob_data = self.make_req("GET", "/fapi/v1/bookTicker", data)

        if ob_data is not None:
            if symbol not in self.prices:
                self.prices[symbol] = {'bid': float(ob_data['bidPrice']), 'ask': float(ob_data['askPrice'])}
            else:
                self.prices[symbol]['bid'] = float(ob_data['bidPrice'])
                self.prices[symbol]['ask'] = float(ob_data['askPrice'])

        return self.prices[symbol]