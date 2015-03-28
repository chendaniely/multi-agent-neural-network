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
