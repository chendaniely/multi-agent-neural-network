#! /usr/bin/env python

import nose
import sys
import io
from mann import agent


# def setup_lens_agent():
#     print('Setting up LENS agent')
#     test_lens_agent = agent.LensAgent(10)


# @with_setup(setup_lens_agent)
# def test_write_agent_state_to_ex():
#     test_file = 'write_agent_state_to_ex.test'
#     assert(1 == 3, 'you failed')
#     assert(3 == 3, 'you no fail')


# # @with_setup(setup_lens_agent)
# def test_pass():
#     assert(1 == 1, 'this should not fail')


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
