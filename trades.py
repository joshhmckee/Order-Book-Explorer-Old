import requests
import pandas as pd
from datetime import datetime
from dateutil import tz
import numpy as np

trade_data = pd.DataFrame()

def collect_trades(coin_symbol):
    """
    This function collects the last 20 trades for coin_symbol.
    :param coin_symbol: The crypto coin symbol.
    :return: A dataframe of the last 20 trades.
    """

    url = f'https://ftx.com/api/markets/{coin_symbol + "-PERP"}/trades'

    data = requests.get(url)
    data = data.json()

    trades = data['result']

    # Process trade times to local timezone.
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    for i, trade in enumerate(trades):
        time_utc = trades[i]['time']
        time_utc = datetime.strptime(time_utc, '%Y-%m-%dT%H:%M:%S.%f+00:00')
        time_utc = time_utc.replace(tzinfo=from_zone)
        local_time = time_utc.astimezone(to_zone)

        trades[i]['time'] = local_time

    trades = pd.DataFrame(trades, columns=['id','price','size','side','time'])
    trades.set_index(trades['time'],inplace=True)
    trades.drop(['time'],axis=1,inplace=True)

    return trades

def plot_parameters(tradedata):
    """
    The function creates plot parameters, specifically for the markers on the scatter plot to adjust them based
    on the size and side of the specific trade.
    :param tradedata: A dataframe of all the trades for the crypto in the last 60 seconds.
    :return: A dataframe which includes the color and markersize of a marker corresponding to each trade.
    """

    plot_params = pd.DataFrame()
    plot_params['color'] = np.where(tradedata['side'] == 'buy', 'green', 'red')
    plot_params['dollarvol'] = (tradedata['price'] * tradedata['size']).values

    # If dollar trade size is greater than $50,000, use max marker size else use dollar trade size divided by 100.
    plot_params['markersize'] = np.where((plot_params['dollarvol'] / 100) > 500, 500, plot_params['dollarvol'] / 100)
    plot_params['markersize'] = np.where((plot_params['dollarvol'] / 100) < 10, 10, plot_params['dollarvol'] / 100)

    return plot_params

def combined_trades(coin_symbol,oldest_time):
    """

    :param coin_symbol: The crypto coin symbol.
    :param oldest_time: The oldest bid-ask update that was plotted
    :return: A dataframe of the trades that took place and a dataframe of the plot parameters for those trades.
    """

    global trade_data

    trades = collect_trades(coin_symbol)

    trade_data = trade_data.append(trades)
    trade_data.drop_duplicates(inplace=True)

    trade_data = trade_data.loc[trade_data.index > oldest_time]

    trade_plot_params = plot_parameters(trade_data)

    return trade_data, trade_plot_params
