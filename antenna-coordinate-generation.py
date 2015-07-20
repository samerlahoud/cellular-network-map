#!/usr/bin/python
###########################################
#Samer Lahoud 2015 (samer AT LAHOUD DOT FR)
###########################################
#http://www.antennesmobiles.fr/index.php?sfr=0&free=0&bouygues=0&cp=rennes&2g=0&3g=0&show

import math
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import sys

# Declaring constants for coordinate computations
NMI = 1852.0
D2R = math.pi/180

city_code = sys.argv[1]
operator_name = sys.argv[2]
network_type = sys.argv[3]

# Testing the arguments
if operator_name not in ['orange', 'bouygues', 'free', 'sfr']:
	print "valid operator names: orange, bouygues, free, sfr" 
	print "syntax: python antenna-coordinate-generation.py city_code operator_name network_type"
	quit()

if network_type not in ['2G', '3G', '4G']:
	print "valid network types: 2G, 3G, 4G"
	print "syntax: python antenna-coordinate-generation.py city_code operator_name network_type"
	quit()

if operator_name =='orange':
	operator_name = 'ORANGE'
elif operator_name =='free':
	operator_name = 'FREE MOBILE'
elif operator_name =='bouygues':
	operator_name = 'BOUYGUES TELECOM'
elif operator_name =='sfr':
	operator_name = 'SFR'
	
antenna_carteradio_id=[]
antenna_support_nb=[]

# Get the antenna from the network map downloaded from www.antennesmobiles.fr
with open('./data/network-map-%s.txt' %(city_code),'r') as antenna_db:
	for line in antenna_db:
		if not line.startswith('#'):
			w=line.split(';')
			if network_type in w[1] and operator_name in w[2] and city_code in w[6]:
				antenna_carteradio_id.append(w[0])

# Copy the id list in a temporary list
tmp_id_list = list(antenna_carteradio_id)

# Get the equivalence between carte radio id and antenna support number (from www.cartoradio.fr)
# Modify filename if necessary
with open('./data/cartoradio-%s/Antennes_Emetteurs_Bandes_Cartoradio.csv' %city_code,'r') as conversion_db:
	for line in conversion_db:
		if line[0].isdigit:
			w=line.split(';')
			if w[1] in tmp_id_list:
				antenna_support_nb.append(w[0])
				# Remove converted antenna id from temporary list
				tmp_id_list.remove(w[1])

# Get coordinates for each antenna given its support number
# Modify filename if necessary
long=[]
lat=[]
with open('./data/cartoradio-%s/Supports_Cartoradio.csv' %city_code,'r') as coordinate_db:
	for line in coordinate_db:
		if line[0].isdigit:
			w=line.split(';')
			if w[0] in antenna_support_nb:
				long.append(float(w[1]))
				lat.append(float(w[2]))			

# Convert longitude and latitude into plain coordinates
p_long = [(long[t] - min(long))*60*NMI*math.cos(D2R*lat[t]) for t in range(len(long))]
p_lat = [(t - min(lat))*60*NMI for t in lat]
antenna_locations = [[i,j] for (i,j) in zip(p_long,p_lat)]

output_file = open('./output/%s_%s_%s_antenna_coordinates.m' %(city_code, operator_name, network_type), 'w')
for c in range(len(p_long)):
	output_file.write('antenna_long({}) = {}\n'.format(c+1, p_long[c]))
	output_file.write('antenna_lat({}) = {}\n'.format(c+1, p_lat[c]))

# Output some eye candies
fig = plt.gcf()
plt.title('%s %s antenna map - %s - France\n %d antennas' %(operator_name, network_type, city_code, len(long)))
plt.plot(p_long,p_lat,'x')
plt.xlabel('Distance (m)')
plt.ylabel('Distance (m)')
fig.savefig('./output/%s-%s-%s-antenna-map.png' %(city_code, operator_name, network_type))			

fig = plt.gcf()
vor = Voronoi(antenna_locations)
voronoi_plot_2d(vor)
plt.xlabel('Distance (m)')
plt.ylabel('Distance (m)')
plt.title('%s %s Voronoi map - %s - France\n %d antennas' %(operator_name, network_type, city_code, len(long)))
plt.savefig('./output/%s-%s-%s-voronoi-map.png' %(city_code, operator_name, network_type))