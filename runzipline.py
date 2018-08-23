import os, datetime as dt, random
import csv
import numpy as np

#do it 5 times
#file = open("simulatordata.csv", "a")
#file.write("Data:\n")
#file.close()

for x in range(1, 20):
    startdate=dt.date(2000,1,1)
    #  nbdays=(dt.date.today()-startdate).days
    nbdays=(dt.date(2017, 1, 1)-startdate).days
    d=random.randint(0,nbdays)
    rand_date=startdate+dt.timedelta(days=d)

    start_date_string = str(rand_date)

    end_date_string = str(rand_date + dt.timedelta(days=365))

    os.system('zipline run -f simulatortest2.py --start %s --end %s -o pickles/sim%s.pickle --capital-base 10000' %
              (start_date_string, end_date_string, x))
    if x != 19:
        file = open("simulatordata.csv", "a")
        file.write(", ")
        file.close()
    else:
        file = open("simulatordata.csv", "a")
        file.write("\n")
        file.close()


expectancies = []
file = open("simulatordata.csv", "r")
reader = csv.reader(file, delimiter=",")
for row in reader:
    expectancies = row
file.close()
print(expectancies)

fixed = [float(x) for x in expectancies]

file = open("simulatordata.csv", "a")
avg_expectancy = float(np.mean(fixed))
std_expectancy = float(np.std(fixed))
file.write("Average Exp: %f, " % avg_expectancy)
file.write("StDev Exp: %f, " % std_expectancy)
my_sqn = avg_expectancy / std_expectancy
file.write("MySQN: %f, " % my_sqn)
min = float(np.min(fixed))
file.write("Min Exp: %f" % min)