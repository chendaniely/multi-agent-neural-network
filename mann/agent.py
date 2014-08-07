#!/usr/bin/env python

from random import random

class Agent(object):
    '''
    This is the agent class.
    Agents are hashable so they can be used as nodes in a network
    from the networkx package
    '''

    # variable that tracks how many instances the Agent object is created
    agent_count = 0

    def __init__(self):
        # first agent created is agent 0XS
        self.agent_id = Agent.agent_count
        Agent.agent_count += 1

    def _random_state(self):
        '''
        generates a random state for the agent as it is created
        raises exception if state cannot be assign

        returns
        -------
        returns an integer value of 0 or 1 for a state
        '''
        random_float = random()
        if random_float < .5:
            return 0
        elif random_float >= .5:
            return 1
        else:
            return -1
            raise Exception("Error in _random_state")

    def set_predecessors(self, predecessors):
        self.predecessors = predecessors

    def __key(self):
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
        return self.__key()

    def __hash__(self):
        '''
        defines the hash function.
        the hash function hashes the __key()
        '''
        return hash(self.__key())

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

