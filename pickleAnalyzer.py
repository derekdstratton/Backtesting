import pandas as pd

data1 = pd.read_pickle("pickles/sim1.pickle")
print(data1)

print(data1.columns)

print(data1.algo_volatility)