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
#calculate percent change in coral cover
df1['coral_change_percent'] = (
    (df1['coral_cover_2100'] - df1['coral_cover_2020']) / df1['coral_cover_2020']
) * 100

#Figure 1: A map showing the predicted percentage change in coral cover over the 21st century, averaged across simulations.       

#getting mean percent cover for each geographic coordinate (https://stackoverflow.com/questions/75480113/python-using-pandas-to-take-average-of-same-lon-lat-value-pairs)
lat_tup = (df1['latitude'])
lon_tup = (df1['longitude'])
cover_tup = (df1['coral_change_percent'])
data = {
    'lat': lat_tup,
    'lon': lon_tup,
    'cover': cover_tup
}
df = pd.DataFrame(data)

# group by pairs of latitude and longitude and calculate the mean spei value for each pair
df_groups = df.groupby([df['lat'], df['lon']])['cover'].mean().reset_index()
df_groups.columns = ['lat', 'lon', 'cover']

# print the resulting dataframe
print(df_groups)

#plotting (from problem set 5)

# Create a figure object and 2x1 GridSpec (main figure + colour bar)
f = plt.figure(constrained_layout=True, figsize=(8, 5)) # 8x5 figure
gs = GridSpec(2, 1, figure=f, height_ratios=[1, 0.03])  # Thin lower axis for colour bar

####################################################################
# TOP AXIS                                                         #
####################################################################

# Create top axis using the default Plate Carree projection.
ax1 = f.add_subplot(gs[0, 0], projection=ccrs.PlateCarree())

# Plot the chlorophyll concentration with pcolormesh
# Note: the transform kwarg sets the DATA coordinate reference system, whereas
#       the projection kwarg (when the axis is made, above) sets the FIGURE
#       (projected) coordinate system. The data are defined on a lon/lat grid,
#       so the data coordinate system is Plate Carree.
cover_map = ax1.pcolormesh(df_groups['lon'], df_groups['lat'], df_groups['cover'], transform=ccrs.PlateCarree())
