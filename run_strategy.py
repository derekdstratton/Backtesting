import os

STRATEGY_FILE = "strategy_follow_trends.py"
start_date_string = "2010-1-1"
end_date_string = "2011-1-1"

os.system('zipline run -f strategies/%s --start %s --end %s -o strategies/pickles/%s.pickle --capital-base 10000' %
              (STRATEGY_FILE, start_date_string, end_date_string, STRATEGY_FILE.split(".")[0]))