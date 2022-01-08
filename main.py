import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

import book_depth as bd
import bid_ask_spread as bas
import data_collection as dc
import trades as t

# Get coin symbol and order book depth
coin_symbol = input('Enter a coin symbol: ')
depth = input('Enter an order book depth: ')

# Plotting presets
fig, ax = plt.subplots(2,2)
fig.suptitle(coin_symbol, size=15, weight='bold')
plt.style.use('seaborn-dark-palette')
fig.patch.set_facecolor('gainsboro')

def animate(i):
    """
    This function plots bid/ask, spread, order book depth and imbalance in real time.
    """
    global coin_symbol, depth

    data = dc.collect_data(coin_symbol + '-PERP',depth)

    bid_ask, spread = bas.combined_bid_ask(data)
    bid_depth, ask_depth, imbalance = bd.order_book_depth(data)

    # Need oldest bid-ask time in order to only plot trades that have occured within
    # the time frame that is shown by the bid-ask on the plot.
    oldest_bid_ask_time = bid_ask.index[0]
    trades, trade_plot_params = t.combined_trades(coin_symbol,oldest_bid_ask_time)

    # Bid Ask Trades
    ax[0,0].cla()
    ax[0,0].ticklabel_format(axis='y', useOffset=None)
    ax[0,0].set_title('BID/ASK', loc='left')
    ax[0,0].set_prop_cycle(color=['forestgreen', 'firebrick'])
    ax[0,0].margins(x=0)
    ax[0,0].plot(bid_ask)
    ax[0,0].scatter(trades.index, trades['price'], c=trade_plot_params['color'],
                    s=trade_plot_params['markersize'], alpha=0.5)

    # Spread
    ax[1,0].cla()
    ax[1,0].set_title('SPREAD', loc='left')
    ax[1,0].margins(x=0)
    ax[1,0].tick_params(labelbottom=False, bottom=False)
    ax[1,0].plot(spread, color='black')

    # Order Book Depth
    ax[0,1].cla()
    ax[0,1].margins(x=0,y=0)
    ax[0,1].set_title('DEPTH', loc='left')
    ax[0,1].step(bid_depth.index, bid_depth.values, color='green')
    ax[0,1].step(ask_depth.index, ask_depth.values, color='red')
    ax[0,1].fill_between(bid_depth.index, bid_depth.values, step='pre', color='green', alpha=0.3)
    ax[0,1].fill_between(ask_depth.index, ask_depth.values, step='pre', color='red', alpha=0.3)

    # Book Imbalance
    imbalance = imbalance.values
    ax[1,1].cla()
    ax[1,1].set_title('IMBALANCE', loc='left')
    ax[1,1].margins(x=0)
    ax[1,1].tick_params(labelbottom=False, bottom=False)
    ax[1,1].plot(imbalance, color='black')
    xaxis = np.zeros(len(imbalance))
    xs = list(range(len(imbalance)))
    ax[1,1].fill_between(xs, imbalance, where=imbalance > xaxis, interpolate=True, color='green', alpha=0.3)
    ax[1,1].fill_between(xs, imbalance, where=imbalance < xaxis, interpolate=True, color='red', alpha=0.3)


ani = FuncAnimation(plt.gcf(),animate,interval=10)
plt.show()
