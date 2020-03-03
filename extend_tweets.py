'''
Extend tweets

1. read orignal tweets data
2. split tweet created time string ('created' columns) into date and hour string ('created date' and 'hour' columns)
3. encode tweet created time ('created' columns) into 'timeslot' for easier selection.
timeslot is the time offset to the start time of tweets data (01 Jan 2018 00:00) in unit of hour
4. extract hashtags used in each tweets ('hashtags' column)
5. save to csv file

'''
# %%
import numpy as np
import pandas as pd
import re

import nltk
from nltk.probability import FreqDist
from nltk.tokenize import TweetTokenizer

# %% read tweets file
tweets = pd.read_csv("data/Tweets1.267Million.csv", engine='python', index_col=0)

tweets.head(4)

# %% timeslot(unit:hour) of each tweet
# split date and hour from tweet created time
tweets['created_date'] = [t.split(' ')[0] for t in tweets.created]
tweets['hour'] = [re.split('[ :]', t)[1] for t in tweets.created]

# timeslot is the hour time since 01 Jan 2018 0a.m
day_list = list(set(tweets['created_date']))
day_list.sort()

hour_list = list(set(tweets['hour']))
hour_list.sort()

tweets['timeslot'] = tweets.apply(lambda row: (day_list.index(row.created_date) * 24 + hour_list.index(row.hour)), axis=1)

# %% hashtags in each tweet
tknzr = TweetTokenizer()
tweets['text_token'] = tweets.apply(lambda row: tknzr.tokenize(row['text']), axis=1)
r = re.compile('^#.+')
tweets['hashtags'] = tweets.apply(lambda row: ','.join(string for string in list(filter(r.match, row['text_token']))), axis=1)

tweets = tweets.drop('text_token', axis=1)

# %% save
import global_variables as gv
tweets.to_csv(gv.fname_extended_tweets)
