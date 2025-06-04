"""
@project_name   - Heuristic Algorithm for Cograph Clustering
@file_name      - Node indexing and reverses indexing for CoE operation
@author         - dewan wahid
"""


from src.heuristic_coe_algo.dict_utils import *

# -----------------------------------------------------------------
# Get new index for node list starts from 1, 2, ....
# -----------------------------------------------------------------

def get_node_new_index_dictionary(node_list: list):
    node_key_dict = {}
    size = len(node_list)

    for i in range(0, size):
        node = node_list[i]
        key: int = i + 1
        node_key_dict[node] = key

    return node_key_dict


# -----------------------------------------------------------------
# Reverse indexing the node list for given node partition
# -----------------------------------------------------------------

def get_reverse_indexing(P_min: list, node_key_dict: dict):
    P_act: list = []

    for p in P_min:
        p_act: list = []

        for e in p:
            # print('e:', e)
            nd: int = get_key_from_dictionary_for_value(node_key_dict, e)
            # print('nd', nd)
            p_act.append(nd)

        P_act.append(p_act)

    return P_act
