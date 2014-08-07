#! /usr/bin/env python

import network
import network_agent

def main():

    # creating n number of agents
    n = 20

    # probablity for edge creation [0, 1]
    p = 0.1


    G = nx.MultiDiGraph()
    G.add_edge(agents[0], agents[1])
    G.add_edge(agents[1], agents[2])
    G.add_edge(agents[2], agents[0])
    

if __name__ == "__main__":
    print("Running")
    main()
