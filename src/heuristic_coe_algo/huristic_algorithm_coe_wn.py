'''
@project_name           - Heuristic Algorithm for Cograph Clustering
@file_description       - Heuristic algorithm
@author                 - dewan wahid
'''


import random

from src.networkx_utils.exporter import *
from src.networkx_utils.importer import *
from src.heuristic_coe_algo.cluster_merging_and_filtering import *
from src.exact_algos.exact_ce_min import *
from src.exact_algos.exact_coe_max import *
from src.exact_algos.exact_coe_min import *
from src.heuristic_coe_algo.cluster_integration_to_network import * 
from src.heuristic_coe_algo.cluster_merging_and_filtering import *
from src.heuristic_coe_algo.induced_network import *
from src.heuristic_coe_algo.node_prioritization import *
from src.heuristic_coe_algo.node_prioritization import *
from src.heuristic_coe_algo.node_reindex_dictionary import *



def get_clusters_using_coe_heuristic(G, Gx, model_thrd: int, c: int, algo_choice: str):
    # ------------------------------------------------------
    # STEP 01: Node prioritization based on degree
    # -------------------------------------------------------
    vList_deg: list = get_degree_node_list_ascending(G)

    # Setting model threshold, indices, and cluster id tracker
    cluster_id_dict: dict = {}  # cluster id dictionary
    model_thrd2 = model_thrd - 1

    # Selecting each node from the node prioritization list
    while len(vList_deg) > 0:

        # Get the highest degree node from the node priority list
        v = vList_deg.pop()

        # --------------------------------------------------------------------
        # STEP 02: Induced Network Selection
        # --------------------------------------------------------------------

        # Get neighbour list of node v in G
        v_nbrs: list = [u for u in G.neighbors(v)]

        # Check the model threshold for the
        v_nbrs_size: int = len(v_nbrs)

        if v_nbrs_size > model_thrd2: v_nbrs = random.choices(v_nbrs, k=model_thrd2)

        # Add node v to its neighbour set
        v_nbrs.append(v)

        # Reindexing dictionary for nodes
        node_key_dict = get_node_new_index_dictionary(v_nbrs)

        # Get the induced network of v in G and Gx
        IG_v = get_induced_network_in_G(G, v_nbrs, node_key_dict)
        IGx_v = get_induced_network_in_Gx(Gx, v_nbrs, node_key_dict)

        # -----------------------------------------------------------------------
        # STEP 3: Solve CoE ILP on induced network
        # -----------------------------------------------------------------------
        P_sol: list = []

        if algo_choice == 'min':
            P_sol = coe_min_clustering_weighted(IG_v, IGx_v)
            print('Used minimization')
        elif algo_choice == 'max':
            P_sol = coe_max_clustering_weighted(IG_v, IGx_v)
            print('Used maximization')

        # Get the solution partitions with actual node (reversing re-indexing)
        P_sol_act: list = get_reverse_indexing(P_sol, node_key_dict)

        # -----------------------------------------------------------------------
        # STEP 4: Integrating clusters to G and removing visited nodes and links
        # -----------------------------------------------------------------------
        G, Gx, c, cluster_id_dict, vList_deg = \
            integrate_this_cluster_list(G, Gx, P_sol_act, c, cluster_id_dict, vList_deg)

    return cluster_id_dict


if __name__ == '__main__':
    # Network path
    net_path = 'test_data\test_net_id.csv'
    net_path_p4 = 'test_data/test_net_id_p4_free_link_net.csv'

    # Read network and its complement network
    G = networkx_read_weighted_network_from_csv(net_path)
    Gx = networkx_read_weighted_network_from_csv(net_path_p4)

    # Model threshold and cluster id starting point
    model_thrd: int = 5  # max size of induced network to be solved by exact ILP
    c: int = 100000  # cluster id starting point

    # Solve heuristic algorithm for CoE on Weighted network
    result_clusters: dict = get_clusters_using_coe_heuristic(G, Gx, model_thrd, c, 'max')
    print('Result: ', result_clusters)

    # Filtering clusters
    final_clusters: dict = get_merged_clusters(result_clusters)
    print('Final clusters:', final_clusters)
