'''
@project_name   - Heuristic Algorithm for Cograph Clustering
@file_name      - Exact Cograph Editing (CoE)
@author         - dewan wahid
'''


from docplex.mp.model import Model
from src.heuristic_coe_algo.partitioning import *
from src.exact_algos import *
from src.networkx_utils.importer import *


def coe_max_clustering_weighted(G, Gx):

    # Indices
    N = range(1, len(G.nodes) + 1)

    # Create Model Instances
    coe = Model(name='cograph_editing_max')

    # Decision variable
    x = {(i, j): coe.binary_var(name='x_{0}_{1}'.format(i, j)) for i in N for j in N}

    # ------------------------------------
    # CoE: Objective Function
    # ------------------------------------
    # Link Deletion Cost
    LDC = 0

    for i in N:
        for j in N:
            if i < j and G.has_edge(i, j):
                w_ij = G.edges[i, j]['weight']

                LDC_this = coe.sum(x[i, j] * w_ij)
                LDC = LDC + LDC_this

    # Link Insertion Cost
    LIC = 0

    for i in N:
        for j in N:
            if i < j and Gx.has_edge(i, j):
                del_ij = Gx.edges[i, j]['weight']

                LIC_this = coe.sum((x[i, j]) * del_ij)
                LIC = LIC + LIC_this

    # Total Cost = Link Deletion Cost (LDC) + Link Insertion Cost (LIC)
    total_cost = LDC - LIC

    # Minimize all cost
    coe.maximize(total_cost)

    # ------------------------------------
    # CoE: Constraint
    # ------------------------------------

    # ............................................
    # Constrain 01: P4 free (Converting to cograph)
    # x_ij + x_jk + x_kl - x_ik - x_jl - x_ik <= 2
    # .............................................
    for i in N:
        for j in N:
            for k in N:
                for l in N:
                    if i != j != k != l:
                        # linear expression for constrain
                        C1 = coe.sum(x[i, j] + x[j, k] + x[k, l] - x[i, k] - x[j, l] - x[i, l])

                        # set constraint
                        coe.add_constraint(C1 <= 2)

    # .............................................
    # Constraint: Undirected link
    # x_ij = x_ji
    # .............................................
    for i in N:
        for j in N:
            if i != j:
                # linear expression for constraint
                C2 = coe.sum(x[i, j] - x[j, i])

                # set constraint
                coe.add_constraint(C2 == 0)

    solution = coe.solve()
    if solution is None:
        print('- coe model is infeasible')

    assert solution

    # Print
    # for i in N:
    #     for j in N:
    #         if i<j:
    #             print('x[', i, ',', j, ']: ', solution.get_value(x[i,j]))

    # Get clusters
    P = []  # clusters partition set

    for i in N:
        for j in N:
            if i < j:
                if solution.get_value(x[i, j]) == 1:
                    S = []
                    S.append(i)
                    S.append(j)
                    P = get_partitions(P, S)

    # Merging any two partitions that have common element(s)
    P_final: list = []

    for L in P:
        P_final = get_partitions(P_final, L)

    # Add objective value to P
    # P_final.append(solution.get_objective_value())

    return P_final


if __name__ == '__main__':
    # Network path
    net_path = 'test_data/test_net_id.csv'
    net_path_p2 = 'test_data/test_net_id_p4_free_link_net.csv'

    # Read network and its complement network
    G = networkx_read_weighted_network_from_csv(net_path)
    Gx = networkx_read_weighted_network_from_csv(net_path_p2)

    # Solve CoE ILP
    P: list = coe_max_clustering_weighted(G, Gx)
    print(P)



