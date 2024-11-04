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
fig1.text(0.5, 1, 'Figure 1: Violin plots of pH and Sea Surface Temperature (SST, C) as predicted by the different models. Colors correspond with model numbers on the x axis for visual clarity. It appears that all 12 models ended with similar pH and temperatures in 2100. It is likely the difference in the models stems from how they got to these values, rather than the final pH and temperature themselves, but we do not have that detailed data.',
     ha='center', wrap=True, fontsize = 9)
plt.savefig("SST_pH.png",dpi=300)

#**************FIX FIGURE CAPTION^^^**********************
