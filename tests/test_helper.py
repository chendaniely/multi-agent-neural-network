#! /usr/bin/env python
import random
# import sys

import nose
import numpy as np

from mann import helper


def test_convert_str_to_int_array():
    converted = helper.convert_str_to_int_array('1, 2, 3')
    expected = np.array([1, 2, 3])
    assert np.array_equal(converted, expected)

    converted = helper.convert_str_to_int_array('1 2 3', delims=[' '])
    assert np.array_equal(converted, expected)

    converted = helper.convert_str_to_int_array('1 2 3 4, 5, 6',
                                                delims=[', ', ' '])
    expected = np.array([1, 2, 3, 4, 5, 6])
    assert np.array_equal(converted, expected)


def test_convert_str_to_2d_int_array():
    calculated = helper.convert_str_to_2d_int_array('1, 2, 3; 4, 5, 6; 7 8 9')
    expected = [np.array([1, 2, 3]), np.array([4, 5, 6]), np.array([7, 8, 9])]
    # assert False
    assert np.array_equal(calculated, expected)

    calculated = helper.convert_str_to_2d_int_array('1, 2, 3\n4, 5, 6;7 8 9')
    assert np.array_equal(calculated, expected)

    calculated = helper.convert_str_to_2d_int_array(
        '\n\n1, 2, 3\n4, 5, 6;7 8 9\n\n')
    assert np.array_equal(calculated, expected)

    calculated = helper.convert_str_to_2d_int_array('None')
    expected = None
    assert calculated is expected
    assert calculated == expected


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


@nose.tools.raises(ValueError)
def test_flip_1_0_expection():
    helper.flip_1_0(3)


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


@nose.tools.raises(ValueError)
def test_mutate_ValueError_neg():
    helper.mutate([0, 0, 0, 0], -1)


@nose.tools.raises(ValueError)
def test_mutate_ValueError_pos():
    helper.mutate([0, 0, 0, 0], 1.1)
