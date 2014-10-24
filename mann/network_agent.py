#! /usr/bin/env python

import random
import networkx as nx
import matplotlib.pyplot as plt
import re

import mann.agent as agent


class NetworkAgent(object):
    def __init__(self):
        pass

    def create_multidigraph_of_agents_from_edge_list(
            self, number_of_agents, edge_list, agent_type=tuple(['None']),
            **kwargs):
        # create the graph
        self.G = nx.MultiDiGraph()

        # dictonary container for agents, key values will be the agent.get_key
        all_agents = {}

        # create all the agents
        for i in range(number_of_agents):
            print("creating agent # ", i)
            # createing the different types of agents for the network
            if agent_type[0] == 'binary':
                new_agent = agent.BinaryAgent()
            elif agent_type[0] == 'lens':
                new_agent = agent.LensAgent(agent_type[1])
                new_agent.create_weight_file(kwargs.get('weight_in_file'),
                                             kwargs.get('weight_dir'),
                                             kwargs.get('base_example'),
                                             kwargs.get('num_train_examples'),
                                             kwargs.get('num_train_mutations'))
            else:
                raise UnknownAgentTypeError(
                    'Unknown agent specified as nodes for network')

            print("agent ", new_agent.get_key(), " created",
                  "; type: ", type(new_agent))

            all_agents[new_agent.get_key()] = new_agent

        print('total number of agents created: ', new_agent.agent_count)

        self.G.add_nodes_from(all_agents.values())
        print('number of nodes created: ', len(self.G))

        for edge in edge_list:
            u, v = edge
            self.G.add_edge(all_agents[u], all_agents[v])

        nx.draw_circular(self.G)
        # plt.show()
        plt.savefig('./output/mann-copied.png')

        return self.G

    def set_predecessors_for_each_node(self):
        # iterate through all nodes in network
        for node_agent in self.G.nodes_iter():
            # look up the predessors for each node
            predecessors = self.G.predecessors(node_agent)
            # since the nodes are an Agent class we can
            # assign the predecessors agent instance variable to the iter
            node_agent.set_predecessors(predecessors)

    def sample_network(self, number_of_agents_to_sample):
        '''
        From the random.sample documentation:
        Return a k length list of unique elements
        chosen from the population sequence or set.
        Used for random sampling without replacement.
        '''
        agents_picked = random.sample(self.G.nodes(),
                                      number_of_agents_to_sample)
        return agents_picked

    def str_list_with_out_brackets(self, list_to_str):
        # reg ex str replace multiple
        # http://stackoverflow.com/questions/6116978/python-replace-multiple-strings
        # dict.iteritems() is a python 2 syntax
        # python 3 has dict.itemd()
        rep = {"[": "", "]": ""}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        text = pattern.sub(lambda m: rep[re.escape(m.group(0))],
                           str(list_to_str))
        return text

    def write_network_agent_step_info(self, time_step,
                                      file_to_write, file_mode):
        with open(file_to_write, mode=file_mode, encoding='utf-8') as f:
            for node in self.G.__iter__():
                f.write(str(time_step) +
                        "," +
                        str(node.get_key()) +
                        "," +
                        str(node.num_update) +
                        "," +
                        self.str_list_with_out_brackets(node.get_state()) +
                        # str(e) for e in list(node.get_state()) +
                        "\n")
