#! /usr/bin/env python

import sys

from mann import helper
from mann import lens_in_writer

test_small_recurrent_attitude_in_string = """name: agent_state
I: 1 2 3;
name: infl1
I: 4 5 6;
"""


def test_generate_lens_recurrent_attitude():
    test_writer = lens_in_writer.LensInWriterHelper()
    calculated = test_writer.generate_lens_recurrent_attitude(
        '1, 2, 3', '4, 5, 6')
    expected = test_small_recurrent_attitude_in_string
    # print(calculated, file=sys.stderr)
    # print(expected, file=sys.stderr)
    assert calculated == expected


def test_generate_lens_recurrent_attitude_list():
    test_writer = lens_in_writer.LensInWriterHelper()
    array_to_string_agent = helper.convert_list_to_delim_str([1, 2, 3], ' ')
    array_to_string_infl = helper.convert_list_to_delim_str([4, 5, 6], ' ')
    calculated = test_writer.generate_lens_recurrent_attitude(
        array_to_string_agent, array_to_string_infl)
    expected = test_small_recurrent_attitude_in_string
    # print(calculated, file=sys.stderr)
    # print(expected, file=sys.stderr)
    assert calculated == expected
