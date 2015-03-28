#! /usr/bin/env python
import numpy as np

from mann import helper

def test_convert_str_to_int_list():
    converted = helper.convert_str_to_int_array('1, 2, 3')
    expected = np.array([1, 2, 3])
    assert np.array_equal(converted, expected)
