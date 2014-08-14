#!/usr/bin/env python

import random


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
        where equality is defined by the __key() values
        '''
        return x.__key() == y.key()

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
        raise BaseAgentStateError('Base agent class has no state')

    def set_predecessors(self, predecessors):
        '''
        returns
        -------
        a list of predecessors
        '''
        self.predecessors = predecessors

    def has_predessor(self):
        if len(self.predecessors) == 0:
            return False
        else:
            return True

    def seed_agent(self):
        raise BaseAgentSeedError('Base agent class cannot be seeded')

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
        assert(value in (0, 1),
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

    def _update_agent_binary_state_1(self):
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

    def update_agent_binary_state(self, pick='1'):
        '''
        pick = '1': uses the update_agent_binary_state_1 algorithm
        '''
        print('in update_agent_binary_state')
        print('has predecessors', self.has_predessor())
        if self.has_predessor():
            if pick == '1':
                self._update_agent_binary_state_1()
            else:
                raise ValueError("algorithm used for pick unknown")
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

    def list_to_str_delim(list_to_convert, delim):
        return delim.join(map(str, list_to_convert))

    def write_agent_state_to_ex(file_dir):
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

            lens_agent_state_str = list_to_str_delim(self.state, " ")
            input_line = 'I: ' + lens_agent_state_str + ' ;'
            f.write(input_line)
