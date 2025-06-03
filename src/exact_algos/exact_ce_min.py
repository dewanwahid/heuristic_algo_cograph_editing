'''
@project_name   -
@file_name      - Clustering Editing (CE)
@author         - dewan wahid
'''

from docplex.mp.model import Model 
from src.exact_algos import *
from src.heuristic_coe_algo import *
from src.networkx_utils import *


def ce_min_clustering_weighted(G, Gx):
    # Index range
    N = range(1, len(G.nodes) + 1)

    # Model
    ce = Model(name='clustering_editing')

    # Decision variable
    x = {(i, j): ce.binary_var(name='x_{0}_{1}'.format(i, j)) for i in N for j in N}

    # Link Deletion Cost
    LDC = 0

    for i in N:
        for j in N:
            if i < j and G.has_edge(i, j):
                w_ij = G.edges[i, j]['weight']

                LDC_this = ce.sum(x[i, j] * w_ij)
                LDC = LDC + LDC_this

    # Link Insertion Cost
    LIC: int = 0

    for i in N:
        for j in N:
            if i < j and Gx.has_edge(i, j):
                del_ij = Gx.edges[i, j]['weight']

                LIC_this = ce.sum((1 - x[i, j]) * del_ij)
                LIC = LIC + LIC_this

    # Total Cost (Objective function) = Link Deletion Cost (LDC) + Link Insertion Cost (LIC)
    total_cost = LDC + LIC

    # Minimize all cost
    ce.minimize(total_cost)

    # ------------------------------------
    # CE: Constraint
    # ------------------------------------

    # Constrain: Triangle inequality
    for i in N:
        for j in N:
            for k in N:
                if i != j != k:
                    # linear expression for constraint
                    c1_this = ce.sum(x[i, j] + x[j, k] - x[i, k])

                    # set constraint
                    ce.add_constraint(c1_this >= 0)

    # Constraint: Undirected link
    for i in N:
        for j in N:
            if i != j:
                # linear expression for constraint
                c2_this = ce.sum(x[i, j] - x[j, i])

                # set constraint
                ce.add_constraint(c2_this == 0)

    # Solve model
    solution = ce.solve()

    if solution is None:
        print('- model is infeasible')

    assert solution

    # Get clusters
    P = []  # clusters partition set

    for i in N:
        for j in N:
            if i < j:
                if solution.get_value(x[i, j]) == 0:
                    S = []
                    S.append(i)
                    S.append(j)
                    P = partitioning.get_partitions(P, S)

    # Merging any two partitions that have common element(s)
    P_final: list = []
    for L in P:
        P_final = partitioning.get_partitions(P_final, L)

    # Add objective value to P
    # P_final.append(solution.get_objective_value())

    return P_final


if __name__ == '__main__':
    # Network path
    net_path = 'C:/Users/shaki/PycharmProjects/invoice_categorization/data/test_data/test_net_id_04.csv'
    net_path_p2 = 'C:/Users/shaki/PycharmProjects/invoice_categorization/data/test_data' \
                  '/test_net_id_04_p4_free_link_net.csv '

    # Read network and its complement network
    G = networkx_read_weighted_network_from_csv(net_path)
    Gx = networkx_read_weighted_network_from_csv(net_path_p2)

    # Solve CoE ILP
    P: list = ce_min_clustering_weighted(G, Gx)
    print(P)


