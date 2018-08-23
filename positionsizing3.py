from zipline.api import order_target, record, symbol
import zipline
import matplotlib.pyplot as plt
import pandas as pd


def initialize(context):
    # context.day = 0

    #cash + money in stocks
    context.total_equity = zipline.api.get_environment(field="capital_base")

    #cash money on hand
    context.cash = context.total_equity

    # the risk r, 1% of total equity
    context.r = context.total_equity * .01  # The r multiple

    equities = ['AAPL', 'GOOG', 'MSFT', 'FB', 'TWTR']

    initial_data = {'equity': equities,
                    'shares_owned': [0 for x in equities],
                    'buy_price': [0 for x in equities],
                    'current_price': [0 for x in equities],
                    'current_value': [0 for x in equities],
                    'asset': [symbol(x) for x in equities]}

    context.df = pd.DataFrame(initial_data)

    context.df = context.df.set_index('equity')

def handle_data(context, data):
    # context.day += 1
    #if context.day < 300:
        #return

    stock_money = 0

    for equity in context.df.index:
        # current price
        context.df.at[equity, 'current_price'] = data.current(context.df.loc[equity]['asset'], 'price')

        # current value
        context.df.at[equity, 'current_value'] = context.df.loc[equity]['current_price'] * context.df.loc[equity]['shares_owned']

        # n is the number of shares to buy
        n = 20*context.r/context.df.loc[equity]['current_price']

        # moving averages- indicators
        short_mavg = data.history(context.df.loc[equity]['asset'], 'price', bar_count=100, frequency="1d").mean()
        long_mavg = data.history(context.df.loc[equity]['asset'], 'price', bar_count=300, frequency="1d").mean()

        #Start with the stop loss
        if context.df.loc[equity]['current_price'] < context.df.loc[equity]['buy_price'] * .95: #95% stop
            zipline.api.order_target(context.df.loc[equity]['asset'], 0)  # value should be 0

            orders = zipline.api.get_open_orders(context.df.loc[equity]['asset'])
            if len(orders) > 0:  # indicates an order has just been placed to sell

                print("stopped %d shares of %s, for: %f" % (
                context.df.loc[equity]['shares_owned'], equity, context.df.loc[equity]['current_value']))

                context.df.at[equity, 'current_value'] = 0
                context.cash += context.df.loc[equity]['shares_owned'] * context.df.loc[equity]['current_price']
                context.df.at[equity, 'buy_price'] = 0
                context.df.at[equity, 'shares_owned'] = 0


        #Buy signal
        elif short_mavg > long_mavg and context.df.loc[equity]['current_value'] == 0 and \
                n * context.df.loc[equity]['current_price'] < context.cash:
            zipline.api.order_target(context.df.loc[equity]['asset'], n)  # value should be 20*R (5% stop loss)

            orders = zipline.api.get_open_orders(context.df.loc[equity]['asset'])
            if len(orders) > 0:  # indicates an order has just been placed to sell
                context.df.at[equity, 'current_value'] = n * context.df.loc[equity]['current_price']
                context.cash -= context.df.loc[equity]['current_value']
                context.df.at[equity, 'buy_price'] = context.df.loc[equity]['current_price']
                context.df.at[equity, 'shares_owned'] = n
                print("buy %d shares of %s, for: %f" % (context.df.loc[equity]['shares_owned'], equity,
                                                       context.df.loc[equity]['current_value']))

        #Sell signal
        elif short_mavg < long_mavg:
            zipline.api.order_target(context.df.loc[equity]['asset'], 0)  # value should be 0

            orders = zipline.api.get_open_orders(context.df.loc[equity]['asset'])
            if len(orders) > 0:  # indicates an order has just been placed to sell
                print("sell %d shares of %s, for %f: " % (
                    context.df.loc[equity]['shares_owned'], equity, context.df.loc[equity]['current_value']))

                context.df.at[equity, 'current_value'] = 0
                context.cash += context.df.loc[equity]['shares_owned'] * context.df.loc[equity]['current_price']
                context.df.at[equity, 'buy_price'] = 0
                context.df.at[equity, 'shares_owned'] = 0

        stock_money += context.df.loc[equity]['current_value']

        dict1 = {equity: context.df.loc[equity]['current_price'], 'short_mavg' + equity: short_mavg,
                'long_mavg' + equity: long_mavg}
        record(**dict1)

        # Data:
        # print("%s Stock Money: %d" % (equity, context.df.loc[equity]['current_value']))
        # print("%s Shares Owned: %d" % (equity, context.df.loc[equity]['shares_owned']))

    #Data:
    print("Cash: %d", context.cash)

    context.total_equity = context.cash + stock_money
    context.r = context.total_equity * .01


def analyze(context, perf):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio value in $')
    plt.show()

    # Stock data:
    '''
    for equity in context.df.index:
        fig = plt.figure()
        ax2 = fig.add_subplot(111)
        ax2.set_ylabel('price in $')
        perf[equity].plot(ax=ax2)
        perf[['short_mavg' + equity, 'long_mavg' + equity]].plot(ax=ax2)
        plt.show()
    '''

    print(perf)

    # System data can now be found
    ### Compute portfolio final - portfolio initial
