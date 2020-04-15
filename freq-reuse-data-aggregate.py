# Data is obtained by anfr and cartoradio
# Adapted for cities with mutiple postal codes
import sys
import pandas as pd
import numpy as np
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
# set gives unique values
antennas = antennas[antennas.sup_id.isin(set(support_id.values))]

# Get frequency bands
# Remove french accents and spaces from column names
freq_bands = pd.read_csv(base_folder+'cartoradio-rennes/Antennes_Emetteurs_Bandes_Cartoradio.csv', sep=';')
freq_bands = freq_bands[freq_bands.Numero_de_support.isin(set(antennas.sup_id.values))]
freq_bands = freq_bands[freq_bands.Systeme.isin(set(antennas.emr_lb_systeme))]

freq_range = np.arange(min(freq_bands.Debut),max(freq_bands.Fin), 0.1)
freq_df = pd.DataFrame(index=freq_range)
freq_df['freq_use'] = 0

for index, row in freq_bands.iterrows():
    freq_df.loc[row['Debut']:row['Fin'], :] +=1

n=500
fig, ax = plt.subplots()
freq_df.plot(kind='bar', ax=ax)
ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::n])
ax.xaxis.set_ticklabels(ticklabels[::n])
ax.set_xlabel("Frequency band")
ax.set_ylabel("Number of antennas")
plt.tight_layout()
fig.savefig('./output/freq_reuse.pdf', format='pdf', bbox_inches='tight')