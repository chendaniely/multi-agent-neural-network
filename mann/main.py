#! /usr/bin/env python

import network
import network_agent

def main():

    # creating n number of agents
    n = 20

    # probablity for edge creation [0, 1]
    p = 0.1

    # Create Erdos-Renyi graph
    my_network = network.DirectedFastGNPRandomGraph(n, p)
    print(my_network.G.edges()) # edge list
    print(my_network.G.edges_iter())
    my_network.show_graph()
    
    network_of_agents = network_agent.NetworkAgent()
    network_of_agents.create_multidigraph_of_agents_from_edge_list(n, my_network.G.edges_iter())

    # make agents aware of predecessors
    # predecessors are agents who influence the current agent
    network_of_agents.set_predecessors_for_each_node()

if __name__ == "__main__":
    print("Running")
    main()
