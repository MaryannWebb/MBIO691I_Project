# Packages for general data manipulation and plotting
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#Read in coral forecast data
raw = pd.read_csv('../datasets/coral_forecast.csv', skiprows=1, header=0,
                  names=['coral_cover_2020', 'coral_cover_2100', 'SST_2020', 'SST_2100', 'SST_seasonal', 
                         'pH_2020', 'pH_2100', 'PAR', 'longitude', 'latitude', 'model'])
#create a copy of the raw data that we can manipulate but easily reset
df1 = raw.copy()

#CALCULATING PERCENT CHANGE IN CORAL COVER
    #Most of the questions have to do with percent change in cover between 2020 and 2100
df1['coral_cover_2020'] = pd.to_numeric(df1['coral_cover_2020'], errors='coerce') #making sure there are no sneaking NAs
df1['coral_cover_2100'] = pd.to_numeric(df1['coral_cover_2100'], errors='coerce')
        #percent change = ((new-old)/(old))*100
df1['coral_change_percent'] = ((df1['coral_cover_2100'] - df1['coral_cover_2020']) / df1['coral_cover_2020']) * 100
     #for some god forsaken reason some of these numbers are in the thousands. Yet the majority of them seem to have worked...
        #I have no idea what's going on. I've tried reading in my code again, multiple ways of calculating percent cover, 
        #checking to see if there is a pattern (e.g. maybe sneaky NAs) in one of the og coral cover columns - but I am truly 
        #stummped why the calculations by hand work but when I apply it to the whole column certain rows just go bananas. 
        #so for now I'm just going to exclude those rows that have an absolute value percent change in cover over 100
#remove psycho numbers 
df1 = df1.loc[(df1['coral_change_percent'] >= -100) & (df1['coral_change_percent'] <= 100)]

##################################
#       FIGURE 1: Predictors    #
##################################

#Check out how the model compare to one another in terms of their 2100 predictors. How do they vary? Is one more intense than another?
#Make two plots showing relationship between percent change and SST 2100 predictions and pH 2100 predictions
fig1 = plt.figure()
 #make room for caption
ax1 = fig1.add_subplot(2, 1, 1)
ax1 = sns.violinplot(data=df1, x='model', y='SST_2100', 
                        hue='model',legend=False, edgecolor='none')
plt.xlabel("Model")
plt.ylabel("Predicted SST (C)")
#plt.title("Predicted Sea Surface Temperatures and pH in 2100")

ax2 = fig1.add_subplot(2, 1, 2)
ax2 = sns.violinplot(data=df1, x='model', y='pH_2100', 
                        hue='model',legend=False, edgecolor='none')
ax2.set_ylim(7.8,8.1)
plt.xlabel("Model")
plt.ylabel("Predicted pH")

#based on these violin plots the final 2100 values are all pretty similar. 
    # Must be the way it tracks over the years that makes the models different but we don't have that dat
#fig1.subplots_adjust(bottom=0.4) #make room for caption
fig1.text(0.5, -1, 'Figure 1: Violin plots of pH and Sea Surface Temperature (SST, C) as predicted by the different models. Colors correspond with model numbers on the x axis for visual clarity. It appears that all 12 models ended with similar pH and temperatures in 2100. It is likely the difference in the models stems from how they got to these values, rather than the final pH and temperature themselves, but we do not have that detailed data.',
     ha='center', wrap=True, fontsize = 9)
plt.savefig("SST_pH.png",dpi=300)
fig1.clear()

#**************FIX FIGURE CAPTION^^^**********************

###################################
#      FIGURE 2: Latitude          #
####################################

#getting mean percent cover for each geographic coordinate (https://stackoverflow.com/questions/75480113/python-using-pandas-to-take-average-of-same-lon-lat-value-pairs)
lat_tup = (df1['latitude'])
lon_tup = (df1['longitude'])
cover_tup = (df1['coral_change_percent'])

df2_work = {
    'lat': lat_tup,
    'lon': lon_tup,
    'cover': cover_tup
}
df2 = pd.DataFrame(df2_work)

# group by pairs of latitude and longitude and calculate the mean cover value for each pair
df2_groups = df2.groupby([df2['lat'], df2['lon']])['cover'].mean().reset_index()
df2_groups.columns = ['lat', 'lon', 'cover']

# print the resulting dataframe
print(df2_groups)


#A plot showing the predicted percentage change in coral cover over the 21st century (averaged across simulations) as a function of latitude.
#fig2, ax3 = plt.subplots()
fig2 = plt.figure()
ax3 = sns.color_palette("rocket_r", as_cmap=True)
ax3 = sns.scatterplot(data=df2_groups, x='lat', y='cover', hue='cover',legend=False, palette = "rocket_r", edgecolor='none')
ax3.set_xlim(-40,40)
plt.axhline(y=0, color='black', linestyle='--') #shows zero change in coral cover
plt.xlabel("Latitude")
plt.ylabel("Percent Change of Coral Cover")
#plt.title("Spatial Change in Coral Cover 2020-2100")
fig2.text(0.5,0.5, 'Figure 2: Compares the predicted percent change of coral cover (averaged across models) with latitude. The horizontal line at zero is where there was is no predicted change in coral cover, generally around 30 degrees latitude. Closer to the equator we see high loses of coral cover (negative percentages).',
     ha='center', wrap=True, fontsize = 9)
plt.savefig("lat_coral",dpi=300)
fig2.clear()


##################################
#        FIGURE 3: MAP           #
##################################

#Figure 3: A map showing the predicted percentage change in coral cover over the 21st century, averaged across simulations.
#plotting (from cartopy)
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import Gridliner
import cartopy.feature as cfeature
from matplotlib.gridspec import GridSpec

fig3 = plt.figure()
ax4 = fig3.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax4.set_extent([-180, 180, -50, 50], crs=ccrs.PlateCarree(central_longitude=-157))
ax4.coastlines('110m')
scatter_4 = ax4.scatter(df2_groups['lon'], df2_groups['lat'], c=df2_groups['cover'],cmap = 'viridis', 
            transform=ccrs.PlateCarree(), marker="x")
#color bar
cbar = fig3.colorbar(scatter_4, orientation='horizontal')
cbar.set_label('Percent change coral cover')
#axis ticks and labels 
gl = ax4.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='gray', alpha=0.5, linestyle='--')
gl.left_labels = False
gl.xlines = False
gl.top_labels = False
gl.ylocator = mticker.FixedLocator([-30, 0, 30])
gl.ylabel_style = {'size': 10, 'color': 'black'}

fig3.text(0.5,0.5, 'Figure 3: Map depicting what percent change in coral cover is expected between 30 degrees South and North of the equator. Dark purple represents a loss of 100% coral cover. Yellow means a gain in coral cover, while teal shows areas with zero predicted change in cover.',
     ha='center', wrap=True, fontsize = 9)
plt.savefig("map",dpi=300)

# Clear the current figure
plt.clf()  # Clears the current figure
plt.cla()  # Clears the current axes
plt.close()  # Closes the current figure window


