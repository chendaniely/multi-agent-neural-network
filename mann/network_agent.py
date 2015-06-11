#! /usr/bin/env python

import random
import networkx as nx
import matplotlib.pyplot as plt
import re
import logging

import mann.agent
import mann.agent_binary


class NetworkAgent(object):
    def __init__(self):
        pass

    def __eq__(self, x, y):
        return x.agent_id == y.agent_id

    def create_multidigraph_of_agents_from_edge_list(
            self, number_of_agents, edge_list, fig_path,
            agent_type=tuple(['None']), logger=None, **kwargs):
        """Create multi directed networkx graph of agents from an edge list

        :param num_of_agents: number of agents in the network
        :type num_of_agents: int

        :param edge_list: edge list of network
        :type edge_list: iterable

        :param fig_path: figure path of output network image
        :type fig_path: str

        :param agent_type: type of agent, binary or lens
        :type agent_type: tuple

        :param logger: logger object, not used
        :type logger: None

        :param **kwargs: kwargs used for lens agent creation
        :type **kwargs: dict
        """
        logging.info('In mann.network_agent.'
                     'create_multidigraph_of_agents_from_edge_list()')

        # create the graph
        self.G = nx.MultiDiGraph()

        # dictonary container for agents, key values will be the agent.get_key
        all_agents = {}

        for i in range(number_of_agents):
            logging.info("creating agent # {}".format(i))

            # createing the different types of agents for the network
            if agent_type[0] == 'binary':
                new_agent = mann.agent_binary.BinaryAgent(agent_type[1])
            elif agent_type[0] == 'lens':
                if agent_type[2] == 'feed_forward_global_cascade':
                    new_agent = agent.LensAgent(agent_type[1])
                    new_agent.create_weight_file(kwargs.get('weight_in_file'),
                                                 kwargs.get('weight_dir'),
                                                 kwargs.get('base_example'),
                                                 kwargs.get(
                                                     'num_train_examples'),
                                                 kwargs.get(
                                                     'prototype_mutation_prob'),
                                                 kwargs.get(
                                                     'training_criterion'))
                elif agent_type[2] == 'recurrent_attitude':
                    # nothing really happens after the agent gets created
                    # this is more of a place holder for later training
                    # procedures
                    new_agent = agent_lens_recurrent.LensAgentRecurrent(
                        agent_type[1])
                else:
                    raise ValueError('Unknown Lens Agent Type')
            else:
                raise mann.agent.UnknownAgentTypeError(
                    'Unknown agent specified as nodes for network')

            logging.info("agent {} created: type: {}".
                         format(new_agent.get_key(), type(new_agent)))
            logging.info("agent {} state: {}".
                         format(new_agent.get_key(), str(new_agent.state)))
            logging.info("agent {} threshold: {}".
                         format(new_agent.get_key(), str(new_agent.threshold)))

            all_agents[new_agent.agent_id] = new_agent


        logging.info('total number of agents created: {}'.
                     format(new_agent.agent_count))

        self.G.add_nodes_from(all_agents.values())
        logging.info('number of nodes created: {}'.format(len(self.G)))

        logging.info('Creating edges')
        for edge in edge_list:
            u, v = edge
            self.G.add_edge(all_agents[u], all_agents[v])

        logging.info('Saving plot of mann copied graph')
        nx.draw_circular(self.G)
        # plt.show()
        plt.savefig(fig_path)

        return self.G

    def export_edge_list(self, export_file_dir, **kwargs):
        nx.write_edgelist(self.G, export_file_dir, **kwargs)

    def set_predecessors_for_each_node(self):
        # iterate through all nodes in network
        for node_agent in self.G.nodes_iter():
            # look up the predessors for each node
            predecessors = self.G.predecessors(node_agent)
            # since the nodes are an Agent class we can
            # assign the predecessors agent instance variable to the iter
            node_agent.set_predecessors(predecessors)
            logging.info('Agent {} predecessors assigned'.
                         format(node_agent.agent_id))
            print(node_agent.predecessors)

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
        rep = {"[": "", "]": "", "(": "", ")": ""}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        text = pattern.sub(lambda m: rep[re.escape(m.group(0))],
                           str(list_to_str))
        return text

    def update_simultaneous(self, num_agents_update, pick,
                            update='simultaneous'):
        assert isinstance(num_agents_update, int)
        agents_for_update = self.sample_network(num_agents_update)

        logging.info('Num agents for update: {}'.
                     format(len(agents_for_update)))

        # assign new temp value
        for selected_agent in agents_for_update:
            logging.info('Updating: {}'.
                         format(self.G.nodes()[selected_agent.agent_id]))
            assert selected_agent.temp_new_state is None
            selected_agent.update_agent_state(update, pick)

        # assign new temp value as final state simultaneous update
        logging.info('Performing simultaneous update')
        for selected_agent in agents_for_update:
            if selected_agent.temp_new_state == 1:
                logging.info('Update agent {}: setting state to {}, was {}'.
                             format(selected_agent.agent_id,
                                    selected_agent.temp_new_state,
                                    selected_agent.state))
                assert selected_agent.temp_new_state is not None
                selected_agent.state = selected_agent.temp_new_state
                selected_agent.num_update += 1
            else:
                logging.info('Agent {}: No state change to {}, was {}'.
                             format(selected_agent.agent_id,
                                    selected_agent.temp_new_state,
                                    selected_agent.state))
            selected_agent.temp_new_state = None

    def update_sequential(self, num_agent_update):
        pass

    def write_network_agent_step_info(self, time_step, file_to_write,
                                      file_mode, agent_type):
        """Write agent info for each time step

        Writes the following information respectively for binary agent
        - time step
        - agent id
        - total number of updates
        - update state for this time step
        - agent state at end of time

        Writes the following information respectively for lens agent
        - time step
        - agent id
        - total number of updates
        - update state for this time step
        - infl agent ID
        - agent state at end of time
        - input agent state
        - lens target
        - prototype
        """
        with open(file_to_write, mode=file_mode, encoding='utf-8') as f:
            for node in self.G.__iter__():
                if agent_type == 'binary':
                    f.write(",".join([
                        str(time_step),  # time step
                        str(node.agent_id),  # agent ID
                        str(node.num_update),  # total num updates
                        str(node.step_update_status),  # update state
                        # str(node.step_input_agent_id),  # infl ID
                        # agent state
                        self.str_list_with_out_brackets(node.state)
                        # input state
                        # self.str_list_with_out_brackets(
                        #     node.step_input_state_values),
                    ]) + "\n")

                elif agent_type == 'lens':
                    f.write(",".join([
                        str(time_step),  # time step
                        str(node.agent_id),  # agent ID
                        str(node.num_update),  # total num updates
                        str(node.step_update_status),  # update state
                        str(node.step_input_agent_id),  # infl ID
                        # agent state
                        self.str_list_with_out_brackets(node.state),
                        # input state
                        self.str_list_with_out_brackets(
                            node.step_input_state_values),
                        # lens target
                        self.str_list_with_out_brackets(node.step_lens_target),
                        # prototype
                        self.str_list_with_out_brackets(node.prototype)
                    ]) + "\n")
                node.reset_step_variables()
