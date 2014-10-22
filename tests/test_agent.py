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
# Unit tests for the base Agent class
###############################################################################
def reset_agent():
    agent.Agent.agent_count = 0


@nose.with_setup(reset_agent)
def test_agent_get_key_single():
    # print("testing single agent creation", file=sys.stderr)
    test_agent = agent.Agent()
    assert test_agent.get_key() == 0


@nose.with_setup(reset_agent)
def test_agent_get_key_multiple():
    # print("testing multiple agent creation", file=sys.stderr)
    list_of_test_agents = []
    for i in range(10):
        test_multiple_agent = agent.Agent()
        list_of_test_agents.append(test_multiple_agent)
    assert list_of_test_agents[0].get_key() == 0
    assert list_of_test_agents[-1].get_key() == 9


@nose.with_setup(reset_agent)
def test_hash():
    test_agent = agent.Agent()
    assert test_agent.get_key() == 0
    assert test_agent.__hash__() == 0


@nose.with_setup(reset_agent)
def test_agent_eq_no():
    test_agent_1 = agent.Agent()
    test_agent_2 = agent.Agent()
    assert not test_agent_1 == test_agent_2


@nose.with_setup(reset_agent)
def test_agent_eq_yes():
    agent.Agent.agent_count = 5
    test_agent_1 = agent.Agent()
    agent.Agent.agent_count = 5
    test_agent_2 = agent.Agent()
    assert test_agent_1 == test_agent_2


@nose.with_setup(reset_agent)
def test_agent_set_state():
    test_agent = agent.Agent()
    try:
        test_agent.set_state(1)
    except agent.BaseAgentStateError:
        assert True
    else:
        assert False


@nose.with_setup(reset_agent)
def test_agent_get_state():
    test_agent = agent.Agent()
    try:
        test_agent.get_state()
    except agent.BaseAgentStateError:
        assert True
    else:
        assert False


@nose.with_setup(reset_agent)
def test_agent_set_predecessors_empty():
    test_agent = agent.Agent()
    test_agent.set_predecessors([])
    assert test_agent.predecessors == []


@nose.with_setup(reset_agent)
def test_agent_set_predecessors_list():
    test_agent = agent.Agent()
    test_agent.set_predecessors([1, 3, 5])
    assert test_agent.predecessors == [1, 3, 5]


@nose.with_setup(reset_agent)
def test_agent_set_predecessors_network_agent():
    list_of_predecessors = []
    for i in range(3):
        agent_predecessor = agent.Agent()
        list_of_predecessors.append(agent_predecessor)

    test_agent = agent.Agent()
    assert test_agent.get_key() == 3

    test_agent.set_predecessors(list_of_predecessors)
    assert test_agent.predecessors[0].get_key() == 0
    assert test_agent.predecessors[-1].get_key() == 2


@nose.with_setup(reset_agent)
def test_has_predessor_empty():
    test_agent = agent.Agent()
    test_agent.set_predecessors([])
    assert test_agent.has_predessor() is False


@nose.with_setup(reset_agent)
def test_has_predessor_list():
    test_agent = agent.Agent()
    test_agent.set_predecessors([1, 3, 5])
    assert test_agent.has_predessor() is True


@nose.with_setup(reset_agent)
def test_has_predessor_network_agent():
    list_of_predecessors = []
    for i in range(3):
        agent_predecessor = agent.Agent()
        list_of_predecessors.append(agent_predecessor)

    test_agent = agent.Agent()
    assert test_agent.get_key() == 3

    test_agent.set_predecessors(list_of_predecessors)
    assert test_agent.has_predessor() is True

    test_agent_no_predecessor = agent.Agent()
    assert test_agent_no_predecessor.has_predessor() is False


@nose.with_setup(reset_agent)
def test_seed_agent():
    test_agent = agent.Agent()
    try:
        test_agent.seed_agent()
    except agent.BaseAgentSeedError:
        assert True
    else:
        assert False


@nose.with_setup(reset_agent)
def test_update_agent_state():
    test_agent = agent.Agent()
    try:
        test_agent.update_agent_state()
    except agent.BaseAgentUpdateStateError:
        assert True
    else:
        assert False
