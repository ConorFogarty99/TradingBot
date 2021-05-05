import pprint

import requests

def get_contracts():

    res_obj = requests.get("https://www.bitmex.com/api/v1/instrument/active")
    contracts = []

    for contract in res_obj.json():
        contracts.append(contract['symbol'])

    return contracts

print(get_contracts())