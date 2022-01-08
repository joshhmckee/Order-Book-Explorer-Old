import datetime as dt
from dateutil import tz
import pandas as pd

price_data = pd.DataFrame()
spread_data = []

def best_bid_ask(data):
    """
    This function computes the best bid and best ask given the current limit order book.
    :param data: A dictionary of bid-ask prices and size.
    :return: Two integers representing the prices of the best bid and ask respectively.
    """

    best_bid = data['result']['bids'][0][0]
    best_ask = data['result']['asks'][0][0]

    return best_bid, best_ask

def combined_bid_ask(data):
    """
    This function combines the current best bid and ask with the past 60 seconds of bid-ask updates.
    :param data: A dictionary of bid-ask prices and size.
    :return: A Dataframe with the last <100 bid-ask prices.
    """
    global price_data, spread_data

    best_bid, best_ask = best_bid_ask(data)
    nbbo = pd.DataFrame([[best_bid, best_ask]], columns=['BID', 'ASK'])

    index_value = data['time']
    time_zone = tz.tzlocal()
    index_value = index_value.astimezone(time_zone)
    nbbo.set_index(pd.Index([index_value]), inplace=True)

    price_data = price_data.append(nbbo)

    spread = best_ask - best_bid
    spread_data.append(spread)

    # Remove data points that are older than 1 minute.
    if price_data.index[-1] - price_data.index[0] > dt.timedelta(minutes=1):
        price_data = price_data.drop(index=price_data.index[0])
        spread_data.pop(0)

    return price_data, spread_data
