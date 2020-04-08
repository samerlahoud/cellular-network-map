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

# Add year and month column
antennas['month'] = antennas.index.strftime('%Y-%m')
antennas['year'] = antennas.index.strftime('%Y')

# Group by month then by emr_lb_systeme (technology)
# Put in a a matrix (month, emr_lb_systeme) with unstack 
# Replace nan with zero then compute a cumulative sum
cumul_antennas = antennas.groupby(['month','emr_lb_systeme']).size().unstack().fillna(0).cumsum()
perc_antennas = cumul_antennas.div(cumul_antennas.sum(axis=1), axis=0)

fig, ax = plt.subplots()
n=10
cumul_antennas.plot(kind='bar',stacked=True, ax=ax)
ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::n])
ax.xaxis.set_ticklabels(ticklabels[::n])
ax.set_xlabel("Date of deployment")
ax.set_ylabel("Cumulated number of antennas")
plt.tight_layout()
ax.get_legend().set_title('Frequency band')
fig.savefig('cum_antenna_evo.pdf')

fig, ax = plt.subplots()
perc_antennas.plot(kind='area',stacked=True, ax=ax)
ax.set_xlabel("Date of deployment")
ax.set_ylabel("Percentage of antennas")
plt.xticks(rotation=90)
plt.tight_layout()
ax.get_legend().set_title('Frequency band')
fig.savefig('perc_antenna_evo.pdf')