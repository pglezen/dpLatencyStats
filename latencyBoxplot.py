# Generate DataPower latency boxplots by URI
#
import pandas as pd
from matplotlib import pyplot as plt

# Read in the CSV data and make a new 'Latency' column
# containing the maximum of the 16 measurement columns.
#
df1 = pd.read_csv('sample6.csv', parse_dates=['Time'])
df1['Latency'] = df1.loc[:,'1':'16'].apply(max, axis=1)

# Make a boxplot of Latencies by URI.
df1.boxplot(column='Latency', by=['uri'])
plt.show()
