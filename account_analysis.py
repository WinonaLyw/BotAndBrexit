'''
Account analysis
Try to detect bot out from human accounts
1. k-means, K=2, use 80 platform
2. k-means, K=2, use 6 categories platform ordinal values
3. k-means, K=2, less attributes ('total_tweet', 'retweet_rate', 'max_tweets_hr')
4. k-means, K=2, with stributes ('total_tweet', 'total_retweet', 'max_tweets_hr', 'platforms_used', 'platform_cate')
5. set rules to include total tweets > 1500 or max tweet per hour (max_tweets_hr) > 50
'''

# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn import preprocessing
import sklearn.cluster as cluster
import sklearn.metrics as metrics

import global_variables as gv

# %%
accounts = pd.read_csv(gv.fname_sample_accounts, index_col=0)

# %% === 1.
attribute_col = ['prob', 'total_tweet', 'retweet_rate', 'max_tweets_hr', 'ave_hashtag', 'platforms_used', 'common_platform']

attributes = accounts.loc[:, attribute_col]

le = preprocessing.LabelEncoder()
# %% label platform into numeric values
# attributes.apply(le.fit_transform(attributes['common_platform']))
## failed with 80 platforms

platforms = list(set(attributes['common_platform']))
attributes['p_1'] = [platforms.index(t) for t in attributes.common_platform]

attributes = attributes.drop('common_platform', axis = 1)

# %% cluster use k-means
K = 2 #one cluster for bot and another for human accounts

km = cluster.KMeans(n_clusters=K)
km.fit(attributes)

print (km.labels_)
print (km.cluster_centers_)

print (np.unique(km.labels_, return_counts=True))
print ("Silhouette score: ", metrics.silhouette_score(attributes, km.labels_))
print (precision_recall(km.labels_))

'''
[11346,   353]
Silhouette score:  0.8833455392588392
precision : 0.2359421822668782
recall : 0.9291912530371399
'''
# accounts['r_1'] = km.labels_

# %% categorise platforms into 6 types
p_c = pd.read_csv('platform_category.csv')
accounts = accounts.join(p_c.set_index(['platform'], verify_integrity=True), on=['common_platform'], how='left')

attribute_col.append('platform_cate')
attribute_col.remove('common_platform')

# %% calculate precision and recall of clustering result bot and bot score selected bot
def precision_recall(labels):
    bscore = list(accounts['b_1'])
    TP = 0.0
    FP = 0.0
    TN = 0.0
    FN = 0.0
    for i in range(len(bscore)):
        if bscore[i] == 1:
            if labels[i] == bscore[i]:
                TP += 1
            else :
                FN += 1
        else :
            if labels[i] == bscore[i]:
                TN +=1
            else :
                FP += 1
    print ('precision :', TP / (TP + FP))
    print ('recall :', TP/ (TP + FN))

# %%  === 2
attributes = accounts.loc[:, attribute_col]

km2 = cluster.KMeans(n_clusters=K)
km2.fit(attributes)

print (km2.labels_)
print (km2.cluster_centers_)

print (np.unique(km2.labels_, return_counts=True))
print ("Silhouette score: ", metrics.silhouette_score(attributes, km2.labels_))
print (precision_recall(km2.labels_))

'''
[11346,   353]
Silhouette score:  0.8833455392588392
precision : 0.2359421822668782
recall : 0.9291912530371399
'''
# accounts['r_2'] = km2.labels_

# %% === 3
attribute_col3 = ['prob','total_tweet', 'retweet_rate', 'max_tweets_hr']

attributes = accounts.loc[:, attribute_col3]

km3 = cluster.KMeans(n_clusters=K)
km3.fit(attributes)

print (km3.labels_)
print (km3.cluster_centers_)


print (np.unique(km3.labels_, return_counts=True))
print ("Silhouette score: ", metrics.silhouette_score(attributes, km3.labels_))
print (precision_recall(km3.labels_))

'''
[11346,   353]
Silhouette score:  0.8833455392588392
precision : 0.2359421822668782
recall : 0.9291912530371399
'''

# accounts['r_3'] = km3.labels_

# %% === 4
attribute_col4 = ['total_tweet', 'total_retweet', 'max_tweets_hr', 'platforms_used', 'platform_cate']
attributes = accounts.loc[:, attribute_col4]

km4 = cluster.KMeans(n_clusters=K)
km4.fit(attributes)

print (km4.labels_)
print (km4.cluster_centers_)


print (np.unique(km4.labels_, return_counts=True))
print ("Silhouette score: ", metrics.silhouette_score(attributes, km4.labels_))
print (precision_recall(km4.labels_))
'''
[6137, 5562]
Silhouette score:  0.881060472116978
precision : 0.6028985507246377
recall : 0.07219715376605346
'''

# %% plot attributes againt botness score scatter
attribute_col = ['prob', 'total_tweet', 'retweet_rate', 'max_tweets_hr', 'ave_hashtag', 'platforms_used', 'platform_cate']

attributes = accounts.loc[:, attribute_col]

prob1 = attributes[attributes.prob >= gv.score_entropy] 
prob2 = attributes[attributes.prob < gv.score_entropy]

cols = attributes.columns
j = 1
n = len(cols)
plt.figure(figsize=(8,24))
for i in range(1, n):
    plt.subplot(6, 1, j)
    plt.scatter(prob1[cols[i]], prob1.prob, c = 'y', marker = 'o')
    plt.scatter(prob2[cols[i]], prob2.prob, c = 'c', marker = '^')
    plt.xlabel(cols[i])
    plt.ylabel('botness score')
    if cols[i] == 'platform_cate':
        plt.xlabel('platforms')
        plt.xticks(range(6), ['Official', 'Alternation', 'Cross Platform', 'Management(3rd pty)', 'Marketing(3rd pty', 'Unknown'], rotation=20)
    plt.legend(['score >= {0}'.format(gv.score_entropy), 'score < {0}'.format(gv.score_entropy)])
    j +=1
plt.savefig('output/accounts_scatter.png')

# %% plot attributes boxplot
cols = attributes.columns
j = 1
n = len(cols)
plt.figure(figsize=(8,24))
for i in range(1, n):
    plt.subplot(7, 1, j)
    plt.boxplot([prob1[cols[i]], prob2[cols[i]]])
    plt.title(cols[i])
    # plt.ylabel('botness score')
    plt.xticks([1,2],['score >= {0}'.format(gv.score_entropy), 'score < {0}'.format(gv.score_entropy)])
    j +=1
plt.savefig('output/accounts_boxplot.png')

# %% === 5
accounts['b_2'] = accounts['b_1']

for i in accounts[accounts.b_1 == 0].index:
    r = 0
    if accounts.loc[i, 'total_tweet'] > 1500 or \
        accounts.loc[i, 'max_tweets_hr'] > 50:
        accounts.loc[i, 'b_2'] = 1
    
# %%
accounts.to_csv(gv.fname_sample_accounts)

