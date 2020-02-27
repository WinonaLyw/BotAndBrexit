# %% import
import numpy as np
import pandas as pd
from nltk.tokenize import TweetTokenizer

# %% read tweets
tweets = pd.read_csv("Tweets1.267Million.csv" , encoding='latin-1')
tweets.head(4)

# %% read terget accounts
human = pd.read_csv("human_accounts.csv")
bots = pd.read_csv("bots_accounts.csv")

# %% concatenate two account dataframes
accounts = pd.concat([human, bots], ignore_index=True)

accounts.head(2)
# %% select tweets tweeted by sample accounts
acc_tweets = tweets[tweets['screenName'].isin(accounts.user)]
print (len(acc_tweets))

# %%
tkznr = TweetTokenizer()
acc_tweets['text_token'] = acc_tweets.apply(lambda row: tknzr.tokenize(row['text']), axis=1)
acc_tweets.head(4)

# %%
acc_tweets.to_csv("sample_tweets.csv")

# %%
