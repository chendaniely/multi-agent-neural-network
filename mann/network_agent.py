#! /usr/bin/env python

import agent
import random
import networkx as nx
import matplotlib.pyplot as plt

class NetworkAgent(object):
    def __init__(self):
        pass

    def create_multidigraph_of_agents_from_edge_list(self, number_of_agents, edge_list):
        # create the graph
        self.G = nx.MultiDiGraph()
        
        # dictonary container for agents, key values will be the agent.get_key
        all_agents = {}

        # create all the agents
        for i in range(number_of_agents):
            print("creating agent # ", i)
            new_agent = agent.Agent()
            print("agent ", new_agent.get_key(), " created")
            all_agents[new_agent.get_key()] = new_agent
            
        print('total number of agents created: ', new_agent.agent_count)

        for edge in edge_list:
            u , v = edge
            self.G.add_edge(all_agents[u], all_agents[v])

        nx.draw_circular(self.G)
        plt.show()

        return self.G

    def set_predecessors_for_each_node(self):
        # iterate through all nodes in network
        for node_agent in self.G.nodes_iter():
            # look up the predessors for each node
            predecessors = self.G.predecessors_iter(node_agent)            
            # since the nodes are an Agent class we can
            # assign the predecessors agent instance variable to the iter
            node_agent.set_predecessors(predecessors)

    def sample_network(self, number_of_agents_to_sample):
        '''
        From the random.sample documentation:
        Return a k length list of unique elements chosen from the population sequence or set.
        Used for random sampling without replacement.
        '''
        agents_picked = random.sample(self.G.nodes(), number_of_agents_to_sample)
        return agents_picked

    def write_network_agent_step_info(self, time_step, file_to_write, file_mode):
        with open(file_to_write, mode=file_mode, encoding='utf-8') as f:
             for node in self.G.__iter__():
                 f.write(str(time_step) +
                         "," +
                         str(node.get_key()) +
                         "," +
                         str(node.binary_state) + "\n")
