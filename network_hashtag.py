'''
Network Hashtag
1. get hashtag occurrence table for bots and human accounts repectively
2. get hashtag co-occurrence table for bots and human accounts repectively
'''

# %% imports
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

import global_variables as gv

# %% read sample tweets

tweets_s = pd.read_csv(gv.fname_sample_tweets, index_col = 0)
accounts = pd.read_csv(gv.fname_sample_accounts, index_col = 0)

# %% separate bot/human accounts
acc = accounts[['user','prob','b_2']].set_index(['user'], verify_integrity=True)
tweets_s = tweets_s.join(acc, on=['screenName'], how='left')

tweets_s = tweets_s.fillna({'hashtags':''})
tweets_s['hashtags'] = [str(s).split(',') for s in tweets_s['hashtags']]

# %% sample huamn account to have same size as bot accounts
M = len(tweets_s[tweets_s.b_2 == 1])
tweets_h_sample = tweets_s[tweets_s.b_2 == 0].sample(n = M)

# %%
def hashtag_occurrence(df):
    hashtag = pd.DataFrame(columns=['T', 'timeslot', 'count'])
    for row in df[['hashtags','timeslot']].iterrows():
        slot = row[1]['timeslot']
        t_l = row[1]['hashtags']
        if len(t_l) > 0:
            for i in range(0, len(t_l)):
                hashtag = hashtag.append({'T': t_l[i].lower(), 'timeslot':slot, 'count':1}, ignore_index=True)
    hashtag = hashtag.groupby(['T','timeslot'], as_index=False).sum()
    hashtag = hashtag.astype({'count':'int32'})
    return hashtag

# %% occurrence 
hashtag_oc = hashtag_occurrence(tweets_s)
hashtag_oc.to_csv(gv.fname_hashtag_oc)

hashtag_oc.nlargest(10, 'count')

# all accounts
hashtag_b_oc = hashtag_occurrence(tweets_s[tweets_s.b_2 == 1])
hashtag_h_oc = hashtag_occurrence(tweets_s[tweets_s.b_2 == 0])
# sample human accounts
hashtag_h_sample_oc = hashtag_occurrence(tweets_h_sample)

hashtag_b_oc.to_csv(gv.fname_bot_hashtag_oc)
hashtag_h_oc.to_csv(gv.fname_human_hashtag_oc)
hashtag_h_sample_oc.to_csv(gv.fname_human_sample_hashtag_oc)

# %%
def plot_hashtag_time_flow(df_b, df_h, tag):
    t_b = df_b[df_b['T']==tag].sort_values(by=['timeslot'])
    t_h = df_h[df_h['T']==tag].sort_values(by=['timeslot'])
    plt.plot(t_b['timeslot']%24, t_b['count'], 'r')
    plt.plot(t_h['timeslot']%24, t_h['count'], 'g')
    plt.title('No. of tweets containing {0} per hour'.format(tag))
    plt.xlabel('hour of day')
    plt.legend(labels=['Bot network', 'Human network'])
    plt.xlim(0, 23)
    plt.xticks(range(0, 24, 4), ['{0:0=2d}:00'.format(i) for i in range(0, 24, 4)])
    plt.savefig('output/hourly_trade_{0}.png'.format(tag))
    plt.close()

# %%
tag_list = list(set(hashtag_oc['T']))
for tag in tag_list:
    # ['#brexit', '#eu', '#nhs', '#article50', '#12months2go', '#politics', '#stopbrexi', '#stopbrexit'] 
    plot_hashtag_time_flow(hashtag_b_oc, hashtag_h_oc, tag)
    # sample
    # plot_hashtag_time_flow(hashtag_b_oc, hashtag_h_sample_oc, tag)

# %%
def hashtag_cooccurrence(df):
    hashtag = pd.DataFrame(columns=['T1', 'T2', 'timeslot', 'count'])
    for row in df[['hashtags','timeslot']].iterrows():
        slot = row[1]['timeslot']
        t_l = row[1]['hashtags']
        if len(t_l) > 0:
            if len(t_l) == 1 and len(t_l[0])>0:
                hashtag = hashtag.append({'T1': t_l[0].lower(), 'timeslot':slot, 'count':1}, ignore_index=True)
            else :
                for i1 in range(0, len(t_l) - 1):
                    for i2 in range(i1 + 1, len(t_l)):
                        hashtag = hashtag.append({'T1': t_l[i1].lower(), 'T2': t_l[i2].lower(), 'timeslot':slot, 'count':1}, ignore_index=True)
    hashtag = hashtag.groupby(['T1','T2','timeslot'], as_index=False).sum()
    hashtag = hashtag.astype({'count':'int32'})
    return hashtag


#%% co-occurrence entire account sample
hashtag_b = hashtag_cooccurrence(tweets_s[tweets_s.b_2 == 1])

hashtag_h = hashtag_cooccurrence(tweets_s[tweets_s.b_2 == 0])

hashtag_b.to_csv(gv.fname_bot_hashtag_cooc)
hashtag_h.to_csv(gv.fname_human_hashtag_cooc)

# %% co-occurrence sample human accounts 
hashtag_h_sample = hashtag_cooccurrence(tweets_h_sample)

hashtag_h_sample.to_csv(gv.fname_human_sample_hashtag_cooc)

# %%
def network_summary(gDict):
    '''
    gDict : a list of networkx graph
    '''
    result_dict = {}
    for (t ,g) in gDict.items():
        h = t%24
        print ('Hourly Hashtag Co-occurence {0:0=2d}:00 to {1:0=2d}:00'.format(h, h+1))

        print ('number of nodes: ', len(g.nodes()))
        print ('number of edges: ', len(g.edges()))
        print ('Density: ', nx.density(g))
        print ('Assortativity coefficient : ', nx.degree_assortativity_coefficient(g, weight='count'))
        print ('Number of connected components: ', nx.number_connected_components(g))
        print ('Diameter of largest connected component: ', nx.diameter(max(nx.connected_component_subgraphs(g), key=len)))
        print ('Clustering coefficient of #brexit: ', nx.clustering(g,'#brexit'))
    
        # print ('Degree: ', g.degree(weight='count'))
        result_dict[t] = {'Nodes':len(g.nodes()), 'Edges': len(g.edges()), \
            'Density':'%.2f'%(nx.density(g)), \
            'Assortativity':'%.2f'%(nx.degree_assortativity_coefficient(g)), \
            'ConnectedComponents':nx.number_connected_components(g), \
            'Diameter':nx.diameter(max(nx.connected_component_subgraphs(g), key=len)), \
            'Clustering#brexit':'%.2f'%(nx.clustering(g,'#brexit'))}
    return result_dict

def hourly_G(df):
    timeslot = list(set(df.timeslot))
    h_g = {}
    for t in timeslot:
        g = nx.from_pandas_edgelist(df[df.timeslot == t], 'T1', 'T2', edge_attr=['count', 'timeslot'])
        h_g[t] = g
    return h_g

        
print ("Bot Hashtags")
bot_dict = network_summary(hourly_G(hashtag_b))
bot_df = pd.DataFrame.from_dict(bot_dict, orient='index')
bot_df.to_csv('output/Bot_hourly_network_stat.csv')

print ("Human Hashtags")
human_dict = network_summary(hourly_G(hashtag_h_sample))
human_df = pd.DataFrame.from_dict(human_dict, orient='index')
human_df.to_csv('output/Human_hourly_network_stat.csv')

# %%
import interactive_network

def draw_interactive_hourly_network(df, fname):
    timeslot = list(set(df.timeslot))
    # plt.figure(figsize=(40, 240))
    h_g = {}
    figs = []
    for t in timeslot:
        # plt.subplot(len(timeslot),2,t+1)
        h = t%24
        figs.append(interactive_network.draw_network(df[df.timeslot == t], title='Hourly Hashtag Co-occurence {0:0=2d}:00 to {1:0=2d}:00'.format(h, h+1)))
    # interactive_network.figures_to_html(figs, fname)

# %%       
draw_interactive_hourly_network(hashtag_b, 'Network_Hourly_Bot')  

# draw_interactive_hourly_network(hashtag_h, 'Network_Hourly_Human')  

draw_interactive_hourly_network(hashtag_h_sample, 'Network_Hourly_Human_Sample')      

# %% daily network
interactive_network.draw_network(hashtag_b[['T1', 'T2', 'count']].groupby(['T1', 'T2']).sum().reset_index()).write_html('output/Daily_bot.html')
interactive_network.draw_network(hashtag_h[['T1', 'T2', 'count']].groupby(['T1', 'T2']).sum().reset_index()).write_html('output/Daily_human.html')
interactive_network.draw_network(hashtag_h_sample[['T1', 'T2', 'count']].groupby(['T1', 'T2']).sum().reset_index()).write_html('output/Daily_human_sample.html')


# %%
def plot_hashtag_pair_time_flow(df_b, df_h, tag_pair):
    t_b = df_b[df_b['T1']==tag_pair[0]][df_b['T2'] == tag_pair[1]].sort_values(by=['timeslot'])
    t_h = df_h[df_h['T1']==tag_pair[0]][df_h['T2'] == tag_pair[1]].sort_values(by=['timeslot'])
    plt.plot(t_b['timeslot']%24, t_b['count'], 'r')
    plt.plot(t_h['timeslot']%24, t_h['count'], 'g')
    plt.title('No. of tweets containing {0} pair per hour'.format(tag_pair))
    plt.xlabel('hour of day')
    plt.legend(labels=['Bot network', 'Human network'])
    plt.xlim(0, 23)
    plt.xticks(range(0, 24, 4), ['{0:0=2d}:00'.format(i) for i in range(0, 24, 4)])
    plt.savefig('output/hourly_pair_trade_{0}_{1}.png'.format(tag_pair[0], tag_pair[1]))
    plt.close()


plot_hashtag_pair_time_flow(hashtag_b, hashtag_h_sample, ('#brexit', '#politics'))
plot_hashtag_pair_time_flow(hashtag_b, hashtag_h_sample, ('#bbcbreakfast', '#brexit'))

# %%
