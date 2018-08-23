from zipline.api import order_target, record, symbol
import zipline
import matplotlib.pyplot as plt


def initialize(context):
    context.day = 0
    context.asset = symbol('AAPL')

    context.total_equity = zipline.api.get_environment(field="capital_base")
    context.cash = context.total_equity
    context.aaplstockmoney = 0
    context.r = context.total_equity*.01 #The r multiple
    context.aaplbuyprice = 0 #the buy price for orders
    context.buyamount = 100

def handle_data(context, data):
    context.day += 1
    if context.day < 300:
        return

    short_mavg = data.history(context.asset, 'price', bar_count=100, frequency="1d").mean()
    long_mavg = data.history(context.asset, 'price', bar_count=300, frequency="1d").mean()

    # n is the number of shares to buy or sell
    n = 100
    # todo make n better
    import math
    n = math.floor(20*context.r/(data.current(context.asset, 'price')))  # type: int
    n = 100
    #print(n)


    if data.current(context.asset, 'price') < context.aaplbuyprice * 0.95: #5% stop loss
        order_target(context.asset, 0)
        context.aaplstockmoney = 0
        aaplList = zipline.api.get_open_orders(asset=symbol('AAPL'))
        if len(aaplList) > 0:  # indicates an order has just been placed to sell
            context.cash += context.buyamount * data.current(context.asset, 'price')
            context.aaplbuyprice = 0
            context.buyamount = 0
            print("selling at %d" % n)
            print(context.total_equity)
    elif short_mavg > long_mavg:
        order_target(context.asset, n)
        context.aaplstockmoney = context.buyamount*data.current(context.asset, 'price')
        aaplList = zipline.api.get_open_orders(asset=symbol('AAPL'))
        if len(aaplList) > 0: #indicates an order has just been placed to buy
            print("buying at %d" % n)
            print(context.total_equity)
            context.cash -= n*data.current(context.asset, 'price')
            context.aaplbuyprice = data.current(context.asset, 'price')
            context.buyamount = n
    elif short_mavg < long_mavg:
        order_target(context.asset, 0)
        context.aaplstockmoney = 0
        aaplList = zipline.api.get_open_orders(asset=symbol('AAPL'))
        if len(aaplList) > 0: #indicates an order has just been placed to sell
            context.cash += context.buyamount*data.current(context.asset, 'price')
            context.aaplbuyprice = 0
            context.buyamount = 0
            print("selling at %d" % n)
            print(context.total_equity)

    context.total_equity = context.cash + context.aaplstockmoney
    context.r = context.total_equity*.01
    # print(context.total_equity)



    #print(zipline.api.get_open_orders(asset=symbol('AAPL')))
    aaplList = zipline.api.get_open_orders(asset=symbol('AAPL'))

    if len(aaplList) > 0:
        print(aaplList.pop(0))

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

