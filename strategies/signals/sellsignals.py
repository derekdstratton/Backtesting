def price_goes_over_one_standard_deviation_away(context, data, equity):
    moving_stdev = data.history(equity, 'price', bar_count=20, frequency="1d").std()
    current_price = data.current(equity, 'price')
    expected_price = data.history(equity, 'price', bar_count=20, frequency="1d").rolling(20).mean()[-1]

    # long position
    if context.portfolio.positions[equity].amount > 0:
        return current_price < expected_price - moving_stdev

    # short position
    elif context.portfolio.positions[equity].amount < 0:
        return current_price > expected_price + moving_stdev


def profit_exit_2r(context, data, equity):
    current_price = data.current(equity, 'price')

    original_loss = context.portfolio.positions[equity].cost_basis * .05

    # long position
    if context.portfolio.positions[equity].amount > 0:
        return current_price > context.portfolio.positions[equity].cost_basis + 2 * original_loss

    # short position
    if context.portfolio.positions[equity].amount < 0:
        return current_price < context.portfolio.positions[equity].cost_basis + 2 * original_loss


def basic_stop_loss(context, data, equity):
    current_price = data.current(equity, 'price')

    # long position
    if context.portfolio.positions[equity].amount > 0:
        return current_price < (context.portfolio.positions[equity].cost_basis * .95)

    # short position
    if context.portfolio.positions[equity].amount < 0:
        return current_price > (context.portfolio.positions[equity].cost_basis * .95)

# todo put in a trailing stop loss that adjusts to 95% of the price when the stock makes a new high
# todo also look into using a different stop loss than 5%, experiment with large ones like 25
