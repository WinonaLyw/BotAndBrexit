# Bot and Brexit
### Analysis of bot influnce with tweets having #Brexit hashtags

## Sample selection**

1. select user account using score: [this subtext](select_account.py)
    1. prob < 0.01 quantile as human accounts, saved in 'human_accounts.csv'
    1. prob > 0.99 quantile as bot accounts, saved in 'bots_accounts.csv'