from zipline.api import order_target, record, symbol
import zipline
import matplotlib.pyplot as plt


def initialize(context):
    context.day = 0
    #context.asset = symbol('AAPL')
    context.asset = symbol('GOOG')

    #cash + money in stocks
    context.total_equity = zipline.api.get_environment(field="capital_base")

    #cash money on hand
    context.cash = context.total_equity

    #money in stocks
    context.aaplstockmoney = 0

    #the risk r, 1% of total equity
    context.r = context.total_equity*.01 #The r multiple

    #the price i last bought apple at
    context.aaplbuyprice = 0 #the buy price for orders

    #the total shares of apple bound
    context.aapl_shares_bought = 0

def handle_data(context, data):
    context.day += 1
    if context.day < 300:
        return

    short_mavg = data.history(context.asset, 'price', bar_count=100, frequency="1d").mean()
    long_mavg = data.history(context.asset, 'price', bar_count=300, frequency="1d").mean()

    current_price = data.current(context.asset, 'price')

    # n is the value of the apple
    # n = 100
    n = 20*context.r/current_price

    context.aaplstockmoney = current_price*context.aapl_shares_bought

    #Start with the stop loss
    if current_price < context.aaplbuyprice * .95: #95% stop
        zipline.api.order_target(context.asset, 0)  # value should be 0

        aaplList = zipline.api.get_open_orders(context.asset)
        if len(aaplList) > 0:  # indicates an order has just been placed to sell
            context.aaplstockmoney = 0
            context.cash += context.aapl_shares_bought * current_price
            context.aaplbuyprice = 0
            context.aapl_shares_bought = 0
            print("stopped at: %f" % current_price)

    #Buy signal
    elif short_mavg > long_mavg and context.aaplstockmoney == 0:
        zipline.api.order_target(context.asset, n)  # value should be 20*R (5% stop loss)

        aaplList = zipline.api.get_open_orders(context.asset)
        if len(aaplList) > 0:  # indicates an order has just been placed to sell
            context.aaplstockmoney = n * current_price
            context.cash -= context.aaplstockmoney
            context.aaplbuyprice = current_price
            context.aapl_shares_bought = n
            print("buy, at: %f" % current_price)

    #Sell signal
    elif short_mavg < long_mavg:
        zipline.api.order_target(context.asset, 0)  # value should be 0

        aaplList = zipline.api.get_open_orders(context.asset)
        if len(aaplList) > 0:  # indicates an order has just been placed to sell
            context.aaplstockmoney = 0
            context.cash += context.aapl_shares_bought * current_price
            context.aaplbuyprice = 0
            context.aapl_shares_bought = 0
            print("sell, at %f: " % current_price)

    #Data:
    #  print("N: %d, Equity: %d" % (n, context.total_equity))
    print("AAPL Stock Money: %d, Cash on hand: %d" % (context.aaplstockmoney, context.cash))


    context.total_equity = context.cash + context.aaplstockmoney
    context.r = context.total_equity * .01

    dict1 = {'AAPL': data.current(context.asset, 'price')}

    record(**dict1)
    record(short_mavg=short_mavg, long_mavg=long_mavg)
    #  print(dict1.keys())

def analyze(context, perf):
    #  print(type(perf.keys()[0]))
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio value in $')

    ax2 = fig.add_subplot(212)
    perf['AAPL'].plot(ax=ax2)
    perf[['short_mavg', 'long_mavg']].plot(ax=ax2)
    '''
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
    '''
    plt.show()
