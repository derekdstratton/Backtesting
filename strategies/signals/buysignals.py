import statsmodels.api as sm

def short_moving_avg_greater_than_long_moving_avg(context, data, equity):
    # moving averages- indicators
    short_mavg = data.history(equity, 'price', bar_count=20, frequency="1d").mean()
    long_mavg = data.history(equity, 'price', bar_count=60, frequency="1d").mean()
    return short_mavg > long_mavg


def price_is_trending_up(context, data, equity):
    prices = data.history(equity, 'price', bar_count=20, frequency="1d")
    dates = range(1, prices.size + 1)
    dates = sm.add_constant(dates)
    model = sm.OLS(prices, dates)
    results = model.fit()
    # print(results.params)
    return results.params[1] > 0.6

def enough_cash_to_buy(context, data, equity):
    # current price
    current_price = data.current(equity, 'price')
    # r is the risk, which is 1% of the total equity
    r = .01 * context.portfolio.portfolio_value
    # n is the number of shares to buy
    n = 20 * r / current_price

    return n * current_price < context.portfolio.cash
