#! /usr/bin/env python

import network
import network_agent


def random_select_and_update(network_of_agents):
    n = len(network_of_agents.G)

    # randomly select nodes from network_of_agents
    # select 10% of the nodes for update, performs floor division
    num_update = n // 10
    agents_for_update = network_of_agents.sample_network(num_update)
    print(agents_for_update)

    print(network_of_agents.G.nodes()[agents_for_update[0].get_key()])

    # update agents who were selected
    for selected_agent in agents_for_update:
        print("updating: ",
              network_of_agents.G.nodes()[selected_agent.get_key()])
        print('pre-update binary_state', selected_agent.binary_state)
        selected_agent.update_agent_binary_state()
        print('post-update_agent_binary_state', selected_agent.binary_state)


def step(time_tick, network_of_agents):
    random_select_and_update(network_of_agents)
    network_of_agents.write_network_agent_step_info(
        time_tick, '../output/network_of_agents.pout', 'a')


def main():

    # creating n number of agents
    n = 20

    # probablity for edge creation [0, 1]
    p = 0.1

    # Create Erdos-Renyi graph
    my_network = network.DirectedFastGNPRandomGraph(n, p)
    print("network edge list to copy\n", my_network.G.edges())  # edge list
    print(my_network.G.edges_iter())
    my_network.show_graph('../output/mann-generated.png')

    network_of_agents = network_agent.NetworkAgent()
    network_of_agents.create_multidigraph_of_agents_from_edge_list(
        n, my_network.G.edges_iter())
    network_of_agents.write_network_agent_step_info(
        -1, '../output/network_of_agents.pout', 'w')

    # make agents aware of predecessors
    # predecessors are agents who influence the current agent
    network_of_agents.set_predecessors_for_each_node()

    # randomly select nodes from network_of_agents to seed
    num_seed = 5
    agents_to_seed = network_of_agents.sample_network(num_seed)
    print("agents to seed: ", agents_to_seed)

    # seed agents who were select
    for selected_agent in agents_to_seed:
        print("seeding: ",
              network_of_agents.G.nodes()[selected_agent.get_key()])
        print('pre-seed binary_state', selected_agent.binary_state)
        selected_agent.set_binary_state(1)
        print('post-seed_agent_binary_state', selected_agent.binary_state)

    for i in range(1000):
        print("STEP # ", i)
        step(i, network_of_agents)

if __name__ == "__main__":
    print("Running")
    main()
