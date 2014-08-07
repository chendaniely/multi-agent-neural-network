#! /usr/bin/env python

import network
import network_agent

def main():

    # creating n number of agents
    n = 20

    # container for agents (dictionary where the __key() is the key)
    agents = {}
    # probablity for edge creation [0, 1]
    p = 0.1

    for i in range(n):
        print("creating agent # ", i)
        new_agent = agent.Agent()
        print("agent ", new_agent.get_key(), " created")
        agents[new_agent.get_key()] = new_agent

    print('total number of agents created: ', new_agent.agent_count)

    G = nx.MultiDiGraph()
    G.add_edge(agents[0], agents[1])
    G.add_edge(agents[1], agents[2])
    G.add_edge(agents[2], agents[0])
    
    nx.draw(G)
    plt.show()

if __name__ == "__main__":
    print("Running")
    main()
