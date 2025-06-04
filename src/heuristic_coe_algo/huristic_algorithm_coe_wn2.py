'''
@project_name           - Heuristic Algorithm for Cograph Clustering
@file_description       - Heuristic algorithm2
@author                 - dewan wahid
'''


import random

from src.networkx_utils.exporter import *
from src.networkx_utils.importer import *
from src.heuristic_coe_algo.cluster_merging_and_filtering import *
from src.exact_algos.exact_ce_min import *
from src.exact_algos.exact_coe_max import *
from src.exact_algos.exact_coe_min import *
from src.heuristic_coe_algo.cluster_integration_to_network2 import * 
from src.heuristic_coe_algo.cluster_merging_and_filtering import *
from src.heuristic_coe_algo.induced_network import *
from src.heuristic_coe_algo.node_prioritization import *
from src.heuristic_coe_algo.node_prioritization import *
from src.heuristic_coe_algo.node_reindex_dictionary import *
from src.heuristic_coe_algo.keyword_clusters_from_result_dict import *


def get_clusters_using_coe_heuristic(G, model_thrd_this: int, c: int, algo_choice: str):
    # ------------------------------------------------------
    # STEP 01: Node prioritization based on degree
    # -------------------------------------------------------
    # vList_deg: list = get_avg_weighted_degree_node_list_ascending(G)
    vList_deg: list = get_degree_node_list_ascending(G)

    # Setting model threshold, indices, and cluster id tracker
    cluster_id_dict: dict = {}  # cluster id dictionary
    model_thrd2 = model_thrd_this - 1
    i_stp = 0

    # Selecting each node from the node prioritization list
    while len(vList_deg) > 0:
        i_stp = i_stp + 1
        print('\n\n-------------------\nStep: ', i_stp)

        # Get the highest degree node from the node priority list
        v = vList_deg.pop()

        # --------------------------------------------------------------------
        # STEP 02: Induced Network Selection
        # --------------------------------------------------------------------

        # Get neighbour list of node v in G
        v_nbrs: list = [u for u in G.neighbors(v)]
        # print('\n\n-------------------\nNode v:', v, '; nbrs:', v_nbrs)
        print('\nNode v:', v)

        # Get the strongest neighbour of v in G
        w_uv: int = 0
        u: int = 0
        for a in v_nbrs:
            w_av = G.edges[a, v]['weight']
            if w_av > w_uv:
                u = a

        # Get neighbour list of u in G
        u_nbrs: list = []
        if u in G.nodes:
            u_nbrs = [j for j in G.neighbors(u)]

        # Merge u and v neighbours
        uv_nbrs = u_nbrs + v_nbrs

        # Remove the repeated elements
        uv_nbrs = list(dict.fromkeys(uv_nbrs))

        # Check the model threshold for the
        uv_nbrs_size: int = len(uv_nbrs)

        # Check model threshold
        if uv_nbrs_size > model_thrd2:
            uv_nbrs = random.sample(uv_nbrs, k=model_thrd2)

        # Add node u and v to its neighbour set
        if u not in uv_nbrs: uv_nbrs.append(u)
        if v not in uv_nbrs: uv_nbrs.append(v)
        print('Got (', u, ',', v, ') neighbours list (final)')

        # Reindexing dictionary for nodes
        node_key_dict: dict = get_node_new_index_dictionary(uv_nbrs)

        # Get the induced network of v in G and Gx
        IG_v = get_induced_network_in_G(G, uv_nbrs, node_key_dict)
        print('Got IG network, Nodes: ', len(IG_v.nodes), ', Links: ', len(IG_v.edges))

        # Get the P4-free network for G
        IGx_v = get_p4_free_link_cost_network2(IG_v)
        print('Got IGx network, Nodes: ', len(IGx_v.nodes), ', Links: ', len(IGx_v.edges))

        # -----------------------------------------------------------------------
        # STEP 3: Solve CoE ILP on induced network
        # -----------------------------------------------------------------------
        P_sol: list = []

        if algo_choice == 'min':
            P_sol = coe_min_clustering_weighted(IG_v, IGx_v)
            print('Solved CoE ILP Minimization')
        elif algo_choice == 'max':
            P_sol = coe_max_clustering_weighted(IG_v, IGx_v)
            print('Solved CoE ILP Maximization')

        # Get the solution partitions with actual node (reversing re-indexing)
        P_sol_act: list = get_reverse_indexing(P_sol, node_key_dict)
        print('Clusters on node', v, 'induced network:', P_sol_act)

        # -----------------------------------------------------------------------
        # STEP 4: Integrating clusters to G and removing visited nodes and links
        # -----------------------------------------------------------------------
        G, c, cluster_id_dict, vList_deg = \
            integrate_this_cluster_list2(G, P_sol_act, c, cluster_id_dict, vList_deg)

        print('vList Length: ', len(vList_deg))

    return cluster_id_dict


if __name__ == '__main__':
    # Network path
    net_path = ' '

    # Read network and its complement network
    G = networkx_read_weighted_network_from_csv(net_path)
    print('Input network loaded')

    # Model threshold and cluster id starting point
    model_thrd: int = 19  # max size of induced network to be solved by exact ILP
    c: int = 1000000  # cluster id starting point

    # Solve heuristic algorithm for CoE on Weighted network
    result_clusters: dict = get_clusters_using_coe_heuristic(G, model_thrd, c, 'min')
    # print('Result: ', result_clusters)
    print('Heuristic solved')

    # Filtering clusters
    final_clusters: dict = get_merged_clusters(result_clusters)
    # print('Final clusters:', final_clusters)

    print('Got final clusters')

    # Get the keyword clusters
    key_id_path = ''

    # output path
    output_path = ''

    # get keywords clusters
    get_produced_clusters(final_clusters, key_id_path, output_path)

    print('\n***************************'
          '\n\tHACoEWN DONE!\n'
          '***************************')
