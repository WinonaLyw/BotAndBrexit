# %% import
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from nltk.tokenize import TweetTokenizer

# %% read sample tweets
tweets_s = pd.read_csv("sample_twwets.csv")
tweets_s.head(4)

# %% hourly tweets count
tweets_s['hour'] = [re.split('[ :]', t)[1] for t in tweets_s.created]

hourly_dist = tweets_s[['hour', 'created']].groupby('hour').count()

# %% plot hourly dist
hourly_dist.plot()
plt.title('No. of #Brexit tweets per hour on 29 Mar, 2018')
plt.legend(labels=['tweet count'])
plt.savefig('hourly_dist.png')
# %%
