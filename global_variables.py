'''
This file is to save globally controlled variables.
'''


fname_extended_tweets = 'data/extended_tweets.csv'

# selected sample date
selected_date = '2018-03-29'

# sample files
fname_sample_tweets = 'data/sample_tweets_{0}.csv'.format(selected_date)
fname_sample_accounts_old = 'data/sample_accounts_old_{0}.csv'.format(selected_date)
fname_sample_accounts = 'data/sample_accounts_{0}.csv'.format(selected_date)

fname_bot_hashtag_cooc = 'data/bot_hashtag_cooc_{0}.csv'.format(selected_date)
fname_human_hashtag_cooc = 'data/human_hashtag_cooc_{0}.csv'.format(selected_date)
fname_human_sample_hashtag_cooc = 'data/human_sample_hashtag_cooc_{0}.csv'.format(selected_date)

fname_hashtag_oc = 'data/hashtags_{0}.csv'.format(selected_date)
fname_bot_hashtag_oc = 'data/bot_hashtags_{0}.csv'.format(selected_date)
fname_human_hashtag_oc = 'data/human_hashtags_{0}.csv'.format(selected_date)
fname_human_sample_hashtag_oc = 'data/human_sample_hashtags_{0}.csv'.format(selected_date)




# botness score
SCORE_50_Q = 0.25
SCORE_75_Q = 0.33
SCORE_85_Q = 0.37

score_entropy = SCORE_85_Q
