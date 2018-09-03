# Backtesting
This is a backtester for trading algorithms.

## Requirements:
- Anaconda
- Zipline
- Quandl
- PyCharm (Recommended)

## Setup:
1. Install Anaconda, and set up an environment for the project
2. Install Zipline in that environment
3. Make sure the Quandl API Key is set in environment variables
4. Using zipline in that environment, ingest data with quandl
5. The trading algorithm can now be run in this environment
6. For convenience use in PyCharm, go to Tools > Terminal > Shell Path, and enter:

    cmd.exe "/K"  "C:\Apps\Anaconda3\Scripts\activate.bat" "C:\Apps\Anaconda3\envs\backtesting"

## Usage:
run_backtest.py: This file runs a backtest for a particular strategy. It simulates the strategy
on random time periods and finds results for various testing.

run_strategy.py: This file runs a strategy once on the same time period, which is useful for 
debugging a strategy before using run_backtest

Strategy files: Strategy files follow the standard Quantopian format, with Initialize()
and Handle_Data() methods. These are the files that will be used in the system.

Signals: Signals are used as indicators of when to buy, sell, and short a position. These are
used in strategy files, and form the basis of a successful trading system. To add a signal,
simply add a function in the file. Every sell signal should account for if the original 
position was bought or shorted for the system to work properly.

Watchlist: Choose an array of equities in this file that will be watched during the trading. 
Obviously, more equities takes longer to process.

Pickles: Pandas dataframes of the performance are stored in files in this directory, used for
later analysis.

## Contributing:
To make a trading strategy, make a new strategy in the strategies folder called \
`strategy_MY_STRATEGY_NAME.py`. This should be a copy of strategy_template.py. Pretty much
focus on editing the signals and the watchlist used. Then the strategy can be tested by
changing the parameter for run_backtest or run_strategy.

The trading strategy should have a logical basis, and ideas about the market are what's
being traded.


## References:
Zipline: https://www.zipline.io/index.html

Quantopian: https://www.quantopian.com/help

Conda: https://conda.io/docs/

## Issues/TODO:
- Add market filters, basically some way to test strategies based on the market type, because
some strategies work well in some markets and work poorly in others. By market type, I mean
both trend (bull/bear/sideways) and volatility (quiet/volatile/neutral)
- Right now, Quandl is used for data, which provides daily data for testing. It would be nice 
to have a data source with minute data for testing for looking at real-time trading.
- This backtester's goal is to create algorithms that can be transferred to Paper Trading/
Live Trading with Interactive Brokers. There's a separate Repo for that, but the goal is for
the code here to be easily transferred to Zipline-Live or IBridgePy. Still deciding about this.

## Credit
Code written by Derek Stratton