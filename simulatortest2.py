from zipline.api import order_target, record, symbol
from zipline.errors import SymbolNotFound
import matplotlib.pyplot as plt
import zipline

import sys, os

sys.path.append(os.getcwd())

import buysignals, sellsignals, shortsignals


# todo if i want to use buysignals, i need to make sure its in the path


def initialize(context):

    # todo: make function that will filter out stocks based on if they exist before a start session
    tickers = ['AAPL', 'GOOG', 'FB', 'TWTR', 'MSFT']

    tickers = ['ABT', 'ABBV', 'ACN', 'ACE', 'ADBE', 'ADT', 'AAP', 'AES', 'AET', 'AFL', 'AMG', 'A', 'GAS',
               'APD', 'ARG', 'AKAM', 'AA', 'AGN', 'ALXN', 'ALLE', 'ADS', 'ALL', 'ALTR', 'MO', 'AMZN', 'AEE',
               'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'APC', 'ADI', 'AON',
               'APA', 'AIV', 'AMAT', 'ADM', 'AIZ', 'T', 'ADSK', 'ADP', 'AN', 'AZO', 'AVGO', 'AVB', 'AVY',
               'BHI', 'BLL', 'BAC', 'BK', 'BCR', 'BXLT', 'BAX', 'BBT', 'BDX', 'BBBY', 'BRK-B', 'BBY', 'BLX',
               'HRB', 'BA', 'BWA', 'BXP', 'BSK', 'BMY', 'BRCM', 'BF-B', 'CHRW', 'CA', 'CVC', 'COG', 'CAM', 'CPB',
               'COF', 'CAH', 'HSIC', 'KMX', 'CCL', 'CAT', 'CBG', 'CBS', 'CELG', 'CNP', 'CTL', 'CERN', 'CF', 'SCHW', 'CHK',
               'CVX', 'CMG', 'CB', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CTXS', 'CLX', 'CME', 'CMS', 'COH', 'KO', 'CCE',
               'CTSH', 'CL', 'CMCSA', 'CMA', 'CSC', 'CAG', 'COP', 'CNX', 'ED', 'STZ', 'GLW', 'COST', 'CCI', 'CSX', 'CMI', 'CVS',
               'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DLPH', 'DAL', 'XRAY', 'DVN', 'DO', 'DTV', 'DFS', 'DISCA', 'DISCK', 'DG', 'DLTR',
               'D', 'DOV', 'DOW', 'DPS', 'DTE', 'DD', 'DUK', 'DNB', 'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA',
               'EMC', 'EMR', 'ENDP', 'ESV', 'ETR', 'EOG', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ES', 'EXC', 'EXPE',
               'EXPD', 'ESRX', 'XOM', 'FFIV', 'FB', 'FAST', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FSIV', 'FLIR', 'FLS',
               'FLR', 'FMC', 'FTI', 'F', 'FOSL', 'BEN', 'FCX', 'FTR', 'GME', 'GPS', 'GRMN', 'GD', 'GE', 'GGP', 'GIS',
               'GM', 'GPC', 'GNW', 'GILD', 'GS', 'GT', 'GOOGL', 'GOOG', 'GWW', 'HAL', 'HBI', 'HOG', 'HAR', 'HRS', 'HIG',
               'HAS', 'HCA', 'HCP', 'HCN', 'HP', 'HES', 'HPQ', 'HD', 'HON', 'HRL', 'HSP', 'HST', 'HCBK', 'HUM', 'HBAN',
               'ITW', 'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IRM', 'JEC', 'JBHT', 'JNJ',
               'JCI', 'JOY', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'GMCR', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS', 'KRFT', 'KR', 'LB',
               'LLL', 'LH', 'LRCX', 'LM', 'LEG', 'LEN', 'LVLT', 'LUK', 'LLY', 'LNC', 'LLTC', 'LMT', 'L', 'LOW', 'LYB', 'MTB',
               'MAC', 'M', 'MNK', 'MRO', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MHFI', 'MCK', 'MJN',
               'MMV', 'MDT', 'MRK', 'MET', 'KORS', 'MCHP', 'MU', 'MSFT', 'MHK', 'TAP', 'MDLZ', 'MON', 'MNST', 'MCO', 'MS', 'MOS',
               'MSI', 'MUR', 'MYL', 'NDAQ', 'NOV', 'NAVI', 'NTAP', 'NFLX', 'NWL', 'NFX', 'NEM', 'NWSA', 'NEE', 'NLSN', 'NKE', 'NI',
               'NE', 'NBL', 'JWN', 'NSC', 'NTRS', 'NOC', 'NRG', 'NUE', 'NVDA', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'OI', 'PCAR',
               'PLL', 'PH', 'PDCO', 'PAYX', 'PNR', 'PBCT', 'POM', 'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD',
               'PBI', 'PCL', 'PNC', 'RL', 'PPG', 'PPL', 'PX', 'PCP', 'PCLN', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM',
               'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RRC', 'RTN', 'O', 'RHT', 'REGN', 'RF', 'RSG', 'RAI', 'RHI', 'ROK', 'COL', 'ROP',
               'ROST', 'RLC', 'R', 'CRM', 'SNDK', 'SCG', 'SLB', 'SNI', 'STX', 'SEE', 'SRE', 'SHW', 'SIAL', 'SPG', 'SWKS', 'SLG', 'SJM',
               'SNA', 'SO', 'LUV', 'SWN', 'SE', 'STJ', 'SWK', 'SPLS', 'SBUX', 'HOT', 'STT', 'SRCL', 'SYK', 'STI', 'SYMC', 'SYY',
               'TROW', 'TGT', 'TEL', 'TE', 'TGNA', 'THC', 'TDC', 'TSO', 'TXN', 'TXT', 'HSY', 'TRV', 'TMO', 'TIF', 'TWX', 'TWC', 'TJK', 'TMK', 'TSS',
               'TSCO', 'RIG', 'TRIP', 'FOXA', 'TSN', 'TYC', 'UA', 'UNP', 'UNH', 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'URBN', 'VFC', 'VLO', 'VAR', 'VTR',
               'VRSN', 'VZ', 'VRTX', 'VIAB', 'V', 'VNO', 'VMC', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'ANTM', 'WFC', 'WDC', 'WU', 'WY', 'WHR', 'WFM', 'WMB',
               'WEC', 'WYN', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XL', 'XYL', 'YHOO', 'YUM', 'ZBH', 'ZION', 'ZTS']

    context.equities = []
    for ticker in tickers:
        try:
            equity = symbol(ticker)
            context.equities.append(equity)
        except SymbolNotFound:
            pass

    context.day = 0
    # context.equities = [symbol('AAPL'), symbol('GOOG')]


def handle_data(context, data):

    context.day = context.day + 1
    print("Day: %d" % context.day)

    # selling, look at all equities i have a position on
    for equity in context.portfolio.positions:
        # current price
        current_price = data.current(equity, 'price')

        # sell_signals = sellsignals.long_moving_avg_greater_than_short_moving_avg(context, data, equity)
        sell_signals = sellsignals.price_goes_over_one_standard_deviation_away(context, data, equity) or \
                       sellsignals.basic_stop_loss(context, data, equity)

        # sell signal
        if sell_signals:
            print("sell %d shares of %s, for %f: " % (context.portfolio.positions[equity].amount, equity,
                                                      data.current(equity, 'price')))
            order_target(equity, 0)  # value should be 0

    # buying, look at all equities that i'm viewing
    for equity in context.equities:
        # todo check each equity to see if it's valid/trade-able before going further

        # only order if there is no currently open position for this equity
        if all(position_equity != equity for position_equity in context.portfolio.positions):
            buy_signals = buysignals.short_moving_avg_greater_than_long_moving_avg(context, data, equity) and \
                          buysignals.enough_cash_to_buy(context, data, equity) and \
                          buysignals.price_is_trending_up(context, data, equity)

            short_signals = shortsignals.long_moving_avg_greater_than_short_moving_avg(context, data, equity) and \
                            shortsignals.enough_cash_to_short(context, data, equity) and \
                            shortsignals.price_is_trending_down(context, data, equity)

            # current price
            current_price = data.current(equity, 'price')
            # r is the risk, which is 1% of the total equity
            r = .01 * context.portfolio.portfolio_value
            # n is the number of shares to buy
            n = 20 * r / current_price

            # Place order if the buy_signal is true and we have enough cash to buy
            if buy_signals:
                order_target(equity, n)
                print("buy %d shares of %s, for: %f" % (n, equity, current_price))
            # todo shorting
            if short_signals:
                order_target(equity, -1 * n)
                print("short %d shares of %s, for: %f" % (n, equity, current_price))

        # Record the data to view later
        # recorded_data = {equity.symbol: current_price, 'short_mavg' + equity.symbol: short_mavg,
        #                 'long_mavg' + equity.symbol: long_mavg}
        # record(**recorded_data)


def analyze(context, perf):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio value in $')
    plt.show()
    # fig.savefig('plots/portfolio.png')

    '''
    for equity in context.equities:
        name = equity.symbol

        fig = plt.figure()
        ax2 = fig.add_subplot(111)
        ax2.set_ylabel('price in $')
        perf[name].plot(ax=ax2)
        perf[['short_mavg' + name, 'long_mavg' + name]].plot(ax=ax2)
        plt.show()
        # fig.savefig('plots/%s.png' % equity)
    '''
    print(context.portfolio.portfolio_value)
