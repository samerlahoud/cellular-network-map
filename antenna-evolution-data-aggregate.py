# Data is obtained by anfr and cartoradio
# Adapted for cities with mutiple postal codes
import sys
import pandas as pd
import folium
from folium import plugins
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'CMU Serif'
plt.rcParams['axes.labelsize'] = 14
#plt.rcParams.update({'font.size': 12})

rennes_latitude = 48.114700
rennes_longitude = -1.679400
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
# Split location into longitude and latitude
antennas['location'] = antennas.coordonnees.str.split(",")

# Folium map
map_latest = folium.Map([rennes_latitude, rennes_longitude], zoom_start=13)
for loc in antennas['location']:
    folium.CircleMarker([loc[0],loc[1]],radius=5,fill_color="#3db7e4").add_to(map_latest)
map_latest.add_child(plugins.HeatMap(antennas['location'], radius=35))
map_latest.save('./output/antenna_map_latest.html')

# Select antennas before 2013
antennas_2013 = antennas[antennas.index < '2013-01-01']
map_2013 = folium.Map([rennes_latitude, rennes_longitude], zoom_start=13)
for loc in antennas_2013['location']:
    folium.CircleMarker([loc[0],loc[1]],radius=5,fill_color="#3db7e4").add_to(map_2013)
map_2013.add_child(plugins.HeatMap(antennas_2013['location'], radius=35))
map_2013.save('./output/antenna_map_2013.html')

# Group by month then by emr_lb_systeme (technology)
# Put in a a matrix (month, emr_lb_systeme) with unstack 
# Replace nan with zero then compute a cumulative sum
cumul_antennas = antennas.groupby(['month','emr_lb_systeme']).size().unstack().fillna(0).cumsum()
cumul_band = antennas.groupby(['month','freq_band']).size().unstack().fillna(0).cumsum()
perc_antennas = cumul_antennas.div(cumul_antennas.sum(axis=1), axis=0)
sorted_perc_antennas = perc_antennas[['GSM 1800', 'LTE 1800', 'UMTS 2100', 'LTE 2100', 'LTE 2600', 'LTE 700', 'LTE 800', 'GSM 900', 'UMTS 900']]
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
ax.legend(bbox_to_anchor=(1.3, 1.0), loc='upper right')
ax.get_legend().set_title('Mobile Technology')
fig.savefig('./output/cum_antenna_evo.pdf', format='pdf', bbox_inches='tight')

fig, ax = plt.subplots()
color_list = ['red', 'darkred', 'blue', 'darkblue', 'violet', 'orange', 'grey', 'green', 'darkgreen']
sorted_perc_antennas.plot(kind='bar',stacked=True, ax=ax, color=color_list)
ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::n])
ax.xaxis.set_ticklabels(ticklabels[::n])
ax.set_xlabel("Date of deployment")
ax.set_ylabel("Percentage of antennas")
ax.xaxis.set_tick_params(rotation=90)
#ax.legend(bbox_to_anchor=(1.3, 1.0), loc='upper right', title='Mobile Technology')
ax.legend(loc='upper left')
fig.savefig('./output/perc_antenna_evo.pdf', format='pdf', bbox_inches='tight')

fig, ax = plt.subplots()
color_list = ['red', 'blue', 'violet', 'orange', 'grey', 'green']
perc_band.plot(kind='bar',stacked=True, ax=ax, color=color_list)
ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::n])
ax.xaxis.set_ticklabels(ticklabels[::n])
ax.set_xlabel("Date of deployment")
ax.set_ylabel("Percentage of antennas")
handles, labels = ax.get_legend_handles_labels()
labels = [l+' MHz' for l in labels]
# Sorting legend labels
#labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: int(t[0])))
#ax.legend(handles, labels, bbox_to_anchor=(1.3, 1.0), loc='upper right', \
#    mode='expand', title='Frequency Band')
ax.legend(handles, labels, loc='upper left')
fig.savefig('./output/perc_band_evo.pdf', format='pdf', bbox_inches='tight')