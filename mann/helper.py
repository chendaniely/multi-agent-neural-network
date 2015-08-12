#!/usr/bin/env python
import random
import warnings

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
    return np.array([float(s) for s in string.strip().split(delim)])


def convert_str_to_2d_int_array(string,
                                delim_array=[', ', ' ', '', ','],
                                delim_array_values=['\n', ';']):
    string = string.strip()
    if string == "None":
        return None
    else:
        arrays = re.split('|'.join(delim_array_values), string)
        arrays = [x.strip()  for x in arrays if x.strip() != '']
        arrays = np.array(
            [convert_str_to_int_array(x, delims=delim_array) for x in arrays])
        print(arrays)
        return(arrays)


def convert_list_to_delim_str(list_to_convert, delim=','):
    """Return a string delimited by delim from a list

    :parm list_to_convert: list of values to convert
    :type list_to_convert: list

    :parm delim: delimeter used in returned string
    :type delim: str

    :returns: string delimited with the delim
    :rtype: str

    Example: self._list_to_str_delim([1, 2, 3, ' '])
    > 1 2 3

    Example self._list_to_str_delim([1, 2, 3], ',')
    > 1,2,3
    """
    return delim.join(map(str, list_to_convert))


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


def mutate(list_to_mutate, mutation_prob):
    """Mutates each element of a list by the mutation_prob
    Mutating means flipping the 1 to a 0 or vice versa

    :param list_to_mutate: list of values to mutate
    :type list_to_mutate: list

    :param mutation_prob: probability of flipping each element in list
    :type mutation_prob: float

    if the mutation_prob == 0, then the original list is returned
    else, there is a probabliy that prototype is still returned
    """
    if mutation_prob > 0.0 and mutation_prob <= 1.0:
        post_mutation_list = list_to_mutate[:]
        for idx, value in enumerate(list_to_mutate):
            prob = random.random()
            if prob <= mutation_prob:
                post_mutation_list[idx] = flip_1_0(value)
        if ((post_mutation_list is list_to_mutate) or
                (post_mutation_list == list_to_mutate)):
            warnings.warn('Mutated example is equal to prototype',
                          UserWarning)
        return post_mutation_list
    elif mutation_prob == 0.0:
        return list_to_mutate
    else:
        raise ValueError('Incorrect value for mutation probability ' +
                         'probability needs to be between ' +
                         '0 and 1 inclusive')
