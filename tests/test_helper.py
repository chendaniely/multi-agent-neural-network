#! /usr/bin/env python
import numpy as np

from mann import helper

def test_convert_str_to_int_list():
    converted = helper.convert_str_to_int_array('1, 2, 3')
    expected = np.array([1, 2, 3])
    assert np.array_equal(converted, expected)

def test_flip_1_0():
    calculated = helper.flip_1_0(1)
    expected = 0
    assert calculated == expected

    calculated = helper.flip_1_0(0)
    expected = 1
    assert calculated == expected
