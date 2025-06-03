## --------------------------
## Network Importer
## --------------------------
import networkx as nx
import pandas as pd
import csv


## --------------
## Read from csv
## ---------------
def networkx_read_weighted_network_from_csv(file_path):
    # Convert csv to dataframe
    df_net = pd.read_csv(file_path)

    # networkx graph
    G = nx.Graph()

    # Add edges to graph (source, target(destination), weight)
    for ind in df_net.index:
        # get source, target(destination) node and weight
        src = int(df_net['Source'][ind])
        trg = int(df_net['Target'][ind])
        wgt = int(df_net['Weight'][ind])

        # add edge to networkx
        G.add_edge(src, trg, weight=wgt)

    return G


if __name__ == '__main__':

    # import path
    imp_path = ""

    G = networkx_read_weighted_network_from_csv(imp_path)

    print('Edges: ', [(e, G.edges[e]['weight']) for e in G.edges])