#!/usr/bin/env python

def convert_str_to_int_list(self, string, delim=','):
    """Returns a list of ints from a delimited separated string of ints
    :parm string: delimited string of ints
    :type string: str

    :parm delim: string delimited, default is ',' (a comma)
    :type delim: str
    """
    assert isinstance(string, str), "string parameter passed is not type str"
    assert isinstance(delim, str), "delim parameter passed is not type str"
    return list(int(s) for s in string.strip().split(delim))
