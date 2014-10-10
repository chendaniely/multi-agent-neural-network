#!/usr/bin/env python

import random
import subprocess
import io
import os


class Error(Exception):
    '''Base class for other exceptions'''
    def __init__(self, message):
        print(message)


class BaseAgentStateError(Error):
    '''Raised when the get_state method is called from the Agent class'''


class BaseAgentSeedError(Error):
    '''Raised when the seed_agent method is called from the Agent class'''


class BaseAgentUpdateStateError(Error):
    '''Raised when the update_agent_state method
    is called from the Agent class'''


class Agent(object):
    '''
    This is the agent class.
    Agents are hashable so they can be used as nodes in a network
    from the networkx package
    '''

    # variable that tracks how many instances the Agent object is created
    agent_count = 0

    def __init__(self):
        # first agent created is agent 0
        self.agent_id = Agent.agent_count
        Agent.agent_count += 1
        self.predecessors = []

    def __hash__(self):
        '''
        defines the hash function.
        the hash function hashes the _key()
        '''
        return hash(self._key())

    def __eq__(x, y):
        '''
        equality method
        used to implement whether 2 agents are the same
        where equality is defined by the get_key() values
        '''
        return x.get_key() == y.get_key()

    def __repr__(self):
        return str(self.__class__.__name__) + ", key: " + str(self.get_key())

    def __str__(self):
        return "A" + str(self.get_key())

    def _key(self):
        '''
        method that returns a tuple of the unique vales of the agent.
        this tuple is then used to hash and do comparisons.

        parameters
        ----------
        none

        return
        ------
        a tuple that represents the unique keys of the agent
        '''
        return self.agent_id

    def get_key(self):
        return self._key()

    def set_state(self, new_state):
        raise BaseAgentStateError('Base agent class has no state')

    def get_state(self):
        raise BaseAgentStateError('Base agent class has no state')

    def set_predecessors(self, list_of_predecessors):
        '''
        Takes a list of predecessors and assigns the list to self.predecessors

        parameters
        ----------
        a lit of predecessors

        returns
        -------
        none
        '''
        self.predecessors = list_of_predecessors

    def has_predessor(self):
        if len(self.predecessors) == 0:
            return False
        else:
            return True

    def seed_agent(self):
        raise BaseAgentSeedError('Base agent class cannot be seeded')

    def update_agent_state(self):
        raise BaseAgentUpdateStateError(
            'Base agent class has no state to update')

#    def get_agent_step_info(self):
#        '''
#        THIS FUNCTION IS NOT USED
#        returns
#        -------
#        a dictionary of values to be saved on each step of a model run
#        '''
#        return {
#            'key': self.get_key(),
#            'binary_state': self.binary_state
#        }


class BinaryAgent(Agent):
    binary_agent_count = 0

    def __init__(self):
        self.agent_id = BinaryAgent.binary_agent_count
        BinaryAgent.binary_agent_count += 1
        self.binary_state = 0
        self.predecessors = []

    def set_binary_state(self, value):
        # binary state means 0 or 1
        assert value in [0, 1],\
            "binary state can only be 0 or 1, got %r" % value

        # make sure we are only changing the state when the value is different
        assert value != self.binary_state, "changing state to same value"

        self.binary_state = value

    def get_state(self):
        return self.binary_state

    def seed_agent(self):
        self.set_binary_state(1)

    def random_binary_state(self):
        '''
        generates a random state for the agent as it is created
        raises exception if state cannot be assign

        returns
        -------
        returns an integer value of 0 or 1 for a state
        '''
        random_float = random.random()
        if random_float < .5:
            return 0
        elif random_float >= .5:
            return 1
        # else:
        #     return -1
        #     raise Exception("Error in _random_state")

    def _update_agent_state_default(self):
        '''
        Looks at the list of predessors for the selected agent
        randomly picks one of them
        if the selected predessor is has a different state
        there will be a 70% chance that the selected agent will change states
        to match the predessor's state
        otherwise no state is changed
        '''
        print('in _update_agent_state_default')
        print("type of predecssors: ",  type(self.predecessors))  # list
        print("container of predessors: ", self.predecessors)
        predecessor_picked = random.sample(list(self.predecessors), 1)[0]
        print("predecessor picked: ", predecessor_picked)
        print("predecessor picked key: ", predecessor_picked.get_key())
        if self.binary_state == predecessor_picked.binary_state:
            print("no update required, binary states are the same")
            print("self.binary_state = ", self.binary_state)
            print("predecessor_picked.binary_state = ",
                  predecessor_picked.binary_state)
            pass
        else:
            print('updateing agent state')
            random_number = random.random()
            if random_number < 0.7:
                self.set_binary_state(predecessor_picked.binary_state)
            else:
                pass

    def update_agent_state(self, pick='default'):
        '''
        pick = 'default': uses the update_agent__state_default algorithm
        '''
        print('in update_agent_state')
        print('has predecessors', self.has_predessor())
        if self.has_predessor():
            if pick == 'default':
                self._update_agent_state_default()
            else:
                raise ValueError("Algorithm used for pick unknown")
        else:
            pass


class LensAgent(Agent):
    lens_agent_count = 0

    def __init__(self, num_state_vars):
        '''
        num_state_vars is the total number of elements the agent has as a state
        for LENS, this is the total number of processing units per agent
        that is, the number of positive valence bank units
        and the number of negative valence bank units
        '''
        self.agent_id = LensAgent.lens_agent_count
        LensAgent.lens_agent_count += 1

        self.state = [0] * num_state_vars
        self.predecessors = []

    # def set_lens_agent_state(self, list_of_processing_unit_activations):
    #     print(len(list_of_processing_unit_activations))
    #     print(len(self.state))
    #     is_len_equal = len(list_of_processing_unit_activations) ==\
    #         len(self.state)

    #     print(is_len_equal)

    #     if():
    #         self.state = list_of_processing_unit_activations[:]
    #     else:
    #         raise ValueError("length of processing units to assign state\
    #                          not equal to lengh of state")

    def get_state(self):
        return self.state

    def _list_to_str_delim(self, list_to_convert, delim):
        '''
        takes in a list and returns a string of list by the delim
        used to write out agent state out to file
        '''
        return delim.join(map(str, list_to_convert))

    def seed_agent(self):
        self.state = [1] * len(self.state)

    def set_state(self, list_of_values):
        # sets state to list of values
        # list slicing is the fastest according to stackoverflow:
        # http://stackoverflow.com/questions/2612802/
        # how-to-clone-or-copy-a-list-in-python
        print('list of values length:', len(list_of_values))
        print('state length:', len(self.state))
        if len(list_of_values) == len(self.state):
            self.state = list_of_values[:]
        else:
            raise ValueError("len of values not equal to len of state")

    def _call_lens(self, lens_in_file):
        # pass
        subprocess.call(['lens', '-nogui',
                         lens_in_file])
        # '/home/dchen/Desktop/ModelTesting/MainM1PlautFix2.in'])

    def _start_end_update_out(self, f):
        # f is the .out file to be read
        return tuple([80, 84, 86, 90])

    def _get_new_state_values_from_out_file(self, file_dir):
        list_of_new_state = []

        here = os.path.abspath(os.path.dirname(__file__))
        read_file_path = here + '/' + file_dir

        with open(read_file_path, 'r') as f:
            start_bank1, end_bank1, start_bank2, end_bank2 = \
                self._start_end_update_out(f)
            for line_idx, line in enumerate(f):
                line_num = line_idx + 1  # python starts from line 0
                if start_bank1 <= line_num <= end_bank1 or \
                   start_bank2 <= line_num <= end_bank2:
                    # in a line that I want to save information for
                    first_col = line.strip().split(' ')[0]
                    list_of_new_state.append(float(first_col))
        return list_of_new_state

    def _update_agent_state_default(self, agent_ex_file, infl_ex_file,
                                    agent_state_out_file):
        if len(self.predecessors) > 0:
            predecessor_picked = random.sample(list(self.predecessors), 1)[0]
            # predecessor_picked.write_agent_state_to_ex('../tests/lens/infl.ex')
            predecessor_picked.write_agent_state_to_ex(infl_ex_file)
            # self.write_agent_state_to_ex('../tests/lens/agent.ex')
            self.write_agent_state_to_ex(agent_ex_file)
            self._call_lens()
            # self.new_state_values = self._get_new_state_values_from_out_file(
            #     '../tests/lens/AgentState.out')
            self.new_state_values = self._get_new_state_values_from_out_file(
                agent_state_out_file)

            self.set_state(self.new_state_values)
        else:
            print('no predecessors')
            pass

    def update_agent_state(self, pick='default'):
        if pick == 'default':
            self._update_agent_state_default()
        else:
            raise ValueError('Algorithm used for pick unknown')

    def _string_agent_state_to_ex(self):
        output = io.StringIO()
        output.write('name: sit1\n')
        lens_agent_state_str = self._list_to_str_delim(self.state, " ")
        input_line = 'I: ' + lens_agent_state_str + ' ;\n'
        output.write(input_line)
        contents = output.getvalue()
        output.close()
        print(contents)
        return contents

    def write_agent_state_to_ex(self, file_dir):
        '''
        file_dir should be in the ./tests/lens/ folder
        usually the file will be something like
        agent.ex for the agent or
        infl.ex for the influencing agent
        '''

        here = os.path.abspath(os.path.dirname(__file__))
        write_file_path = here + '/' + file_dir
        print(here)
        print(write_file_path)
        with open(write_file_path, 'w') as f:
            '''
            should look something like this:
            name: sit1
            I: 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ;
            '''
            f.write('name: sit1\n')

            lens_agent_state_str = self._list_to_str_delim(self.state, " ")
            input_line = 'I: ' + lens_agent_state_str + ' ;'
            f.write(input_line)
