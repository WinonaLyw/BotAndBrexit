'''
Select tweets

1. read tweets
2. sum the total tweets per day
3. calculate the moving difference of total tweets for each day
4. selext tweets for a specific day as sample
5. save file

'''

# %% import
import numpy as np
import pandas as pd
import matplotlib.plot as plt

import global_variables as gv

# %% read tweets
tweets = pd.read_csv(gv.fname_extended_tweets , encoding='latin-1', index_col=0)

tweets.head(4)

# %% daily tweets count
# groupby date to get daily tweets count from 1 Jan to 31 Mar 2018
d_counts = tweets[['created_date', 'created']].groupby('created_date').count()

# list top 10 
d_counts.nlargest(10, 'created')

'''
created_date created     	
2018-03-29	 26327
2018-03-25	 24915
2018-02-28	 24506
2018-03-02	 23907
2018-03-23 	 23678
2018-03-20	 23567
2018-03-19	 22731
2018-03-24	 22338
2018-01-30	 20941
2018-03-09	 20835
'''

# %% plot daily tweets count
plt.plot(d_counts.index, d_counts['created'])
plt.title('No. of #Brexit tweets per day from 1 Jan to 31 Mar, 2018')
plt.xlabel('date')
plt.legend(labels=['tweet count'])
plt.xlim(0, len(d_counts)-1)
plt.xticks([0, 14, 31, 45, 59, 73, 89], rotation=20)
plt.savefig('output/daily_dist.png')


# %% daily difference
# calculate daily difference comparing the previous day
d_counts['moving_diff'] = 0.0

dates = d_counts.index

for i in range(1, len(dates)):
    d = dates[i]
    prev_d = dates[i-1]
    d_counts.loc[d, 'moving_diff'] = d_counts.loc[d]['created'] - d_counts.loc[prev_d]['created']
    
# list top 10 / least 10 (increase/decrease the most)
d_counts.nlargest(10, 'moving_diff')
'''	
            created	moving_diff
created_date		
2018-03-19	22731	8192.0
2018-02-14	19079	7939.0
2018-02-28	24506	7509.0
2018-03-29	26327	7382.0
2018-01-16	17750	6865.0
2018-01-30	20941	6436.0
2018-02-26	17238	4829.0
2018-01-11	15205	4599.0
2018-03-08	20087	4585.0
2018-03-23	23678	4559.0

'''

d_counts.nsmallest(10, 'moving_diff')
'''
	        created	moving_diff
created_date		
2018-03-30	15495	-10832.0
2018-03-03	15572	-8335.0
2018-02-15	11720	-7359.0
2018-01-31	13638	-7303.0
2018-03-26	18053	-6862.0
2018-01-17	11196	-6554.0
2018-01-12	9982	-5223.0
2018-03-01	19663	-4843.0
2018-03-10	16447	-4388.0
2018-01-05	7055	-3775.0
'''

# %% plot daily tweets count
plt.plot(d_counts.index, d_counts['moving_diff'])
plt.title('Difference of #Brexit tweets to previous day from 1 Jan to 31 Mar, 2018')
plt.xlabel('date')
plt.legend(labels=['tweet count difference'])
plt.xlim(0, len(d_counts)-1)
plt.xticks([0, 14, 31, 45, 59, 73, 89], rotation=20)
plt.savefig('output/daily_diff_dist.png')

'''
2018-03-29 
1. top 10 tweets
2. top 10 increase 
3. top 10 decrease in 2018-03-30
'''

# %% select tweets data for 29 Mar 2018 as sample
# selected_date = '2018-03-29'

tweets_s = tweets[tweets.created_date == gv.selected_date]
tweets_s.to_csv(gv.fname_sample_tweets)

