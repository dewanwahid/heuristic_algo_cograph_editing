import csv


def get_produced_clusters(result_dict, key_id_input_path: str, keyword_cluster_output_path: str):
    # read the keyword id list
    reader = csv.reader(open(key_id_input_path, 'r'))
    key_id_dict = {}
    for row in reader:
        k, v = row
        k_int = int(k)
        key_id_dict[k_int] = v

    for k in result_dict.keys():

        # this cluster
        this_cluster = result_dict[k]
        # print(this_cluster)

        # this cluster node name (keyword)
        this_cluster_keyword = []
        for i in this_cluster:
            i_keyword = key_id_dict[i]
            this_cluster_keyword.append(i_keyword)
            # print(i_keyword)

        # output file path name
        clus_output_path = keyword_cluster_output_path + str(k) + '.txt'

        with open(clus_output_path, 'w') as f:
            for e in this_cluster_keyword:
                f.write(e)
                f.write('\n')

    return None


if __name__ == '__main__':
    # keyword id dicti
    key_id_path = ''

    # output path
    output_path = ''

    # Final dictionary output
    final_dict: dict = {100001: [5, 7, 6, 8, 12], 100007: [10, 9, 2, 1, 4, 3, 15, 16, 17, 11, 13, 14, 18]}

    # get keywords clusters
    get_produced_clusters(final_dict, key_id_path, output_path)
    print('done')
