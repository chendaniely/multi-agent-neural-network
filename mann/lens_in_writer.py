#! /usr/bin/env/python
"""This module contains the LensInWriter class that is used to write the
various .in files used to interface with LENS
"""

import re

# from mann import helper


class LensInWriterHelper(object):
    def __init__(self):
        pass

    def clean_agent_state_in_file(self, agent_id_str, agent_state):
        """Generate a string to be used as an update step for LENS agents
        that are using a recurrent network for the attitude model
        generalized form of `generate_lens_recurrent_attitude`
        takes an agent state and returns a space separated string

        :param agent_id_str: string representation of agent ID,
        this is so something like 'tminus1' can be passed to show the current
        agent marked for update, can be delimited by commas or spaces
        :type agent_id_str: str

        :param agent_state: string representation of a list w/outt the brackets
        :type agent_state: str

        should return a string like this: (the -1 shows this is the agent that
        was marked for update)
        name: agent1-1
        I: 0 0 0 0 0 1 1 1 1 1

        or
        name: agent42
        I: 1 1 1 1 1 0 0 0 0 0
        """
        # if comma separated, make it space separated
        agent_state_clean = re.sub(',\s+', ' ', agent_state)
        string = "name: agent{}\nI: {}\n".\
                 format(agent_id_str, agent_state_clean)
        return(string)

    def generate_lens_recurrent_attitude(self, agent_state, infl_state):
        """Generate a string to be used as an update step for LENS agents
        that are using a recurrent network for the attitude model

        :param agent_state: comma delimited string of agent state values
        :type agent_state: str

        :param infl_state: comma delimited string of the infl agent state
        :type infl_state: str

        :returns string: a string that can be used to write a .in file
        :rtype: str

        should return something like this:
        name: tminus1
        I: 0 0 0 0 0 1 1 1 1 1;
        name: update1
        I: 1 1 1 1 1 0 0 0 0 0;
        """
        agent_state_clean = re.sub(',\s+', ' ', agent_state)
        infl_state_clean = re.sub(',\s+', ' ', infl_state)
        string = "name: agent_state\nI: {};\nname: infl1\nI: {};\n".\
                 format(agent_state_clean, infl_state_clean)
        return(string)

    def write_in_file(self, file_dir, string):
        """Writes a given string to the given file_dir
        """
        with open(file_dir, 'w') as f:
            f.write(string)
