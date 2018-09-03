from zipline.api import order_target, symbol
from zipline.errors import SymbolNotFound
import matplotlib.pyplot as plt

import sys, os

sys.path.append(os.getcwd())

from strategies import watchlist
from strategies.signals import shortsignals, buysignals, sellsignals

# Every trade should risk 1% of total equity
RISK_PERCENTAGE = 0.01


def initialize(context):
    tickers = watchlist.speedy

    context.equities = []
    for ticker in tickers:
        try:
            equity = symbol(ticker)
            context.equities.append(equity)
        except SymbolNotFound:
            pass

    context.day = 0


def handle_data(context, data):

    context.day = context.day + 1
    print("Day: %d" % context.day)
    print("Cash: %d" % context.portfolio.cash)
    # print("Positions: ")
    # print(context.portfolio.positions, sep=" ")

    position_amount = len(context.portfolio.positions) # this it the number of positions at the start of the day
    # this is tracked because context.portfolio.positions is updated on each iteration
    # the goal is to be involved in no more than 4 positions at a time

    # selling, look at all equities i have a position on
    for equity in context.portfolio.positions:
        # current price
        current_price = data.current(equity, 'price')

        # sell_signals = sellsignals.long_moving_avg_greater_than_short_moving_avg(context, data, equity)
        sell_signals = sellsignals.price_goes_over_one_standard_deviation_away(context, data, equity) or \
                       sellsignals.basic_stop_loss(context, data, equity) or \
                       sellsignals.profit_exit_2r(context, data, equity)

        # sell signal
        if sell_signals:
            print("sell %d shares of %s, for %f: " % (context.portfolio.positions[equity].amount, equity,
                                                      data.current(equity, 'price')))
            order_target(equity, 0)  # value should be 0
            position_amount -= 1

    # buying, look at all equities that i'm viewing
    for equity in context.equities:
        # less than 5 positions at a given time
        # only order if there is no currently open position for this equity
        if position_amount < 5 and all(position_equity != equity for position_equity in context.portfolio.positions):
            buy_signals = buysignals.short_moving_avg_greater_than_long_moving_avg(context, data, equity) and \
                          buysignals.enough_cash_to_buy(context, data, equity) and \
                          buysignals.price_is_trending_up(context, data, equity)

            short_signals = shortsignals.long_moving_avg_greater_than_short_moving_avg(context, data, equity) and \
                            shortsignals.enough_cash_to_short(context, data, equity) and \
                            shortsignals.price_is_trending_down(context, data, equity)

            # current price
            current_price = data.current(equity, 'price')
            # r is the risk, which is 1% of the total equity
            r = RISK_PERCENTAGE * context.portfolio.portfolio_value
            # n is the number of shares to buy
            n = 20 * r / current_price

            # Place order if the buy_signal is true and we have enough cash to buy
            if buy_signals:
                order_target(equity, n)
                print("buy %d shares of %s, for: %f" % (n, equity, current_price))
                position_amount += 1
            if short_signals:
                order_target(equity, -1 * n)
                print("short %d shares of %s, for: %f" % (n, equity, current_price))
                position_amount += 1


def analyze(context, perf):
    # Show the portfolio value over time
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio value in $')
    plt.show()
    # fig.savefig('plots/portfolio.png')
    # print(context.portfolio.portfolio_value)
