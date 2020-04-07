# Get the json file from data.anfr.fr
# Two filter in use: postal code and activation
import sys
import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Read .csv and parse date column
antennas = pd.read_csv('./data/cartoradio-35000/7a2457be-a5f1-4075-8481-4515fc90acc0.csv', sep=';', \
    index_col=['emr_dt_service'], parse_dates=['emr_dt_service'])

# Add year column
antennas['month'] = antennas.index.strftime('%Y-%m')
cumul_antennas = antennas.groupby(['month','emr_lb_systeme']).size().unstack().fillna(0).cumsum()
perc_antennas = cumul_antennas.div(cumul_antennas.sum(axis=1), axis=0)
# Group by month then by emr_lb_systeme (technology)
# Put in a a matrix (month, emr_lb_systeme) with unstack 
# Replace nan with zero then compute a cumulative sum
fig, ax = plt.subplots()
cumul_antennas.plot(kind='bar',stacked=True, ax=ax)
plt.show()

fig, ax = plt.subplots()
perc_antennas.plot(kind='bar',stacked=True, ax=ax)
plt.show()