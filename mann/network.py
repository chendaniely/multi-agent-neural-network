#! /usr/bin/env python

import networkx as nx
import matplotlib.pyplot as plt


class Network(object):
    def __init__(self):
        pass

    def get_edge_list(self):
        pass


class DirectedFastGNPRandomGraph(nx.MultiDiGraph):
    def __init__(self, n, p):
        self.G = nx.fast_gnp_random_graph(n, p, directed=True)

    def show_graph(self, path_and_name):
        nx.draw_circular(self.G)
        # plt.show()
        plt.savefig(path_and_name)
