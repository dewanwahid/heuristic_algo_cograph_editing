import networkx as nx

from src.networkx_utils.importer import *


def integrate_this_cluster_list(G_this,
                                Gx_this,
                                cluster_list: list,
                                c_id: int,
                                cluster_id_dict2: dict,
                                vList_deg: list):
    # -----------------------------------------------------------------------
    # Step 4: Integrating clusters to G and removing visited nodes and links
    # ----------------------------------------------------------------------

    for this_cluster in cluster_list:

        # -----------------------------------------------------------------
        # Step 4 (I): Get each cluster from the solution partition set
        # -----------------------------------------------------------------

        # put this cluster to the cluster id dictionary for tracking
        c_id = c_id + 1  # increase c for next cluster
        cluster_id_dict2[c_id] = this_cluster

        # print('\n\n******************************\nID:', c_id, '; Cluster: ', this_cluster)

        # Add this node to the network
        G_this.add_node(c_id)
        Gx_this.add_node(c_id)

        # Length of this cluster
        this_cls_len = len(this_cluster)

        # ----------------------------------------------
        # Step 4 (II): Get all neighbour of this cluster
        # ----------------------------------------------
        # Neighbours list of this cluster in G and Gx
        nbrs_c_G: list = []
        nbrs_c_Gx: list = []

        for k in this_cluster:

            # in G network
            if k in G_this.nodes:
                l_G: list = [i for i in G_this.neighbors(k)]
                nbrs_c_G = nbrs_c_G + l_G

                # print(k, ':', l_G)
                # print('Nbrs c in G:', nbrs_c_G)

            # in Gx network
            if k in Gx_this.nodes:
                l_Gx: list = [i for i in Gx_this.neighbors(k)]
                nbrs_c_Gx = nbrs_c_Gx + l_Gx

                # print(k, ':', l_Gx)
                # print('Nbrs c in Gx:', nbrs_c_Gx)

        # Union of neighbours in G and Gx together
        nbrs_c_GGx: list = nbrs_c_G + nbrs_c_Gx

        # Unique neighbours of c in G and Gx together
        nbrs_c_GGx_uniq = list(dict.fromkeys(nbrs_c_GGx))

        # Remove this cluster nodes from the neighbours list
        for k in this_cluster:
            if k in nbrs_c_GGx_uniq: nbrs_c_GGx_uniq.remove(k)

        # -----------------------------------------------------------------
        # Step 4(III): Remove link between this custer nodes and its neighbour node
        # -----------------------------------------------------------------

        w_ic_pos: int = 0
        w_ic_neg: int = 0

        # For each node from this cluster neighbour node
        for i in nbrs_c_GGx_uniq:
            # print('\n\tChecking for this cluster nbr:', i)

            # This cluster node
            for j in this_cluster:

                # get link weight(s) from G
                if G_this.has_edge(i, j):
                    w_ij_pos = G_this.edges[i, j]['weight']
                    w_ic_pos = w_ic_pos + w_ij_pos

                    # remove this link from G
                    e_pos = (i, j, {"weight": w_ij_pos})  # an edge with attribute data
                    G_this.remove_edge(*e_pos[:2])

                # get link weight(s) from Gx
                if Gx_this.has_edge(i, j):
                    w_ij_neg = Gx_this.edges[i, j]['weight']
                    w_ic_neg = w_ic_neg + w_ij_neg

                    # remove this link from Gx
                    e_neg = (i, j, {"weight": w_ij_neg})  # an edge with attribute data
                    Gx_this.remove_edge(*e_neg[:2])

            # -----------------------------------------------------------------
            # Step 4(IV): Add link between this cluster and its nei
            # -----------------------------------------------------------------
            # Calculate link (c,i) weight
            w_ic: int = w_ic_pos - int(w_ic_neg /12)

            # Add link (i,c_id) either in G or Gx based on weight
            if w_ic > 0: G_this.add_edge(c_id, i, weight=w_ic)
            elif w_ic < 0: Gx_this.add_edge(c_id, i, weight=abs(w_ic))
            else: continue

            # Resetting weight
            w_ic_pos = 0
            w_ic_neg = 0

        # Remove this cluster nodes from the network G and Gx and node prioritization list
        for k in this_cluster:
            if k in G_this.nodes: G_this.remove_node(k)
            if k in Gx_this: Gx_this.remove_node(k)
            if k in vList_deg: vList_deg.remove(k)

    return G_this, Gx_this, c_id, cluster_id_dict2, vList_deg


if __name__ == '__main__':
    # Network path
    g_net_path = 'test_net.csv'
    gx_net_path = 'complement_net.csv '

    # Read network and its complement network
    G = networkx_read_weighted_network_from_csv(g_net_path)
    Gx = networkx_read_weighted_network_from_csv(gx_net_path)

    # Node partition
    P_min_act = [[1, 2, 3], [5, 6], [7, 8]]
    vList_deg = [2, 3, 1, 6, 5, 8, 7]

    # Cluster id starts from
    c: int = 100000

    # Cluster id tracker dictionary
    cluster_id_dict: dict = {}

    # Integrate this node partition
    G_new, Gx_new, c, cluster_id_dict_new, vList_deg = \
        integrate_this_cluster_list(G, Gx, P_min_act, c, cluster_id_dict, vList_deg)

    # Print integrated networks
    print("\nG Links:", [(e, G_new.edges[e]['weight']) for e in G_new.edges])
    print('G Nodes: ', G.nodes)

    print("\nGx Network:", [(e, Gx_new.edges[e]['weight']) for e in Gx_new.edges])
    print('Gx Nodes: ', Gx.nodes)

    print('\nc: ', c)
    print('cluster_id_dict:', cluster_id_dict_new)
    print('vList_deg:', vList_deg)
