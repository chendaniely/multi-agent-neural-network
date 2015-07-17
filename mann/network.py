#! /usr/bin/env python

import networkx as nx
import matplotlib.pyplot as plt


class Network(object):
    def __init__(self):
        pass

    def get_edge_list(self):
        pass


class MannGraph(nx.MultiDiGraph):
    def show_graph(self, path_and_name):
        nx.draw_circular(self.G)
        # nx.draw_networkx_labels(self.G, pos=nx.draw_circular(self.G))
        # plt.show()
        plt.savefig(path_and_name)


class DirectedFastGNPRandomGraph(MannGraph):
    def __init__(self, n, p):
        self.G = nx.fast_gnp_random_graph(n, p, directed=True)


class BidirectionalBarabasiAlbertGraph(MannGraph):
    def __init__(self, n, m, seed=None):
        self.G = nx.barabasi_albert_graph(n, m, seed)


class WattsStrogatzGraph(nx.MultiGraph):
    def __init__(self, n, k, p, seed=None):
        self.G = nx.watts_strogatz_graph(n, k, p, seed=None)
