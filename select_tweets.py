# %% import
import numpy as np
import pandas as pd
import matplotlib.plot as plt

# %% read tweets
tweets = pd.read_csv("Tweets1.267Million.csv" , encoding='latin-1')

tweets.head(4)

# tweets.statusSource[0:7]

# %% daily tweets count
# split date from created time
tweets['created_date'] = [t.split(' ')[0] for t in tweets.created]

# groupby date to get daily tweets count from 1 Jan to 31 Mar 2018
d_counts = tweets[['created_date', 'created']].groupby('created_date').count()

# list top 10 
d_counts.nlargest(10, 'created')

# %% plot daily tweets count
plt.plot(d_counts.index, d_counts['created'])
plt.title('No. of #Brexit tweets per day from 1 Jan to 31 Mar, 2018')
plt.xlabel('date')
plt.legend(labels=['tweet count'])
plt.xlim(0, len(d_counts)-1)
plt.xticks([0, 14, 31, 45, 59, 73, 89], rotation=20)
plt.savefig('daily_dist.png')


# %% daily difference
# calculate daily difference comparing the previous day
d_counts['moving_diff'] = 0.0

dates = d_counts.index

for i in range(1, len(dates)):
    d = dates[i]
    prev_d = dates[i-1]
    d_counts.loc[d, 'moving_diff'] = d_counts.loc[d]['created'] - d_counts.loc[prev_d]['created']
    # d_counts.loc[d, 'moving_diff'] = (d_counts.loc[d]['created'] - d_counts.loc[prev_d]['created']) / d_counts.loc[prev_d]['created'] * 100

# list top 10 / least 10 (increase/decrease the most)
d_counts.nlargest(10, 'moving_diff')
d_counts.nsmallest(10, 'moving_diff')

# %% plot daily tweets count
plt.plot(d_counts.index, d_counts['moving_diff'])
plt.title('Difference of #Brexit tweets to previous day from 1 Jan to 31 Mar, 2018')
plt.xlabel('date')
plt.legend(labels=['tweet count difference'])
plt.xlim(0, len(d_counts)-1)
plt.xticks([0, 14, 31, 45, 59, 73, 89], rotation=20)
plt.savefig('daily_diff_dist.png')

# ================================
# 2018-03-29 
# 1. top 10 tweets
# 2. top 10 increase
# 3. top 10 decrease in 2018-03-30
# ================================

# %%
tweets_s = tweets[tweets.created_date == '2018-03-29']
tweets_s.to_csv('sample_tweets.csv')

