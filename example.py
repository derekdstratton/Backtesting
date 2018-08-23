from zipline.api import order_target, record, symbol
import matplotlib.pyplot as plt
import zipline
import datetime

def initialize(context):
    context.day = 0
    context.asset = symbol('AAPL')
    print(zipline.api.get_environment(field="capital_base"))

    context.totalequity = zipline.api.get_environment(field="capital_base")


def handle_data(context, data):
    # Skip first 300 days to get full windows, avoid stock split
    context.day += 1
    if context.day < 300:
        return

    ### Trading Strategy starts here.

    # Compute averages
    # data.history() has to be called with the same params
    # from above and returns a pandas dataframe.
    short_mavg = data.history(context.asset, 'price', bar_count=100, frequency="1d").mean()
    long_mavg = data.history(context.asset, 'price', bar_count=300, frequency="1d").mean()

    # Trading logic
    if short_mavg > long_mavg:
        # order_target orders as many shares as needed to
        # achieve the desired number of shares.
        order_target(context.asset, 100)
        aaplList = zipline.api.get_open_orders(asset=symbol('AAPL'))
        if len(aaplList) > 0:  # indicates an order has just been placed to sell
            print("buy")
    elif short_mavg < long_mavg:
        order_target(context.asset, 0)
        aaplList = zipline.api.get_open_orders(asset=symbol('AAPL'))
        if len(aaplList) > 0:  # indicates an order has just been placed to sell
            print("sell")

    ### Trading Strategy ends here.

    #print(zipline.api.get_open_orders(asset=symbol('AAPL')))
    aaplList = zipline.api.get_open_orders(asset=symbol('AAPL'))
    #if len(aaplList) > 0:
        #print(aaplList.pop(0))

    ## Figure out how to get the current price on a day, or the current portfolio value on a day
    #print(data.current(context.asset, 'price'))

    # Save values for later inspection
    record(AAPL=data.current(context.asset, 'price'),
           short_mavg=short_mavg,
           long_mavg=long_mavg)

    #print(zipline.api.get_environment(field="capital_base"))


def analyze(context, perf):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio value in $')

    ax2 = fig.add_subplot(212)
    perf['AAPL'].plot(ax=ax2)
    perf[['short_mavg', 'long_mavg']].plot(ax=ax2)

    perf_trans = perf.ix[[t != [] for t in perf.transactions]]
    buys = perf_trans.ix[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
    sells = perf_trans.ix[
        [t[0]['amount'] < 0 for t in perf_trans.transactions]]
    ax2.plot(buys.index, perf.short_mavg.ix[buys.index],
             '^', markersize=10, color='m')
    ax2.plot(sells.index, perf.short_mavg.ix[sells.index],
             'v', markersize=10, color='k')
    ax2.set_ylabel('price in $')
    plt.legend(loc=0)
    plt.show()

