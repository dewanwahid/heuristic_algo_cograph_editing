

def get_merged_clusters(cluster_id_dict3: dict):

    # Deleting node id
    del_node = []

    # For each key in the cluster lists dictionary
    for k in cluster_id_dict3.keys():

        # Cluster list corresponding to this key
        this_cluster: list = cluster_id_dict3.get(k)

        # Nodes list to be added/deleted this cluster
        add_nodes_this_cluster = []
        del_nodes_this_cluster = []

        # Checking each node  in this cluster
        for id in this_cluster:
            id = int(id)
            # print('\tid:', id)

            if id > 100000:
                # get the linked cluster corresponding to this node id
                linked_cluster = cluster_id_dict3[id]
                
                # remove the linked clusters from dictionary
                del_node.append(id)

                # remove this node id from this cluster
                del_nodes_this_cluster.append(id)

                # merge linked cluster with this cluster
                add_nodes_this_cluster = add_nodes_this_cluster + linked_cluster

        # delete nodes from this clusters
        for j in del_nodes_this_cluster:
            this_cluster.remove(j)

        # add additional node to this cluster
        this_cluster = this_cluster + add_nodes_this_cluster

        # Updating dictionary
        cluster_id_dict3[k] = this_cluster
        # print('cluster_id_dict (updated):', cluster_id_dict3)

    # Removing linked clusters
    # print('del node: ', del_node)
    for i in del_node:
        cluster_id_dict3.pop(i)

    return cluster_id_dict3


if __name__ == '__main__':

    dc = {100001: [5, 7, 6, 8, 12],
          100002: [11, 13, 14, 18],
          100003: [1, 4, 3],
          100004: [9, 100003, 2],
          100005: [16, 17, 100002],
          100006: [100005, 15],
          100007: [100004, 100006, 10]
          }

    res: dict = get_merged_clusters(dc)
    print('Final:', res)