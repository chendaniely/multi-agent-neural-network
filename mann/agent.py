#!/usr/bin/env python

import random
import subprocess


class Error(Exception):
    '''Base class for other exceptions'''
    def __init__(self, message):
        print(message)


class BaseAgentStateError(Error):
    '''Raised when the get_state method is called from the Agent class'''
    def __init__(self):
        print('Base agent class has no state')


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

    def __hash__(self):
        '''
        defines the hash function.
        the hash function hashes the __key()
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

    def get_state(self):
        raise BaseAgentStateError

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

    def set_binary_state(self, value):
        # binary state means 0 or 1
        assert(value in [0, 1],
               "binary state can only be 0 or 1, got %r" % value)

        # make sure we are only changing the state when the value is different
        assert(value != self.binary_state)

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
        else:
            return -1
            raise Exception("Error in _random_state")

    def _update_agent_state_default(self):
        print('in _update_agent_binary_state_1')
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

    def update_agent_state(self, pick):
        '''
        pick = '1': uses the update_agent_binary_state_1 algorithm
        '''
        print('in update_agent_binary_state')
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
        self.agent_id = LensAgent.lens_agent_count
        LensAgent.lens_agent_count += 1

        self.state = [None] * num_state_vars

    def set_lens_agent_state(list_of_processing_unit_activations):
        self.state = list_of_processing_unit_activations

    def get_state(self):
        return self.state

    def _list_to_str_delim(self, list_to_convert, delim):
        return delim.join(map(str, list_to_convert))

    def seed_agent(self):
        self.state = [1] * len(self.state)

    def set_agent_state(self, list_of_values):
        # sets state to list of values
        # list slicing is the fastest according to stackoverflow:
        # http://stackoverflow.com/questions/2612802/
        # how-to-clone-or-copy-a-list-in-python
        self.state = list_of_values[:]

    def _call_lens(self):
        pass
        # subprocess.call(['lens', '-nogui',
        #                 '/home/dchen/temp/lens/MainM1.in'])

    def _start_end_update_out(self, f):
        # f is the .out file to be read
        return tuple([80, 84, 86, 90])

    def _get_new_state_values_from_out_file(self):
        list_of_new_state = []
        with open('../temp/AgentState.out', 'r') as f:
            start_bank1, end_bank1, start_bank2, end_bank2 = \
                self._start_end_update_out(f)
            for line_idx, line in enumerate(f):
                line_num = line_idx + 1
                if start_bank1 <= line_num <= end_bank1 or \
                   start_bank2 <= line_num <= end_bank2:
                    # in a line that I want to save information for
                    first_col = line.strip().split(' ')[0]
                    list_of_new_state.append(first_col)
        return list_of_new_state

    def _update_agent_state_default(self):
        if len(self.predecessors) > 0:
            predecessor_picked = random.sample(list(self.predecessors), 1)[0]
            predecessor_picked.write_agent_state_to_ex('../temp/infl.ex')
            self.write_agent_state_to_ex('../temp/agent.ex')
            self._call_lens()
            self.new_state_values = self._get_new_state_values_from_out_file()
            self.set_agent_state(self.new_state_values)
        else:
            print('no predecessors')
            pass

    def update_agent_state(self, pick):
        if pick == 'default':
            self._update_agent_state_default()
        else:
            raise ValueError('Algorithm used for pick unknown')

    def write_agent_state_to_ex(self, file_dir):
        '''
        file_dir should be in the ../temp/ folder
        usually the file will be something like
        agent.ex for the agent or
        infl.ex for the influencing agent
        '''
        with open('../temp/agent.ex', 'w') as f:
            '''
            should look something like this:
            name: sit1
            I: 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ;
            '''
            f.write('name: sit1\n')

            lens_agent_state_str = self._list_to_str_delim(self.state, " ")
            input_line = 'I: ' + lens_agent_state_str + ' ;'
            f.write(input_line)
