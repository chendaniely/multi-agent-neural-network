#! /usr/bin/env python

import nose
import sys
import io
from mann import agent




def setup_lens_agent():
    print('Setting up LENS agent')
    test_lens_agent = agent.LensAgent(10)


@with_setup(setup_lens_agent)
def test_write_agent_state_to_ex():
    test_file = 'write_agent_state_to_ex.test'
    assert(1 == 3, 'you failed')
    assert(3 == 3, 'you no fail')


# @with_setup(setup_lens_agent)
def test_pass():
    assert(1 == 1, 'this should not fail')
