'''
@project_name   - Heuristic Algorithm for Cograph Clustering
@file_name      - Node prioritization based on average weighted degree
@author         - dewan wahid
'''


def get_avg_weighted_degree_node_list_ascending(G):
    vList: dict = {}
    V = G.nodes

    # calculate average weighted degree of each node
    for v in V:
        avgDeg_v = int(G.degree(v, 'weight')/G.degree(v))      # average degree = weighted degree / degree
        vList[v] = avgDeg_v     # dict = {key : value}, key = node, value = average degree

    # sorting (descending order) nodes based on average weighted degree
    # vList_desc = sorted(vList, key=vList.get, reverse=True)
    vList_desc = sorted(vList, key=vList.get)
    return vList_desc


def get_degree_node_list_ascending(G):
    vList: dict = {}
    V = G.nodes

    # calculate average weighted degree of each node
    for v in V:
        avgDeg_v = G.degree(v)      # degree of node v
        vList[v] = avgDeg_v         # dict = {key : value}, key = node, value = average degree

    # sorting (descending order) nodes based on average weighted degree
    # vList_desc = sorted(vList, key=vList.get, reverse=True)
    vList_desc = sorted(vList, key=vList.get)
    return vList_desc