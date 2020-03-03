from os import path
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import stylecloud

# %% Read the whole text.
tweets_s = pd.read_csv('../data/sample_tweets_2018-03-29.csv')
tweets_s = tweets_s.fillna({'hashtags':''})

text = ''
for hastags in tweets_s.hashtags :
    text += str(hastags)


# %%
file1 = open("hashtag.txt","w") 

file1.writelines(text) 
file1.close()


stylecloud.gen_stylecloud(file_path='hashtag.txt',
                          icon_name='fab fa-twitter',
                          palette='colorbrewer.sequential.Blues_9',
                          gradient='horizontal')


# %%
