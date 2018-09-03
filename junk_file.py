# Junk File is a place to test random things to see how they work for debugging, not part of the trading system.

import pandas, numpy
import matplotlib.pyplot as plt

d = {'equity': ['AAPL', 'GOOG'], 'shares_owned': [100, 0], 'buy_price': [137.31, 0], 'current_price': [0, 0], 'current_value':[145, 0]}
df = pandas.DataFrame(d)

df = df.set_index('equity')

#Print the whole data structure
print(df)

rolling = df.ro
'''
#  Accessing an individual value
print('Shares of apple:')
print(df.loc['AAPL']['shares_owned'])

for e in df.index:
    print(df.loc[e]['buy_price'])

plt.plot([1, 2, 3])
plt.show()

plt.plot([4, 5, 6])
plt.show()
'''

ser = pandas.Series([1, 2, 3, 4, 5])

'''
print(ser)
print(ser[0])
print(ser[ser.size - 1])

print(numpy.mean([1,2,3,4])) #mean
print(numpy.std([1,2,3,4])) #standard deviation

ratio = numpy.mean([1,2,3,4]) / numpy.std([1,2,3,4])
print(ratio)

x = '1.234'
print(float(x))
'''
