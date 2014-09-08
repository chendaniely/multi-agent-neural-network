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


#####################################
# Unit tests for the base Agent class
#####################################
def reset_agent_count():
    agent.Agent.agent_count = 0


def test_get_key():
    print("testing single agent creation", file=sys.stderr)
    test_agent = agent.Agent()
    assert test_agent.get_key() == 0, '1 agent fail'

    print("testing multiple agent creation", file=sys.stderr)
    list_of_test_agents = []
    agent.Agent.agent_count = 0
    for i in range(10):
        test_multiple_agent = agent.Agent()
        list_of_test_agents.append(test_multiple_agent)
    assert list_of_test_agents[0].get_key() == 0, 'first agent fail'
    assert list_of_test_agents[-1].get_key() == 9, 'last agent fail'
