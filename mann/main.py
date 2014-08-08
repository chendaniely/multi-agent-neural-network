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

    # randomly select nodes from network_of_agents
    s = n // 10 # select 10% of the nodes for update, performs floor division
    agents_for_update = network_of_agents.sample_network(s)
    print(agents_for_update)
    
    print(network_of_agents.G.nodes()[agents_for_update[0].get_key()])
    # randomly select nodes from network_of_agents to seed
    num_seed = 1
    agents_to_seed = network_of_agents.sample_network(num_seed)
    print("agents to seed: ", agents_to_seed)

    # seed agents who were select
    for selected_agent in agents_to_seed:
        print("seeding: ", network_of_agents.G.nodes()[selected_agent.get_key()])
        print('pre-seed binary_state', selected_agent.binary_state)
        selected_agent.set_binary_state(1)
        print('post-seed_agent_binary_state', selected_agent.binary_state)

if __name__ == "__main__":
    print("Running")
    main()
