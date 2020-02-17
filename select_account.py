# %% import
import numpy as np
import pandas as pd

# %% read csv using pandas
accounts = pd.read_csv("BotScore73KUsers.csv")# , encoding='latin-1'
print (len(accounts))

# %% head dataframe
accounts.head(2)

# %% 0.01 & 0.99 quantiles score
q1, q2 = accounts.prob.quantile([0.01,0.99])
print (q1, q2)

# %% retrieve protential human account (score <= 0.01 quantile)
human = accounts[accounts.prob <= q1]
print (len(human))
human.to_csv("human_accounts.csv")

# %% retrieve protential bot account (score >= 0.99 quantile)
bots = accounts[accounts.prob >= q2]
print (len(bots))
bots.to_csv("bots_accounts.csv")

