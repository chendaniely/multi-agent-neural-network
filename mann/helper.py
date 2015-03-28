#!/usr/bin/env python
import numpy as np

def convert_str_to_int_array(string, delim=','):
    """Returns a list of ints from a delimited separated string of ints
    :parm string: delimited string of ints
    :type string: str

    .. note::
    The string parameter cannot be empty

    :parm delim: string delimited, default is ',' (a comma)
    :type delim: numpy.ndarray
    """
    assert isinstance(string, str), "string parameter passed is not type str"
    assert isinstance(delim, str), "delim parameter passed is not type str"
    assert string != '', 'string parameter is empty'
    return np.array([int(s) for s in string.strip().split(delim)])

def flip_1_0(number):
    """Flip 1 to 0, and vice versa
    :parm number: 1 or 0 to flip
    :type number: int

    :returns flipped value
    :rtype: int
    """
    assert number in [0, 1], 'number to flip is not a 0 or 1'
    assert isinstance(number, int), 'number to flip is not int'
    if number == 0:
        return 1
    elif number == 1:
        return 0
    else:
        raise ValueError('Number to flip not 0 or 1')
