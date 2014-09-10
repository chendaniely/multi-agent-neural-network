#! /usr/bin/env python

import nose
import sys
import io
from mann import agent


#####################################
# Unit tests for the base Agent class
#####################################
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
    agent.Agent.agent_count = 0
    for i in range(10):
        test_multiple_agent = agent.Agent()
        list_of_test_agents.append(test_multiple_agent)
    assert list_of_test_agents[0].get_key() == 0
    assert list_of_test_agents[-1].get_key() == 9


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
    '''
    TODO: implement unit test where predecessors are other agents
    '''
    pass


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
    '''
    TODO implement unit test where predecessors are other agents
    '''
    pass


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


#################
# Unit Test notes
#################
# To write to 'file', write to StringIO
# use getvalue() to get and check its final contents
# writer.getvalue()
# nose.assert_almost_equals()
Data = '''0 0 1 1
1 0 2 1
2 0 3 1
'''


def count_lines_in(reader):
    count = 0
    for line in reader:
        count += 1
    return count


def count_lines(filename):
    reader = open(filename, 'r')
    reader.close()
    result = count_rect_in(reader)
    return result


def test_count_lines():
    # print("testing count lines", file=sys.stderr)
    reader = io.StringIO(Data)
    assert count_lines_in(reader) == 3


# Fixtures
# something we run a test on
# nose has a function called setup
# will be run before any of the tests
# use nose.with_setup to apply the
# function before each test
