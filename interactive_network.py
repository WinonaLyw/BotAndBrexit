'''
Interactive network

1. to plot

'''

#%% 
import plotly.graph_objects as go
import networkx as nx
import os

#%%
def draw_network(df, title='Hourly Hashtag Co-occurence'):

    '''Draw a hashtag co-occurance network with given dataframe 

    Parameters
    ----------
    df : a hashtag co-occurence dataframe
        with columns ('T1', 'T2', 'count')

    title : str
        Title of the network graph.

    Return
    ----------
        a plotly figure in html format
        show graph with <figure>.show()
        or wrtie into html file with <figure>.write_html(<filname>, auto_open=True)

    '''

    nodes = list(set(df.T1).union(set(df.T2)))
    n_dict = {}
    for n in nodes:
        n_dict[n]=n

    G = nx.from_pandas_edgelist(df, 'T1', 'T2', edge_attr=['count'], create_using=nx.Graph())
    nx.set_node_attributes(G, n_dict, 'Hashtag')
    pos = nx.kamada_kawai_layout(G)

    for node in G.nodes:
        G.nodes[node]['pos'] = list(pos[node])

    edge_x = []
    edge_y = []
    traces = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        weight = float(G.edges[edge]['count']) / max(df['count']) * 3

    
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=weight, color='#888'),
            hoverinfo=None,
            mode='lines+text')
        traces.append(edge_trace)

    node_x = []
    node_y = []


    node_text = []
    node_degree = []

    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

        node_text.append(str(G.nodes[node]['Hashtag']))
        node_degree.append(nx.degree(G, weight='count')[node])

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo = 'text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='Blues',
            reversescale=False,
            color=[0,1000],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Co-occurence',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
        
    node_trace.marker.color = node_degree
    node_trace.text = node_text
    traces.append(node_trace)

    info_text = 'Total number of hastags: {0}, total number of co-occurence combination: {1}'.format(len(G.nodes()), len(G.edges()))
    fig = go.Figure(data=traces,
                layout=go.Layout(
                title='<br>{0}'.format(title),
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text=info_text,
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 )],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    fig.show()
    # fig.write_html('output/{0}.html'.format(fname), auto_open=True)
    return fig


# %%
def figures_to_html(figs, fname='network'):
    '''Saves a list of plotly figures in an html file.

    Parameters
    ----------
    figs : list[plotly.graph_objects.Figure]
        List of plotly figures to be saved.

    fname : str
        File name to save in.

    '''
    import plotly.offline as pyo

    filename = os.path.join('output', '{0}.html'.format(fname))

    dashboard = open(filename, 'w')
    dashboard.write("<html><head></head><body>" + "\n")

    add_js = True
    for fig in figs:
        inner_html = pyo.plot(
            fig, include_plotlyjs=add_js, output_type='div'
        )
        dashboard.write(inner_html)
        add_js = False

    dashboard.write("</body></html>" + "\n")
    dashboard.close()
