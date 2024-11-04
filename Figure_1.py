#Packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
#geospatial packages (Problem set 5)
import matplotlib.ticker as mticker 
import cartopy.crs as ccrs 
import cartopy.feature as cfeature 
import cmocean as cmo 
from matplotlib.gridspec import GridSpec 


#Read in data
raw = pd.read_csv('../datasets/coral_forecast.csv', skiprows=1, header=0, 
        names=['coral_cover_2020', 'coral_cover_2100','SST_2020','SST_2100','SST_seaonal','pH_2020','pH_2100','PAR','longitude','latitude','model'])

#Create dataset to manipulate
df1 = raw


##################################
#        FIGURE 1: MAP           #
##################################

#calculate percent change in coral cover
df1['coral_change_percent'] = (
    (df1['coral_cover_2100'] - df1['coral_cover_2020']) / df1['coral_cover_2020']
) * 100

#Figure 1: A map showing the predicted percentage change in coral cover over the 21st century, averaged across simulations.       

#getting mean percent cover for each geographic coordinate (https://stackoverflow.com/questions/75480113/python-using-pandas-to-take-average-of-same-lon-lat-value-pairs)
lat_tup = (df1['latitude'])
lon_tup = (df1['longitude'])
cover_tup = (df1['coral_change_percent'])
lat_lon_cov = {
    'lat': lat_tup,
    'lon': lon_tup,
    'cover': cover_tup
}
df2 = pd.DataFrame(lat_lon_cov)

# group by pairs of latitude and longitude and calculate the mean cover value for each pair
df2_groups = df2.groupby([df2['lat'], df2['lon']])['cover'].mean().reset_index()
df2_groups.columns = ['lat', 'lon', 'cover']

# print the resulting dataframe
print(df2_groups)

#plotting (from problem set 5)
ax1 = plt.axes(projection=ccrs.PlateCarree())
ax1.coastlines()
ax1.scatter(df2_groups['lon'], df2_groups['lat'], c=df2_groups['cover'], transform=ccrs.PlateCarree(),
        alpha=0.1)
#ax1.set_extent([-180, 180,-40,40])

#need to do a few more things before ready 
        #make color scale more refined
        #try and focus map on central 30- -30 lat area
        #create legend

###################################
#      FIGURE 2: pH               #
####################################
