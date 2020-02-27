# %% import
import numpy as np
import pandas as pd

# %% read csv using pandas
accounts = pd.read_csv("BotScore73KUsers.csv")
print (len(accounts))

# %% read sample tweets
tweets_s = pd.read_csv('sample_tweets.csv')

# %% select user from the sample tweets
users_s = set(tweets_s.screenName)
accounts_s = accounts[accounts.user.isin(users_s)]

len (accounts_s)  # 11699

# %% 0.75 & 0.90 quantiles score
q1, q2, q3 = accounts.prob.quantile([0.5, 0.75, 0.90])
print (q1, q2, q3)  # (0.25, 0.33, 0.4)

# %%
accounts_s.to_csv('sample_accounts.csv')

# %%
