import pandas as pd
import datetime as dt

book_imbalance = pd.Series()

def order_book_depth(data):
    """
    This function computes the order book depth of both the bid and ask and preprocesses series for plotting.
    :param data: A dictionary of bid-ask prices and size.
    :return: Three series, the first and second with cumulative bid/ask quotes & size respectfully and the third
             with order book imbalance - the difference between the size of offers and bids.
    """
    global book_imbalance

    bids = data['result']['bids']
    asks = data['result']['asks']

    bid_prices = []
    ask_prices = []
    bid_quantity = []
    ask_quantity = []

    # To make the line plot end on the x axis.
    bid_prices.append(bids[0][0])
    bid_quantity.append(0)
    ask_prices.append(asks[0][0])
    ask_quantity.append(0)

    # This is used to make sure the price depth on both sides of the mid price is identical.
    # This will make the mid price static in the plot (in the middle).
    mid_price = (bids[0][0] + asks[0][0])/2
    mid_to_smallest_bid = abs(mid_price - bids[-1][0])
    mid_to_largest_ask = abs(mid_price - asks[-1][0])
    min_distance = min(mid_to_smallest_bid, mid_to_largest_ask)

    for level in bids:
        price = level[0]
        if abs(price - mid_price) < min_distance:
            bid_prices.append(level[0])
            bid_quantity.append(level[1])
        else:
            break

    for level in asks:
        price = level[0]
        if abs(price - mid_price) < min_distance:
            ask_prices.append(level[0])
            ask_quantity.append(level[1])
        else:
            break

    bid_prices.append(mid_price-min_distance)
    bid_quantity.append(bid_quantity[-1])

    ask_prices.append(mid_price+min_distance)
    ask_quantity.append(ask_quantity[-1])

    bid_series = pd.Series(bid_quantity, index=bid_prices).cumsum()
    ask_series = pd.Series(ask_quantity, index=ask_prices).cumsum()

    # Order Book Imbalance
    bid_size = bid_series.iloc[-1]
    ask_size = ask_series.iloc[-1]
    imbalance_size = bid_size - ask_size
    book_imbalance = book_imbalance.append(pd.Series(imbalance_size, [data['time']]))

    if book_imbalance.index[-1] - book_imbalance.index[0] > dt.timedelta(minutes=1):
        book_imbalance = book_imbalance.drop(index=book_imbalance.index[0])

    return bid_series, ask_series, book_imbalance
