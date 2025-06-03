'''
@project_name   - Heuristic Algorithm for Cograph Clustering
@file_name      - Induced network for a node
@author         - dewan wahid
'''

import networkx as nx


def get_induced_network_in_G(G, v_nbrs_list, node_key_dict):
    # create a graph instance
    IG_v1 = nx.Graph()

    for u in v_nbrs_list:
        for v in v_nbrs_list:
            if u != v and G.has_edge(u, v):
                # edge weight
                wgt = G.edges[v, u]['weight']

                # get key of u and v for reindexing
                u_key = node_key_dict.get(u)
                v_key = node_key_dict.get(v)

                # add edge to networkx
                IG_v1.add_edge(v_key, u_key, weight=wgt)

    return IG_v1


def get_induced_network_in_Gx(Gx, v_nbrs_list, node_key_dict):
    # graph instance for induced network
    IGx_v2 = nx.Graph()

    for u in v_nbrs_list:
        for v in v_nbrs_list:
            if u != v and Gx.has_edge(u, v):
                # edge weight in Gx
                wgt = Gx.edges[v, u]['weight']

                # get key of u and v for reindexing
                u_key = node_key_dict.get(u)
                v_key = node_key_dict.get(v)

                # add edge to networkx
                IGx_v2.add_edge(v_key, u_key, weight=wgt)

    return IGx_v2
