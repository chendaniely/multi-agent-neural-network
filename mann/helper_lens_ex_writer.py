#! /usr/bin/env/python
"""This module contains helper functions to write a LENS ex file
"""

import mann.helper

def create_ex_str_from_1d_list(list_1d, delim=' ', name=''):
	print(list_1d)
	ex_values = mann.helper.convert_list_to_delim_str(list_1d, delim=delim)
	string = "name: sit{}\nB: {};\n".format(name, ex_values)
	return(string)

def create_ex_str_from_2d_list(list_2d, returns='string'):
	d1_strings = []
	for idx, list_1d in enumerate(list_2d):
		d1_strings.append(create_ex_str_from_1d_list(list_1d, name=idx))
	if returns == 'string':
		string = "\n".join(d1_strings)
		print(string)
		return(string)
	elif returns == 'list':
		return(d1_strings)


def write_lens_ex_file(file_to_write,
                       string_to_write=None,
                       list_to_write_into_string=None):
        """Takes a string or list and writes an .ex file for lens
        """
        print("-"*80)
        print("string", string_to_write)
        print("list", list_to_write_into_string)
        with open(file_to_write, 'w') as f:
            if string_to_write is None and list_to_write_into_string is not None:
                # passed in a list of stings to write and not a full string
                ex_file_strings = '\n'.join(list_to_write_into_string)
                f.write(ex_file_strings)
            elif string_to_write is not None and list_to_write_into_string is None:
                # passed in just a string to directly write
                f.write(string_to_write)
            else:
                raise(ValueError,
                      "Unknown combination of strings or list passed")