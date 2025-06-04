'''
@project_name   - Heuristic Algorithm for Cograph Clustering
@file_name      - P4 free network creation
@author         - dewan wahid
'''

# -------------------
# P4 List in a network
# ---------------------
import networkx as nx
import pandas as pd
import math
from src.networkx_utils.exporter import *
from src.networkx_utils.importer import *


# ---------------------------
# P4 link list
# ---------------------------
def get_p4_list(G):
    p4_list = []

    for i in G.nodes:
        for j in G.nodes:
            for k in G.nodes:
                for l in G.nodes:
                    if i != j != k != l:
                        if G.has_edge(i, j):
                            if G.has_edge(j, k):
                                if G.has_edge(k, l):
                                    if not G.has_edge(i, k):
                                        if not G.has_edge(j, l):
                                            if not G.has_edge(i, l):

                                                this_p4 = [i, j, k, l]

                                                if any(sorted(this_p4) == sorted(x) for x in p4_list):
                                                    continue
                                                else:
                                                    p4_list.append(this_p4)

    return p4_list


# ------------------------------
# P4 link cost
# ------------------------------
def get_p4_free_link_cost_network(G, p4_list, exp_net_path):
    # Creating a graph for storing possible links and corresponding costs
    Gx = nx.Graph()

    for p4 in p4_list:

        # get p4 nodes
        i = p4[0]
        j = p4[1]
        k = p4[2]
        l = p4[3]

        # get all edges weights in this pp4
        w_ij = G.edges[i, j]['weight']
        w_jk = G.edges[j, k]['weight']
        w_kl = G.edges[k, l]['weight']

        # calculate the delta
        delta = math.floor((w_ij + w_jk + w_kl) / 3)

        # print('{', i, ',', j, ',', k, ',', l, '} : ', delta)

        # add links (i,k) at Gx with weight `delta'
        if not Gx.has_edge(i, k):
            Gx.add_edge(i, k, weight=delta)
        else:
            delta_o = Gx.edges[i, k]['weight']
            if delta < delta_o:
                Gx.edges[i, k]['weight'] = delta

        # add links (j,l) at Gx with weight `delta'
        if not Gx.has_edge(j, l):
            Gx.add_edge(j, l, weight=delta)
        else:
            delta_o = Gx.edges[j, l]['weight']
            if delta < delta_o:
                Gx.edges[j, l]['weight'] = delta

        # add links (i,l) at Gx with weight `delta'
        if not Gx.has_edge(i, l):
            Gx.add_edge(i, l, weight=delta)
        else:
            delta_o = Gx.edges[i, l]['weight']
            if delta < delta_o:
                Gx.edges[i, l]['weight'] = delta

        # export network
        networkx_export_network_as_csv(Gx, exp_net_path)

    return Gx


# ------------------------------
# P4 link cost
# ------------------------------
def get_p4_free_link_cost_network2(G):
    # Creating a graph for storing possible links and corresponding costs
    Gx = nx.Graph()

    # Get P4 list for G
    p4_list: list = get_p4_list(G)

    for p4 in p4_list:

        # get p4 nodes
        i = p4[0]
        j = p4[1]
        k = p4[2]
        l = p4[3]

        # get all edges weights in this pp4
        w_ij = G.edges[i, j]['weight']
        w_jk = G.edges[j, k]['weight']
        w_kl = G.edges[k, l]['weight']

        # calculate the delta
        delta = math.floor((w_ij + w_jk + w_kl) / 3)

        # print('{', i, ',', j, ',', k, ',', l, '} : ', delta)

        # add links (i,k) at Gx with weight `delta'
        if not Gx.has_edge(i, k):
            Gx.add_edge(i, k, weight=delta)
        else:
            delta_o = Gx.edges[i, k]['weight']
            if delta < delta_o:
                Gx.edges[i, k]['weight'] = delta

        # add links (j,l) at Gx with weight `delta'
        if not Gx.has_edge(j, l):
            Gx.add_edge(j, l, weight=delta)
        else:
            delta_o = Gx.edges[j, l]['weight']
            if delta < delta_o:
                Gx.edges[j, l]['weight'] = delta

        # add links (i,l) at Gx with weight `delta'
        if not Gx.has_edge(i, l):
            Gx.add_edge(i, l, weight=delta)
        else:
            delta_o = Gx.edges[i, l]['weight']
            if delta < delta_o:
                Gx.edges[i, l]['weight'] = delta

    return Gx


if __name__ == '__main__':
    # Network path
    net_path = 'test_net.csv'

    # Read network and its complement network
    G = networkx_read_weighted_network_from_csv(net_path)

    # Print
    print('\nG Network:')
    for e in G.edges:
        print(e, G.edges[e]['weight'])

    # P4 link network
    Gx = get_p4_free_link_cost_network2(G)

    # Print
    print('\nGx Network:')
    for e in Gx.edges:
        print(e, Gx.edges[e]['weight'])


