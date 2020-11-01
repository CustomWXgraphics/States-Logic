#Import modules for data analysis, and plotting
import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import geopandas
import numpy as np
import numpy as np

#Blank Dictionary to be used later
dict = {}

#If True, only counties with be plotted with selected state
Select_State_County = True

#Select State to Zoom to
State = "NJ"

#Select Distance from states (0=close, 100=far)
distance=25


#Open County and States shapefiles from directory [THESE ARE IN THE GITHUB DIRECTORY]
states_shapefile = geopandas.read_file("cb_2018_us_state_5m.shp")
counties_shapefile = geopandas.read_file("cb_2018_us_county_5m.shp")


#Associate State (key) w/ Abbreviation (value) ("North Caroline" = "NC") into dictionary
dict = pd.Series(states_shapefile["STATEFP"].values, index=states_shapefile["STUSPS"]).to_dict()

#If the State you selected is a correct State, assign it to variable (chosen_state)
for key, value in dict.items():
    if key == State:
        chosen_state = value

#Only plot the counties within your chosen state
if Select_State_County == True:
    county_geometries = counties_shapefile[counties_shapefile['STATEFP'] == str(chosen_state)]

#Selected only the state we can center
selected_state_geometries = states_shapefile[states_shapefile['STATEFP'] == str(chosen_state)]

#Find Maximum extent value 
south = selected_state_geometries.bounds.miny
north = selected_state_geometries.bounds.maxy
west = selected_state_geometries.bounds.minx
east =  selected_state_geometries.bounds.maxx

#Center longitude and Latitude by finding the average
lon1 = float(east)+float(west)
lat1 = float(north)+float(south)

#Define the global projection
proj = ccrs.Orthographic(
    central_longitude = (lon1/2),
    central_latitude =  (lat1/2)
)

#Plot blank figure
fig = plt.figure(figsize=(16,12))
ax = fig.add_subplot(1,1,1, projection=proj)

#Define the distance between North and South
ne = float(north-south)
we = float(east-west)

bvalue = []
avalue = []

#Select x, y box ratio
x_ratio = 7.45
y_ratio = 14

#Loop through all valid 
if float(lat1/2) > 39:
    for i in range(1,200):
        a = x_ratio*(i/100)
        b = y_ratio*(i/100)
        if b > we and a > ne:
            avalue.append(a)
            bvalue.append(b)

    b = bvalue[0+distance]
    a = avalue[0+distance]

    ne = (a - ne)/2
    we = (b - we)/2
    
else:
    for i in range(1,200):
        a = 7.45*(i/100)
        b = 13.333*(i/100)
        if b > we and a > ne:
            avalue.append(a)
            bvalue.append(b)

    b = bvalue[0+distance]
    a = avalue[0+distance]

    ne = (a - ne)/2
    we = (b - we)/2


south = south - ne
north = north + ne
east = east + we
west = west - we 



ax.set_extent([west,east,north,south])

ax.add_geometries(states_shapefile["geometry"], crs=ccrs.PlateCarree(), linewidth=0.5, zorder=7,facecolor="none", edgecolor="black")
if Select_State_County == True:
    ax.add_geometries(county_geometries["geometry"], crs=ccrs.PlateCarree(), edgecolor="black", facecolor="none", linewidth=0.1,zorder=59)
if Select_State_County == False:
    ax.add_geometries(counties_shapefile["geometry"], crs=ccrs.PlateCarree(), edgecolor="black", facecolor="none", linewidth=0.05,zorder=59)

aspect = sum(np.abs(ax.get_xlim())) / sum(np.abs(ax.get_ylim()))
y = sum(np.abs(ax.get_ylim()))/100000
x = sum(np.abs(ax.get_xlim()))/100000

exa = (a-y)/2
exb = (b-x)/2

south = south
north = north
east = east + exb - (exa*2)
west = west - exb + (exa*2)

ax.set_extent([west,east,north,south])

plt.show()
