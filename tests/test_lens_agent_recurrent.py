#! /usr/bin/env python
###############################################################################
import nose
import sys
import io
import random
import os
import glob
import subprocess
import numpy as np
import numpy.testing

from mann import agent_lens_recurrent
import helper

HERE = os.path.abspath(os.path.dirname(__file__))


###############################################################################
# Unit tests for the LensAgent class
###############################################################################
def reset_LensAgentRecurrent():
    agent_lens_recurrent.LensAgentRecurrent.agent_count = 0


def remove_lens_files():
    call_lens_files = os.path.join(HERE, 'lens', 'output', 'AgentState.out')
    infl_ex = os.path.join(HERE, 'lens', 'Infl.ex')
    weight_file = os.path.join(HERE, 'lens', 'weights', 'AgentWgt000000.wt')
    try:
        os.remove(call_lens_files)
    except:
        pass
    try:
        os.remove(infl_ex)
    except:
        pass
    try:
        os.remove(weight_file)
    except:
        pass


@nose.with_setup(reset_LensAgentRecurrent)
def test_sample_predecessor_values():
    test_agent = agent_lens_recurrent.LensAgentRecurrent(10)
    test_agent_1 = agent_lens_recurrent.LensAgentRecurrent(10)
    test_agent_2 = agent_lens_recurrent.LensAgentRecurrent(10)
    test_agent_3 = agent_lens_recurrent.LensAgentRecurrent(10)
    test_agent_1.state = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    test_agent_2.state = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    test_agent_3.state = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    test_agent.set_predecessors([test_agent_1, test_agent_2, test_agent_3])
    # print(test_agent.predecessors, file=sys.stderr)
    random.seed(42)
    expected_value = ['name: agent0-1\nI: 0 0 0 0 0 0 0 0 0 0;\n']
    lens_ex_file_strings = test_agent.sample_predecessor_values(0)
    assert expected_value == lens_ex_file_strings

    random.seed(42)
    expected_value = ['name: agent0-1\nI: 0 0 0 0 0 0 0 0 0 0;\n',
                      'name: agent3\nI: 3 3 3 3 3 3 3 3 3 3;\n',
                      'name: agent1\nI: 1 1 1 1 1 1 1 1 1 1;\n']
    lens_ex_file_strings = test_agent.sample_predecessor_values(2)
    assert expected_value == lens_ex_file_strings

    random.seed(42)
    expected_value = ['name: agent0-1\nI: 0 0 0 0 0 0 0 0 0 0;\n',
                      'name: agent3\nI: 3 3 3 3 3 3 3 3 3 3;\n',
                      'name: agent1\nI: 1 1 1 1 1 1 1 1 1 1;\n',
                      'name: agent2\nI: 2 2 2 2 2 2 2 2 2 2;\n']
    lens_ex_file_strings = test_agent.sample_predecessor_values(3)
    assert expected_value == lens_ex_file_strings

    # random.seed(42)
    np.random.seed(42)
    manual_predecessor_inputs = np.array([[9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
                                          [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
    expected_value = ['name: agent0-1\nI: 0 0 0 0 0 0 0 0 0 0;\n',
                      'name: agent0_manual\nI: 8 8 8 8 8 8 8 8 8 8;\n']
    lens_ex_file_strings = test_agent.sample_predecessor_values(
        1, manual_predecessor_inputs=manual_predecessor_inputs)
    assert expected_value == lens_ex_file_strings


@nose.with_setup(reset_LensAgentRecurrent, remove_lens_files)
def test_write_lens_ex_file():
    test_agent = agent_lens_recurrent.LensAgentRecurrent(10)
    test_agent_1 = agent_lens_recurrent.LensAgentRecurrent(10)
    test_agent_2 = agent_lens_recurrent.LensAgentRecurrent(10)
    test_agent_3 = agent_lens_recurrent.LensAgentRecurrent(10)
    test_agent_1.state = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    test_agent_2.state = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    test_agent_3.state = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    test_agent.set_predecessors([test_agent_1, test_agent_2, test_agent_3])

    file_to_write = os.path.join(HERE, 'lens', 'Infl.ex')

    if os.path.exists(file_to_write):
        print('file found:{}'.format(file_to_write), file=sys.stderr)
        os.remove(file_to_write)

    random.seed(42)
    test_agent.write_lens_ex_file(
        file_to_write,
        list_to_write_into_string=test_agent.sample_predecessor_values(3))
    expected_file_contents = """name: agent0-1
I: 0 0 0 0 0 0 0 0 0 0;

name: agent3
I: 3 3 3 3 3 3 3 3 3 3;

name: agent1
I: 1 1 1 1 1 1 1 1 1 1;

name: agent2
I: 2 2 2 2 2 2 2 2 2 2;
"""
    with open(file_to_write, 'r') as f:
        file_contents = f.read()
        assert file_contents == expected_file_contents


@nose.with_setup(reset_LensAgentRecurrent, remove_lens_files)
def test_call_lens_weight_file_attitude_02_01_wgtmk():
    agent_lens_recurrent.LensAgentRecurrent.agent_count = 0
    test_agent = agent_lens_recurrent.LensAgentRecurrent(10)
    test_agent_1 = agent_lens_recurrent.LensAgentRecurrent(10)
    test_agent_2 = agent_lens_recurrent.LensAgentRecurrent(10)
    test_agent_3 = agent_lens_recurrent.LensAgentRecurrent(10)
    test_agent_1.state = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    test_agent_2.state = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    test_agent_3.state = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    test_agent.set_predecessors([test_agent_1, test_agent_2, test_agent_3])
    file_to_write = os.path.join(HERE, 'lens', 'Infl.ex')
    test_agent.write_lens_ex_file(
        file_to_write,
        list_to_write_into_string=test_agent.sample_predecessor_values(3))
    in_file_path = os.path.join(
        HERE, 'lens', 'lens_in_files', 'attitude_02_01_wgtmk.in')
    test_agent.call_lens(lens_in_file_dir=in_file_path,
                         lens_env={'a': test_agent.get_padded_agent_id(),
                                   'bm': .10,
                                   'bs': .12,
                                   'wm': .30,
                                   'ws': .40,
                                   'cs': .50},
                         stdout_null=True)
    agent_state_out = os.path.join(HERE, 'lens', 'output', 'AgentState.out')
    weight_file = os.path.join(HERE, 'lens', 'weights', 'AgentWgt000000.wt')
    assert os.path.exists(weight_file)
    assert os.path.exists(agent_state_out)


@nose.with_setup(reset_LensAgentRecurrent)
def test_get_new_state_values_from_out_file():
    # call test_call_lens_weight_file_attitude_02_01_wgtmk()
    # to get an AgentState.out file
    test_agent = agent_lens_recurrent.LensAgentRecurrent(10)
    test_call_lens_weight_file_attitude_02_01_wgtmk()
    lens_output_dir = os.path.join(HERE, 'lens', 'output', 'AgentState.out')
    # print(test_agent.state, file=sys.stderr)
    new_state = test_agent.get_new_state_values_from_out_file(lens_output_dir)
    # print(new_state, file=sys.stderr)
    # print(test_agent.state, file=sys.stderr)
    test_agent.state = new_state
    # print(test_agent.state, file=sys.stderr)
    assert False, "can't test right now"
