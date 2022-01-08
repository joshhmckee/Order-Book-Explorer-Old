import requests
from datetime import datetime

def collect_data(coin_symbol,depth):
    """
    This function collects the current order book data for coin_symbol using the FTX API.
    :param coin_symbol: The crypto coin symbol.
    :param depth: The depth of order book to collect data for.
    :return: A dictionary of bid-ask prices and size along with the current time.
    """

    url = f"https://ftx.com/api/markets/{coin_symbol}/orderbook?depth={depth}"

    data = requests.get(url)
    data = data.json()

    data['time'] = datetime.now()

    return data
