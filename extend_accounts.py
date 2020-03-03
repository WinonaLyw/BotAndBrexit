'''
Extend accounts

1. read sampled accounts and all extended tweets
2. calculate total number of tweets per aacounts ('total_tweet' column)
3. calculate total number of retweets per aacounts ('total_retweet' column)
4. calculate # of retweets/ # of tweets ('retweet_rate' column)
5. maxminum # of tweets within an hour ('max_tweet_hr' column)
6. average number of hashtags included in one tweet ('ave_hashtag' columns)
7. total number of different platform used ('platforms_used' columns), extract from 'statusSource' columns
8. most commonly use platform ('common_platform' columns)

'''

# %% imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import global_variables as gv

# %% 
accounts = pd.read_csv(gv.fname_sample_accounts_old, index_col=0)

tweets = pd.read_csv(gv.fname_extended_tweets)

tweets = tweets.fillna({'hashtags':''})
tweets['hashtags'] = [s.split(',') for s in tweets['hashtags']]

# %% 
# 1. total number of tweets in three month time
# 2. total reweet 
accounts['total_tweet'] = 0
accounts['total_retweet'] = 0
for i in accounts.index:
    t = tweets[tweets.screenName == accounts.loc[i, 'user']][['isRetweet', 'retweeted']]
    accounts.loc[i, 'total_tweet'] = len(t)
    l = t[t.isRetweet]
    accounts.loc[i, 'total_retweet'] = len(l)

accounts['retweet_rate'] = accounts.total_retweet/accounts.total_tweet

# %% maxinum number of tweets within an hour
accounts['max_tweets_hr'] = 0
for i in accounts.index:
    t = tweets[tweets.screenName == accounts.loc[i, 'user']][['timeslot','X']]
    mx = t.groupby('timeslot').count().max()['X']

    accounts.loc[i, 'max_tweets_hr'] = mx

# %% average No. of hashtags in a tweet
accounts['ave_hashtag'] = 0

for i in accounts.index:
    tag_list = tweets[tweets.screenName == accounts.loc[i, 'user']]['hashtags']
    n = len(tag_list)
    # stack_list =[item.split(',') for item in tag_list]
    flat_list = []
    for x in tag_list:
        if x is not None:
            flat_list.extend(x)
    accounts.loc[i, 'ave_hashtag'] = len(flat_list)/ n

# %% number of platforms used, and most commonly used platform
import re

def platform(df):
    platforms = []
    for t in df.itertuples():
        platforms.append(re.sub('<((?!>).)*>', '',t.statusSource))
    return platforms


accounts['platforms_used'] = 0
accounts['common_platform'] = ''

for i in accounts.index:
    t = tweets[tweets.screenName == accounts.loc[i, 'user']]
    p = platform(t)
    accounts.loc[i, 'platforms_used'] = len(set(p))
    accounts.loc[i, 'common_platform'] = max(set(p), key = p.count)

# %% assume accounts with bot score >= 0.85 quantiles as bots
accounts['b_1'] = accounts.apply(lambda row:(1 if row.prob >= gv.score_entropy else 0), axis=1)

# %%
accounts.to_csv(gv.fname_sample_accounts)