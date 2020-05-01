# Data is obtained by anfr and cartoradio
# Adapted for cities with mutiple postal codes
import sys
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'CMU Serif'
plt.rcParams['axes.labelsize'] = 14
#plt.rcParams.update({'font.size': 12})

base_folder = './data/aggregate-rennes/'

# Remove french accents and spaces from column names
# support_df includes all type of antennas not only for mobile communications 
support_df = pd.read_csv(base_folder+'cartoradio-rennes/Supports_Cartoradio.csv', sep=';')
support_id = support_df.Numero_du_support

antennas = pd.read_csv(base_folder+'data-anfr-rennes-lsquare-active.csv', sep=';', \
    index_col=['emr_dt_service'], parse_dates=['emr_dt_service'])

# Keep only the city antennas
antennas = antennas[antennas.sup_id.isin(support_id.values)]

# Add year and month column
antennas['month'] = antennas.index.strftime('%Y-%m')
antennas['year'] = antennas.index.strftime('%Y')
antennas['freq_band'] = antennas.emr_lb_systeme.str.split(expand=True)[1]

# Group by month then by emr_lb_systeme (technology)
# Put in a a matrix (month, emr_lb_systeme) with unstack 
# Replace nan with zero then compute a cumulative sum
cumul_antennas = antennas.groupby(['month','emr_lb_systeme']).size().unstack().fillna(0).cumsum()
cumul_band = antennas.groupby(['month','freq_band']).size().unstack().fillna(0).cumsum()
perc_antennas = cumul_antennas.div(cumul_antennas.sum(axis=1), axis=0)
perc_band = cumul_band.div(cumul_band.sum(axis=1), axis=0)

n=10
fig, ax = plt.subplots()
cumul_antennas.plot(kind='bar',stacked=True, ax=ax)
ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::n])
ax.xaxis.set_ticklabels(ticklabels[::n])
ax.set_xlabel("Date of deployment")
ax.set_ylabel("Cumulated number of antennas")
plt.legend(bbox_to_anchor=(1.3, 1.0), loc='upper right')
#plt.tight_layout()
ax.get_legend().set_title('Frequency band')
fig.savefig('./output/cum_antenna_evo.pdf', format='pdf', bbox_inches='tight')

fig, ax = plt.subplots()
perc_antennas.plot(kind='bar',stacked=True, ax=ax)
ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::n])
ax.xaxis.set_ticklabels(ticklabels[::n])
ax.set_xlabel("Date of deployment")
ax.set_ylabel("Percentage of antennas")
plt.xticks(rotation=90)
plt.legend(bbox_to_anchor=(1.3, 1.0), loc='upper right')
#plt.tight_layout()
ax.get_legend().set_title('Frequency band')
fig.savefig('./output/perc_antenna_evo.pdf', format='pdf', bbox_inches='tight')

fig, ax = plt.subplots()
perc_band.plot(kind='bar',stacked=True, ax=ax)
ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::n])
ax.xaxis.set_ticklabels(ticklabels[::n])
ax.set_xlabel("Date of deployment")
ax.set_ylabel("Percentage of antennas")
plt.legend(bbox_to_anchor=(1.3, 1.0), loc='upper right')
#plt.tight_layout()
ax.get_legend().set_title('Frequency band')
fig.savefig('./output/perc_band_evo.pdf', format='pdf', bbox_inches='tight')