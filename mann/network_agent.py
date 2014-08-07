#! /usr/bin/env python

import agent
import networkx as nx
import matplotlib.pyplot as plt

class NetworkAgent(object):
    def __init__(self):
        pass

    def create_multidigraph_of_agents_from_edge_list(self, number_of_agents, edge_list):
        # create the graph
        G = nx.MultiDiGraph()
        
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
            G.add_edge(all_agents[u], all_agents[v])

        nx.draw_circular(G)
        plt.show()

        return G
