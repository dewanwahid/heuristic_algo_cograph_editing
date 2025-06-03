## --------------------------
## Network exporter
## --------------------------
import networkx as nx
import pandas as pd
import csv


# ----------------
# Export network as csv
# -----------------

# Export network
def networkx_export_network_as_csv(Gx, file_path):
    with open(file_path, 'w', newline='\n') as csvfile:
        wr = csv.writer(csvfile)

        # header
        rh = 'Source', 'Target', 'Weight'
        wr.writerow(rh)
        print('here')

        # write each rows
        for e in Gx.edges:
            rhx = str(e[0]), str(e[1]), str(Gx.edges[e[0], e[1]]['weight'])
            wr.writerow(rhx)

    return None


if __name__ == '__main__':
    Gx = nx.Graph()

    # add nodes
    Gx.add_edge(1, 2, weight=2)
    Gx.add_edge(1, 3, weight=4)
    Gx.add_edge(1, 4, weight=5)

    # export path
    exp_path = ""

    networkx_export_network_as_csv(Gx, exp_path)
