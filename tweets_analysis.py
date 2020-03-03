'''
Tweets analysis
To get some overall idea of the hashtag network
'''

# %% import
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from pandas.plotting import table
import nltk
from nltk.probability import FreqDist

import global_variables as gv

# %% read sample tweets and accounts
tweets_s = pd.read_csv(gv.fname_sample_tweets, engine='python', index_col=0)

tweets_s = tweets_s.fillna({'hashtags':''})
tweets_s['hashtags'] = [str(s).split(',') for s in tweets_s['hashtags']]

accounts = pd.read_csv(gv.fname_sample_accounts, index_col=0)

# %% plot hourly dist
hourly_dist = tweets_s[['hour', 'created']].groupby('hour').count()
hourly_dist.plot()
plt.title('No. of #Brexit tweets per hour on 29 Mar, 2018')
plt.legend(labels=['tweet count'])
plt.savefig('output/hourly_dist.png')

# %% tweets per account 
acc_dist = tweets_s[['screenName', 'created']].groupby('screenName').count()
acc_dist.nlargest(10, 'created')

acc_dist.nlargest(10, 'created').join(accounts[['user', 'prob', 'b_2']].set_index(['user']), on='screenName')
'''
                created	prob	b_2
screenName			
brexit_politics	76	0.780000	1
SandraDunn1955	68	0.400000	1
SafariSara  	61	0.360000	0
lunaperla	    59	0.340000	1
curiocat13	    55	0.450000	1
catherinemginn	54	0.380552	1
Iloveautumn2	52	0.410000	1
RLH_Initials	52	0.380000	1
BJ_Gardener	    50	0.310000	1
HelenMagi	    46	0.320000	0
'''

# %% hourly tweets per account
acc_hourly_dist = acc_dist.reset_index()
acc_hourly_dist = acc_hourly_dist.rename(columns={'created':'total'})
hour_l = list(hourly_dist.index)

for h in hour_l:
    h_s = tweets_s[tweets_s.hour == h]
    acc_hourly_dist[h] = [len(h_s[h_s.screenName == n]) for n in acc_hourly_dist.screenName]

# %% describe table
desc = acc_hourly_dist.describe().round(1)

plt.figure(figsize=(20,2.5))
#create a subplot without frame
plot = plt.subplot(111, frame_on=False)

#remove axis
plot.xaxis.set_visible(False) 
plot.yaxis.set_visible(False) 

#create the table plot and position it in the upper left corner
table(plot, desc,loc='upper right')

#save the plot as a png file
plt.savefig('output/acc_hourly_desc_table.png')

# %% plot histogram
acc_hourly_dist.hist(figsize=(20,20))
plt.savefig('output/hist_acc_hourly.png')

# %% select active account
active_acc_h = acc_hourly_dist[acc_hourly_dist.total > 2]
hours=active_acc_h.columns[2:]

plt.figure(figsize=(10,5))
for row in active_acc_h.loc[:, hours].itertuples():
    # print (row)
    plt.plot(hours,row[1:])
plt.xlim(0,23)
# plt.show()
plt.savefig('output/hourly_active.png')

# %% tweet frequency distribution
fdist = nltk.FreqDist(tweets_s['text'])
tweets_dist = pd.DataFrame.from_dict(fdist, orient='index')
tweets_dist.columns = ['Frequency']
tweets_dist.index.name = 'Text'
tweets_dist.reset_index()

# %%
