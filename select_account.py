'''
Select accounts

1. read original user account file
2. read sampled tweets
3. sample user accounts included in the tweets sample ('user' and 'screenNAme' columns)
4. calculate the mean, Q3, 0.85 quantiles value of the botness score ('prob' column)
5. save sample accounts

'''

# %% import
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% read csv using pandas
accounts = pd.read_csv("data/BotScore73KUsers.csv")
print (len(accounts))

# %% plot prob
sns.boxplot(accounts.prob)
plt.xlabel('botness score')
plt.savefig('output/boxplot_all_aacounts_prob.png')

# %% read sample tweets
import global_variables as gv
tweets_s = pd.read_csv(gv.fname_sample_tweets)

# %% select user accounts from the sample tweets
users_s = set(tweets_s.screenName)
accounts_s = accounts[accounts.user.isin(users_s)]

len (accounts_s)
'''
11699
'''

# %% 0.75 & 0.90 quantiles score
q1, q2, q3 = accounts.prob.quantile([0.5, 0.75, 0.85])
print (q1, q2, q3)  
'''
(0.25, 0.33, 0.37)
'''

# %% write sample users to file
accounts_s.to_csv(gv.fname_sample_accounts_old)
