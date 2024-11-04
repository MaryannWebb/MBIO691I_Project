# Packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Geospatial packages (Problem set 5)
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean as cmo
from matplotlib.gridspec import GridSpec


# Read in data
raw = pd.read_csv('../datasets/coral_forecast.csv', skiprows=1, header=0,
                  names=['coral_cover_2020', 'coral_cover_2100', 'SST_2020', 'SST_2100', 'SST_seasonal', 
                         'pH_2020', 'pH_2100', 'PAR', 'longitude', 'latitude', 'model'])

#data frame to manipulate
df1 = raw.copy()
#CALCULATING PERCENT CHANGE IN CORAL COVER
df1['coral_cover_2020'] = pd.to_numeric(df1['coral_cover_2020'], errors='coerce')
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
#        FIGURE 1: MAP           #
##################################

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

#plotting (from cartopy)
#ax1 = plt.axes(projection=ccrs.PlateCarree())
#ax1.coastlines()
#ax1.scatter(df2_groups['lon'], df2_groups['lat'], c=df2_groups['cover'], transform=ccrs.PlateCarree(),
        #alpha=0.1)

#need to do a few more things before ready 
        #make color scale more refined
        #create legend

###################################
#      FIGURE 2: pH               #
####################################
#A plot showing the predicted percentage change in coral cover over the 21st century (averaged across simulations) as a function of latitude.
fig, ax2 = plt.subplots()
sns.color_palette("rocket_r", as_cmap=True)
ax2 = sns.scatterplot(data=df2_groups, x='lat', y='cover', hue='cover',legend=False, palette = "rocket_r", edgecolor='none')
ax2.set_xlim(-40,40)
plt.axhline(y=0, color='black', linestyle='--')
plt.xlabel("Latitude")
plt.ylabel("Percent Change of Coral Cover")
plt.title("Spatial Change in Coral Cover 2020-2100")





###################################
#       FIGURE 3:FACET            #
###################################
#first make a column for the overall change in coral cover 
df3 = raw
df3['coral_change'] = (df3['coral_cover_2020'])-(df3['coral_cover_2100'])
#use groupby to aggregate by model
df3_model = df3[['coral_change','pH_2020',"pH_2100",'model','coral_cover_2020','coral_cover_2100','SST_2020','SST_2100']].groupby(df3['model'])
# Compute the mean
df3_change_mean = df3_model.mean().drop(columns='model')
df3_change_mean['model'] = ['0','1','2','3','4','5','6','7','8','9','10','11']

#make a new dataframe in better format for plotting
    #make a new dataframe to manipulate starting with the data from 2020
df_2020 = df3_change_mean[['coral_cover_2020','pH_2020','SST_2020','model']]
df_2020 = df_2020.rename(columns={"coral_cover_2020": "coral_cover","pH_2020":"pH","SST_2020":"SST"})

df_2100 = df3_change_mean[['coral_cover_2100','pH_2100','SST_2100','model']] #same thing for 2100
df_2100 = df_2100.rename(columns={"coral_cover_2100": "coral_cover","pH_2100":"pH","SST_2100":"SST"})
#combine 2020 and 2100 datasets on top of each other so year become its own column rather than separate cols
df3_join = pd.concat([df_2020, df_2100], axis=0)
#add year column (there's got to be a better way *fix if I have time)
df3_join['year'] = ['2020','2020','2020','2020','2020','2020','2020','2020','2020','2020','2020','2020',
                '2100','2100','2100','2100','2100','2100','2100','2100','2100','2100','2100','2100']


g = sns.FacetGrid(df3_join, col="year",hue="model",legend_out=True, palette="colorblind",height=3,aspect=.75)
g.map(sns.scatterplot, "pH", "coral_cover", alpha=.7)
g.set_titles(col_template="{col_name}")
g.add_legend(title="Simulation")
g.set_axis_labels(x_var="pH", y_var="Coral Cover (sq.km)", clear_inner=True)
sns.move_legend(g,"upper right")
