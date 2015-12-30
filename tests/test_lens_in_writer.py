#! /usr/bin/env python
import os
import sys

from mann import helper
from mann import lens_in_writer

HERE = os.path.abspath(os.path.dirname(__file__))

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


def test_write_in_file():
    test_writer = lens_in_writer.LensInWriterHelper()
    s = test_writer.generate_lens_recurrent_attitude(
        '1, 2, 3', '4, 5, 6')
    in_file_path = os.path.join(HERE, 'lens', 'output',
                                'test_in_file.in')
    test_writer.write_in_file(in_file_path, s)
    with open(in_file_path, 'r') as f:
        file_contents = f.read()
        assert file_contents == test_small_recurrent_attitude_in_string
