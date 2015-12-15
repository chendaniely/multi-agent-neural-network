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


# @nose.with_setup(reset_LensAgentRecurrent)
# def test_calc_new_state_values_rps_1():
#     test_agent = agent_lens_recurrent.LensAgentRecurrent(10)

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

    random.seed(42)
    manual_predecessor_inputs = np.array([[9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
                                          [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
    expected_value = ['name: agent0-1\nI: 0 0 0 0 0 0 0 0 0 0;\n',
                      'name: agent0_manual\nI: 8 8 8 8 8 8 8 8 8 8;\n']
    lens_ex_file_strings = test_agent.sample_predecessor_values(
        1, manual_predecessor_inputs=manual_predecessor_inputs)
    assert expected_value == lens_ex_file_strings

# @nose.with_setup(reset_LensAgentRecurrent)
# def test_write_lens_ex_file():
#     test_agent = agent_lens_recurrent.LensAgentRecurrent(10)
#     file_to_write = os.path.join(HERE, 'lens', 'Infl.ex')
#     # string_to_write = helper.convert_list_to_delim_str(test_agent.state)
#     values_list = test_agent.state
#     test_agent.write_lens_ex_file(file_to_write,
#                                   list_to_write_into_string=None)

# @nose.with_setup(reset_LensAgentRecurrent)
# def test_create_weight_file_attitude_02_01_wgtmk():
#     test_agent = agent_lens_recurrent.LensAgentRecurrent(10)
#     weight_in_file_path = os.path.join(HERE, 'lens', 'lens_in_files',
#                                         'attitude_02_01_wgtmk.in')
#     # print(weight_in_file_path, file=sys.stderr)
#     weight_directory = os.path.join(HERE, 'lens', 'weights')
#     ex_file_path = os.path.join(HERE, 'lens', 'Infl.ex')
#     test_agent.create_weight_file(weight_in_file_path,
#                                   weight_directory,
#                                   ex_file_path)



# @nose.with_setup(reset_LensAgentRecurrent)
# def test_pick_random_predecessor():
#     test_agent = agent_lens_recurrent.LensAgentRecurrent(10)
#     test_agent_p1 = agent_lens_recurrent.LensAgentRecurrent(10)
#     test_agent_p2 = agent_lens_recurrent.LensAgentRecurrent(10)

#     test_agent.predecessors = [test_agent_p1, test_agent_p2]
#     print(test_agent.predecessors, file=sys.stderr)
#     picked_predecessor = test_agent.pick_random_predecessor(
#         test_agent.predecessors, 1)
#     print(picked_predecessor, file=sys.stderr)
