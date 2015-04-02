#! /usr/bin/env python
import random
# import sys

import numpy as np

from mann import helper

def test_convert_str_to_int_array():
    converted = helper.convert_str_to_int_array('1, 2, 3')
    expected = np.array([1, 2, 3])
    assert np.array_equal(converted, expected)

def test_convert_list_to_delim_str():
    converted = helper.convert_list_to_delim_str([1, 2, 3])
    expected = '1,2,3'
    assert converted == expected

def test_flip_1_0():
    calculated = helper.flip_1_0(1)
    expected = 0
    assert calculated == expected

    calculated = helper.flip_1_0(0)
    expected = 1
    assert calculated == expected

def test_mutate():
    calculated = helper.mutate([0, 0, 0, 0], 0)
    expected = [0, 0, 0, 0]
    assert np.array_equal(np.array(calculated), np.array(expected))

    calculated = helper.mutate([0, 0, 0, 0], 1)
    expected = [1, 1, 1, 1]
    assert np.array_equal(np.array(calculated), np.array(expected))

    random.seed(1)
    calculated = helper.mutate([0, 0, 0, 0], .5)
    # print(calculated, file=sys.stderr)
    expected = [1, 0, 0, 1]
    assert np.array_equal(np.array(calculated), np.array(expected))
