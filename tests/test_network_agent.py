#! /usr/bin/env python
###############################################################################
import nose
import sys
# import io
# import random
import os
# import glob
# import subprocess

import networkx as nx
import matplotlib.pyplot as plt
# import numpy as np
# import numpy.testing

from mann import agent_lens_recurrent
from mann import network_agent
# import helper

HERE = os.path.abspath(os.path.dirname(__file__))


class test_network_agent():
    def setup(self):
        # print("setup", file=sys.stderr)
        agent_lens_recurrent.LensAgentRecurrent.agent_count = 0

        self.test_agent = agent_lens_recurrent.LensAgentRecurrent(10)
        self.test_agent_1 = agent_lens_recurrent.LensAgentRecurrent(10)
        self.test_agent_2 = agent_lens_recurrent.LensAgentRecurrent(10)
        self.test_agent_3 = agent_lens_recurrent.LensAgentRecurrent(10)
        self.test_agent_1.state = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.test_agent_2.state = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        self.test_agent_3.state = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        all_agents = [self.test_agent, self.test_agent_1,
                      self.test_agent_2, self.test_agent_3]

        nx_G = nx.watts_strogatz_graph(4, 2, .5, 42)
        # print(nx_G.edges(), file=sys.stderr)

        self.test_network_agent = network_agent.NetworkAgent()
        self.test_network_agent.G = nx.MultiDiGraph()
        self.test_network_agent.G.add_nodes_from(all_agents)
        for idx, edge in enumerate(nx_G.edges()):
            # print(edge, file=sys.stderr)
            u, v = edge
            self.test_network_agent.G.add_edge(all_agents[u], all_agents[v])
        # print("Number of edges: {}".format(idx + 1), file=sys.stderr)
        nx.draw_circular(self.test_network_agent.G,
                         with_labels=True, arrows=True,
                         node_size=600)
        plt.draw()
        plt.savefig(os.path.join(HERE, 'lens', 'output', 'setup_network.png'))

    def teardown(self):
        # print("teardown", file=sys.stderr)
        pass

    @nose.with_setup(setup)
    def test_network_agent_step_info_lens_recurrent(self):
        test_time = 3
        test_network_agent = network_agent.NetworkAgent()
        calculated = test_network_agent.network_agent_step_info_lens_recurrent(
            test_time, self.test_agent)
        expected = '3,0,0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0\n'
        assert calculated == expected

        calculated = test_network_agent.network_agent_step_info_lens_recurrent(
            test_time, self.test_agent_2)
        expected = '3,2,0,2, 2, 2, 2, 2, 2, 2, 2, 2, 2\n'
        assert calculated == expected

    @nose.with_setup(setup)
    def test_write_network_agent_step_info(self):
        time_step = 2
        file_to_write = os.path.join(HERE, 'lens', 'output',
                                     'network_of_ageNts.pout')
        file_mode = 'w'
        agent_type = 'lens'

        # test_network_agent = network_agent.NetworkAgent()
        self.test_network_agent.write_network_agent_step_info(
            time_step, file_to_write, file_mode, agent_type,
            lens_agent_type='recurrent_attitude')
        expected = """2,0,0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0
2,1,0,1, 1, 1, 1, 1, 1, 1, 1, 1, 1
2,2,0,2, 2, 2, 2, 2, 2, 2, 2, 2, 2
2,3,0,3, 3, 3, 3, 3, 3, 3, 3, 3, 3
"""
        with open(file_to_write, 'r') as f:
            file_contents = f.read()
            # print(file_contents, file=sys.stderr)
            assert file_contents == expected

    @nose.with_setup(setup)
    def test_set_predecessors_for_each_node(self):
        self.test_network_agent.set_predecessors_for_each_node()
        calculated = {node.agent_id: node.predecessors
                      for node in self.test_network_agent.G}
        # print(self.test_network_agent.G.nodes(), file=sys.stderr)
        # print(calculated, file=sys.stderr)
        expected = {0: [],
                    1: [self.test_agent],
                    2: [self.test_agent],
                    3: [self.test_agent_1, self.test_agent_2]}
        # print(expected, file=sys.stderr)
        assert calculated == expected
