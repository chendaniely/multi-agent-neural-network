#! /usr/bin/env python
###############################################################################
import nose
import sys
import io
import random
import os
import glob
import pdb
import subprocess
import numpy.testing

from mann import agent

here = os.path.abspath(os.path.dirname(__file__))

###############################################################################
# Unit tests for the BinaryAgent class
###############################################################################
def reset_BinaryAgent():
    agent.BinaryAgent.binary_agent_count = 0


@nose.with_setup(reset_BinaryAgent)
def test_binary_agent_get_key_single():
    test_binary_agent = agent.BinaryAgent()
    assert test_binary_agent.get_key() == 0


@nose.with_setup(reset_BinaryAgent)
def test_binary_agent_get_key_multiple():
    list_of_test_binary_agents = []
    for i in range(10):
        test_multiple_binary_agent = agent.BinaryAgent()
        list_of_test_binary_agents.append(test_multiple_binary_agent)
    assert list_of_test_binary_agents[0].get_key() == 0
    assert list_of_test_binary_agents[-1].get_key() == 9


@nose.with_setup(reset_BinaryAgent)
def test_binary_agent_set_state():
    test_binary_agent = agent.BinaryAgent()
    assert test_binary_agent.get_state() == 0

    test_binary_agent.set_binary_state(1)
    assert test_binary_agent.get_state() == 1

    test_binary_agent.set_binary_state(0)
    assert test_binary_agent.get_state() == 0

    try:
        test_binary_agent.set_binary_state(3)
    except:
        assert True
    else:
        assert False


@nose.with_setup(reset_BinaryAgent)
def test_binary_agent_seed():
    test_binary_agent = agent.BinaryAgent()
    assert test_binary_agent.get_state() == 0

    test_binary_agent.seed_agent()
    assert test_binary_agent.get_state() == 1


@nose.with_setup(reset_BinaryAgent)
def test_binary_agent_seed_random():
    '''
    In [1]: random.seed(1)

    In [2]: random.random()
    Out[2]: 0.13436424411240122

    In [3]: random.random()
    Out[3]: 0.8474337369372327
    '''
    random.seed(1)
    test_binary_agent = agent.BinaryAgent()
    random_seed = test_binary_agent.random_binary_state()
    assert random_seed == 0

    test_binary_agent = agent.BinaryAgent()
    random_seed = test_binary_agent.random_binary_state()
    assert random_seed == 1


@nose.with_setup(reset_BinaryAgent)
def test_binary_agent_update_agent_state():
    '''
    In [1]: random.seed(1)

    In [2]: random.sample([1,2,3], 1)
    Out[2]: [1]

    In [3]: random.random()
    Out[3]: 0.5692038748222122

    In [4]: random.sample([1,2,3], 1)
    Out[4]: [1]

    In [5]: random.random()
    Out[5]: 0.2550690257394217

    In [6]: random.sample([1,2,3], 1)
    Out[6]: [2]

    In [7]: random.random()
    Out[7]: 0.7609624449125756
    '''
    test_binary_agent = agent.BinaryAgent()
    assert test_binary_agent.get_state() == 0
    test_binary_agent.update_agent_state()

    list_binary_agents_for_predecessor = []
    for i in range(3):
        test_binary_agent_predecessor = agent.BinaryAgent()
        list_binary_agents_for_predecessor.append(
            test_binary_agent_predecessor)
    test_binary_agent.set_predecessors(list_binary_agents_for_predecessor)
    list_binary_agents_for_predecessor[0].set_binary_state(1)

    random.seed(1)
    test_binary_agent.update_agent_state()
    assert test_binary_agent.get_state() == 1

    test_binary_agent.update_agent_state()
    assert test_binary_agent.get_state() == 1

    test_binary_agent.update_agent_state()
    assert test_binary_agent.get_state() == 0


@nose.with_setup(reset_BinaryAgent)
def test_binary_agent_update_agent_state_fail():
    test_binary_agent = agent.BinaryAgent()
    assert test_binary_agent.get_state() == 0
    test_binary_agent.update_agent_state()

    list_binary_agents_for_predecessor = []
    for i in range(3):
        test_binary_agent_predecessor = agent.BinaryAgent()
        list_binary_agents_for_predecessor.append(
            test_binary_agent_predecessor)
    test_binary_agent.set_predecessors(list_binary_agents_for_predecessor)
    list_binary_agents_for_predecessor[0].set_binary_state(1)

    try:
        test_binary_agent.update_agent_state(pick='fail')
    except ValueError:
        assert True
    else:
        assert False