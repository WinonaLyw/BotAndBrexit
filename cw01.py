import numpy as np
import pandas as pd


tweets = pd.read_csv("Tweets1.267Million.csv" , encoding='latin-1')

tweets.head(4)

# with open('Tweets1.267Million.csv', 'r') as fp:
#     for _ in range(4):
#         line = fp.readline()
#         print (line)