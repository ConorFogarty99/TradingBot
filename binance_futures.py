import logging
import requests

logger = logging.getLogger()


def get_contracts():
    res_obj = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")

    contracts = []

    for contract in res_obj.json()['symbols']:
        contracts.append(contract['pair'])

    return contracts

print(get_contracts())