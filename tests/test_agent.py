#! /usr/bin/env python

import nose
import sys
import io
import random
import os
import pdb

from mann import agent


###############################################################################
# Unit tests for the base Agent class
###############################################################################
def reset_agent():
    agent.Agent.agent_count = 0


def reset_BinaryAgent():
    agent.BinaryAgent.binary_agent_count = 0


def reset_LensAgent():
    agent.LensAgent.lens_agent_count = 0


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


###############################################################################
# Unit tests for the BinaryAgent class
###############################################################################

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


###############################################################################
# Unit tests for the LensAgent class
###############################################################################
@nose.with_setup(reset_LensAgent)
def test_lens_agent_get_key_single():
    test_lens_agent = agent.LensAgent(4)
    assert test_lens_agent.get_key() == 0


@nose.with_setup(reset_LensAgent)
def test_lens_agent_get_key_multiple():
    list_of_test_agents = []
    for i in range(10):
        test_multiple_lens_agent = agent.LensAgent(4)
        list_of_test_agents.append(test_multiple_lens_agent)
    assert list_of_test_agents[0].get_key() == 0
    assert list_of_test_agents[-1].get_key() == 9


@nose.with_setup(reset_LensAgent)
def test_lens_agent_state_init():
    test_lens_agent = agent.LensAgent(4)
    assert test_lens_agent.get_state() == [0] * 4


@nose.with_setup(reset_LensAgent)
def test_lens_agent_set_get_state():
    test_lens_agent = agent.LensAgent(4)
    test_lens_agent.set_state([1, 2, 3, 4])
    assert test_lens_agent.get_state() == [1, 2, 3, 4]

    try:
        test_lens_agent.set_state([1, 2])
    except ValueError:
        assert test_lens_agent.get_state() == [1, 2, 3, 4]
        assert True
    else:
        assert False


@nose.with_setup(reset_LensAgent)
def test_list_to_str_delim():
    test_lens_agent = agent.LensAgent(4)
    expected_string = "1 3 5"
    output_string = test_lens_agent._list_to_str_delim([1, 3, 5], delim=" ")
    assert output_string == expected_string


@nose.with_setup(reset_LensAgent)
def test_lens_agent_seed():
    test_lens_agent = agent.LensAgent(4)
    assert test_lens_agent.get_state() == [0] * 4
    test_lens_agent.seed_agent()
    assert test_lens_agent.get_state() == [1] * 4


@nose.with_setup(reset_LensAgent)
def test_get_new_state_values_from_out_file():
    test_lens_agent = agent.LensAgent(10)
    here = os.path.abspath(os.path.dirname(__file__))
    agent_state_out_file_dir = here + '/' + 'lens/AgentState.out'
    calculated_state = test_lens_agent._get_new_state_values_from_out_file(
        agent_state_out_file_dir)
    expected_state = [1, 5, 0.333333, 0.333333, 0.333333,
                      0.333333, 5, 0, 0, 0]
    assert calculated_state == expected_state


@nose.with_setup(reset_LensAgent)
def test_write_agent_state_to_ex():
    pass


@nose.with_setup(reset_LensAgent)
def test_update_agent_state_default():
    pass


# TODO need to get LENS workign and set predessors to test
@nose.with_setup(reset_LensAgent)
def test_update_agent_state():
    list_of_predecessors = []
    for i in range(3):
        lens_agent_predecessor = agent.LensAgent(10)
        list_of_predecessors.append(lens_agent_predecessor)
    test_lens_agent = agent.LensAgent(10)
    assert test_lens_agent.get_key() == 3

    test_lens_agent.set_predecessors(list_of_predecessors)
    assert test_lens_agent.predecessors[0].get_key() == 0
    assert test_lens_agent.predecessors[-1].get_key() == 2

    here = os.path.abspath(os.path.dirname(__file__))
    lens_in_file_dir = here + '/' + 'lens/MainM1PlautFix2.in'
    agent_ex_file_dir = here + '/' + 'lens/AgentState.ex'
    infl_ex_file_dir = here + '/' + 'lens/infl.ex'
    agent_state_out_file_dir = here + '/' + 'lens/AgentState.out'

    test_lens_agent.update_agent_state(lens_in_file=lens_in_file_dir,
                                       # lens_agent_predecessor,
                                       agent_ex_file=agent_ex_file_dir,
                                       infl_ex_file=infl_ex_file_dir,
                                       agent_state_out_file=agent_state_out_file_dir)
    expected_state = [1, 5, 0.333333, 0.333333, 0.333333,
                      0.333333, 5, 0, 0, 0]
    assert test_lens_agent.get_state() == expected_state


expected_ex_file = '''name: sit1
I: 1 1 1 1 ;
'''


@nose.with_setup(reset_LensAgent)
def test_string_agent_state_to_ex():
    test_lens_agent = agent.LensAgent(4)
    test_lens_agent.seed_agent()
    assert test_lens_agent.get_state() == [1, 1, 1, 1]
    generated_file = test_lens_agent._string_agent_state_to_ex()
    assert generated_file == expected_ex_file

    # pdb.set_trace()
###############################################################################
# Unit Test notes
###############################################################################
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
