import datetime as dt
import random
import os
import numpy as np
import pandas as pd

STRATEGY_FILE = "strategy_follow_trends.py"
ITERATION_COUNT = 15

for iteration in range(0, ITERATION_COUNT):
    startdate = dt.date(2000, 1, 1)
    nbdays = (dt.date(2017, 1, 1) - startdate).days
    d = random.randint(0, nbdays)
    rand_date = startdate + dt.timedelta(days=d)

    start_date_string = str(rand_date)

    end_date_string = str(rand_date + dt.timedelta(days=365))

    os.system(
        'zipline run -f strategies/%s --start %s --end %s -o strategies/pickles/%s%d.pickle --capital-base 10000' %
        (STRATEGY_FILE, start_date_string, end_date_string, STRATEGY_FILE.split(".")[0], iteration))

# improvements to the portfolio, as decimal increases of their original value
# 1 means no money gain, 1.1 means 10% gain, etc.
values = []

for iteration in range(0, ITERATION_COUNT):
    portfolio = pd.read_pickle("strategies/pickles/%s%d.pickle" % (STRATEGY_FILE.split(".")[0], iteration))
    print(portfolio.portfolio_value[0])  # start val
    print(portfolio.portfolio_value[-1])  # end val
    improvement = float(portfolio.portfolio_value[-1]) / float(portfolio.portfolio_value[0])
    values.append(improvement)

print("\n-------------------\n")
print("Mean (Expectancy): %f" % np.mean(values))
print("Std: %f" % np.std(values))

