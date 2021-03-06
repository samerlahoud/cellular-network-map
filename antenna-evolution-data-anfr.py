# Get the json file from data.anfr.fr
# Two filter in use: postal code and activation
# This does not provide all resutls for a city with multiple postal codes

import sys
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'CMU Serif'
plt.rcParams['axes.labelsize'] = 14
#plt.rcParams.update({'font.size': 12})

# Read .csv and parse date column
antennas = pd.read_csv('./data/aggregate-rennes/data-anfr-35000-active.csv', sep=';', \
    index_col=['emr_dt_service'], parse_dates=['emr_dt_service'])

# Add year and month column
antennas['month'] = antennas.index.strftime('%Y-%m')
antennas['year'] = antennas.index.strftime('%Y')

# Group by month then by emr_lb_systeme (technology)
# Put in a a matrix (month, emr_lb_systeme) with unstack 
# Replace nan with zero then compute a cumulative sum
cumul_antennas = antennas.groupby(['month','emr_lb_systeme']).size().unstack().fillna(0).cumsum()
perc_antennas = cumul_antennas.div(cumul_antennas.sum(axis=1), axis=0)

n=10
fig, ax = plt.subplots()
cumul_antennas.plot(kind='bar',stacked=True, ax=ax)
ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::n])
ax.xaxis.set_ticklabels(ticklabels[::n])
ax.set_xlabel("Date of deployment")
ax.set_ylabel("Cumulated number of antennas")
plt.tight_layout()
ax.get_legend().set_title('Frequency band')
fig.savefig('./output/cum_antenna_evo_incomplete.pdf', format='pdf', bbox_inches='tight')

fig, ax = plt.subplots()
perc_antennas.plot(kind='bar',stacked=True, ax=ax)
ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::n])
ax.xaxis.set_ticklabels(ticklabels[::n])
ax.set_xlabel("Date of deployment")
ax.set_ylabel("Percentage of antennas")
plt.xticks(rotation=90)
plt.tight_layout()
ax.get_legend().set_title('Frequency band')
fig.savefig('./output/perc_antenna_evo_incomplete.pdf', format='pdf', bbox_inches='tight')