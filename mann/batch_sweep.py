#! /usr/bin/env python

import multiprocessing as mp
import numpy as np
import os
import shutil
import configparser
import subprocess

"""Module that contains functions to help run batches and parameter sweeps
"""


def _parse_config_fr_to_by(config_string):
    """Returns the value for the fr, to, and by, range in the config file.

    Args:
        config_string (string): a string of fr, to, by values
                                separated by \n character

    Returns:
        tuple: float of number to the right of the fr, to, and by values in the
               config file

    Examples: # TODO test this
        >>> print(_parse_config_fr_to_by("fr = 0\nto = 1\nby = .2")
        (0.0, 1.0, 0.2)
    """
    config_string = config_string.strip()
    fr_to_by_list = config_string.split('\n')

    # for each fr, to, by value, take the value to the right of the equal sign
    fr_to_by_str = tuple(e.split("=")[1].strip() for e in fr_to_by_list)
    fr_to_by_float = map(float, fr_to_by_str)
    return fr_to_by_float


def parse_config_list(config_string, sep=','):
    """Returns a python tuple of a delimited string from the config file

    Args:
        config_string (string): a delimited string separated by the sep param
        sep (string): delimited for config_string, default is ','

    Returns:
        tuple: of string split by the sep
    """
    return tuple(config_string.split(','))


def _get_sweep_values_range(fr, to, by):
    """Returns an ndarray values that will be used for the simulation run.

    Will include the 'to' value if the 'by' step will does not exceed the
    'to' value

    Args:
        fr (float): value of where the sweep will start
        to (float): value of where the sweep will end
        by (float): values between fr and to by specified step

    Returns:
        values (ndarray): values for parameter sweep

    Examples:
        >>> print(get_sweep_values(0, 10, 2))
        array([0, 2, 4, 6, 8, 10])

        >>> print(get_sweep_values(1, 10, 2))
        array([1, 3, 5, 7, 9])
    """
    assert(isinstance(fr, float))
    assert(isinstance(to, float))
    assert(isinstance(by, float))

    values = np.arange(fr, to, by)
    # print('values in _get_sweep_values_range(): ', str(values))
    # make the range inclusive on the right, since this is what
    # the usuer will most likely mean in the parameter file
    end_value = values[-1] + by
    if end_value == to:
        values = np.append(values, values[-1] + by)

    # print('return values in _get_sweep_values_range(): ', str(values))
    return values


def _get_sweep_values_list(config_string):
    """Returns an ndarray values that will be used for the simulation run

    Args:
        config_string (string): config string read form config file

    Returns:
        ndarray of values
    """
    return np.asarray(
        list(float(x.strip()) for x in (config_string.split(','))))


def get_sweep_values(config_string, sweep_type):
    """Returns an ndarray of values that will be used for the simulation run

    Takes a config string form the config file, and the sweep type.  The sweep
    type can be a range (the fr, to, by syntax) or a list of values.  This
    function will either call the
    _get_sweep_values_ftb or
    _get_sweep_values_list
    depending on the sweep_type

    Args:
        config_string (string): string from the config file
        sweep_type (string): type of config string, either range or list

    Returns:
        values (ndarray): values for parameter sweep
    """
    if (sweep_type == "range"):
        values_range = _ftb_string_to_values(config_string)
        return(values_range)
    elif (sweep_type == "list"):
        values_list = _get_sweep_values_list(config_string)
        return(values_list)
    else:
        raise ValueError(str("Unknown sweep type, can be range or list " +
                             str(sweep_type) + " passed"))


def copy_directory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)


def _ftb_string_to_values(ftb_string):
    """
    """
    f, t, b = _parse_config_fr_to_by(ftb_string)
    # print(f, t, b)

    # sweep_values = np.arange(f, t, b)
    # print(str(sweep_values))

    # print(get_sweep_values(f, t, b))
    sweep_values = _get_sweep_values_range(f, t, b)
    # print("return sweep_values in _ftb_string_to_values(): ", sweep_values)
    return sweep_values


def _format_values_lens(tuple_of_values):
    # assert(len(tuple_of_values) == 5)
    assert(len(tuple_of_values) == 2)
    # agents, delta, epsilon, criterion, run = tuple_of_values
    agents, run = tuple_of_values

    agents = int(agents)
    # delta = float("{0:.2f}".format(delta))
    # epsilon = float("{0:.2f}".format(epsilon))
    # criterion = int(criterion)
    run = int(run)

    assert isinstance(agents, int)
    # assert isinstance(delta, float)
    # assert isinstance(epsilon, float)
    # assert isinstance(criterion, int)
    assert isinstance(run, int)

    # return tuple((agents, delta, epsilon, criterion, run))
    return tuple((agents, run))


def _format_values_watts(tuple_of_values):
    assert(len(tuple_of_values) == 2)
    agents, run = tuple_of_values

    agents = int(agents)
    run = int(run)

    assert isinstance(agents, int)
    assert isinstance(run, int)

    return tuple((agents, run))


def format_values(base_directory, tuple_of_values):
    if base_directory in ["02-lens"]:
        return(_format_values_lens(tuple_of_values))
    elif base_directory in ["01-watts"]:
        return(_format_values_watts(tuple_of_values))


# def _create_folder_lens(base_directory,
#                         current_time,
#                         agents_str,
#                         delta_str,
#                         epsilon_str,
#                         criterion_str,
#                         run_str):

#     new_sim_folder_name = '_'.join(['a'+agents_str,
#                                     'd'+delta_str,
#                                     'e'+epsilon_str,
#                                     'c'+criterion_str,
#                                     'r'+run_str])
#     print(new_sim_folder_name, " created")

#     batch_folder_name = '_'.join([base_directory, 'batch', current_time])
#     # print('batch folder name: ', batch_folder_name)

#     dir_to_copy_from = os.path.join(here, base_directory)
#     # print('from: ', dir_to_copy_from)

#     batch_folder_full_path = os.path.join(here, '..', 'results', 'simulations',
#                                           batch_folder_name)

#     if not os.path.exists(batch_folder_full_path):
#         # print('created: ', batch_folder_full_path)
#         os.makedirs(batch_folder_full_path)

#     dir_to_copy_to = os.path.join(batch_folder_full_path,
#                                   new_sim_folder_name)
#     # print('to : ', dir_to_copy_to)

#     copy_directory(dir_to_copy_from, dir_to_copy_to)
#     return dir_to_copy_to


def _create_folder_lens(base_directory,
                        here,
                        current_time,
                        agents_str,
                        run_str):

    new_sim_folder_name = '_'.join(['a'+agents_str,
                                    'r'+run_str])
    print(new_sim_folder_name, " created")

    batch_folder_name = '_'.join([base_directory, 'batch', current_time])
    print('batch folder name: ', batch_folder_name)

    dir_to_copy_from = os.path.join(here, '..', base_directory)
    print('from: ', dir_to_copy_from)

    batch_folder_path = os.path.join(here, '..', '..',
                                     'results', 'simulations',
                                     batch_folder_name)

    if not os.path.exists(batch_folder_path):
        print('created: ', batch_folder_path)
        os.makedirs(batch_folder_path)

    dir_to_copy_to = os.path.join(batch_folder_path,
                                  new_sim_folder_name)
    print('to : ', dir_to_copy_to)

    copy_directory(dir_to_copy_from, dir_to_copy_to)
    return dir_to_copy_to


def _create_folder_watts(base_directory,
                         here,
                         current_time,
                         agents_str,
                         run_str):

    new_sim_folder_name = '_'.join(['a'+agents_str,
                                    'r'+run_str])
    print(new_sim_folder_name, " created")

    batch_folder_name = '_'.join([base_directory, 'batch', current_time])
    print('batch folder name: ', batch_folder_name)

    dir_to_copy_from = os.path.join(here, '..', base_directory)
    print('from: ', dir_to_copy_from)

    batch_folder_path = os.path.join(here, '..', '..',
                                     'results', 'simulations',
                                     batch_folder_name)

    if not os.path.exists(batch_folder_path):
        print('created: ', batch_folder_path)
        os.makedirs(batch_folder_path)

    dir_to_copy_to = os.path.join(batch_folder_path,
                                  new_sim_folder_name)
    print('to : ', dir_to_copy_to)

    copy_directory(dir_to_copy_from, dir_to_copy_to)
    return dir_to_copy_to


def create_folder(base_directory, here, **kwargs):
    if base_directory in ["02-lens"]:
        # dir_to_copy_to = _create_folder_lens(**kwargs)
        dir_to_copy_to = _create_folder_lens(base_directory, here, **kwargs)
    elif base_directory in ["01-watts"]:
        dir_to_copy_to = _create_folder_watts(base_directory, here, **kwargs)
    return dir_to_copy_to


def _update_init_file_lens(folder_name,
                           agents,
                           delta,
                           epsilon,
                           criterion,
                           run):
    """Updates the config file for a particular set of parameters for sweep

    Args:
        mutation (float): mutation value parameter for sweep
        ci (int): criterion value parameter for sweep
        run_number (int): run number for a set of value parameters for sweep
    """
    assert isinstance(agents, int)
    assert isinstance(delta, float)
    assert isinstance(epsilon, float)
    assert isinstance(criterion, int)
    assert isinstance(run, int)

    #
    # Read in config file
    #
    sim_config = configparser.SafeConfigParser()
    sim_config_file_dir = os.path.join(folder_name, 'config.ini')
    sim_config.read(sim_config_file_dir)

    #
    # Get new config file values
    #

    # set agents
    sim_config.set('LENSParameters', 'NumberOfAgents',
                   str(agents))

    # set delta
    sim_config.set('LENSParameters', 'WeightTrainExampleMutationsProb',
                   str(delta))
    # set epsilon
    sim_config.set('LENSParameters', 'Epsilon', str(epsilon))

    # set criterion
    sim_config.set('LENSParameters', 'Criterion', str(criterion))

    # set run
    sim_config.set('General', 'RunNumber', str(run))

    #
    # Write new config file
    #
    with open(sim_config_file_dir, 'w') as update_config:
        sim_config.write(update_config)
        # print('config file updated: ', sim_config_file_dir)


def _update_init_file_watts(config,
                            agents,
                            run):
    """Updates the config file for a particular set of parameters for sweep

    Args:
        run_number (int): run number for a set of value parameters for sweep
    """
    assert isinstance(agents, int)
    assert isinstance(run, int)

    # set agents
    sim_config.set('General', 'NumberOfAgents',
                   str(agents))
    # set run
    sim_config.set('General', 'RunNumber', str(run))

    return sim_config


def update_init_file(folder_name, **kwargs):
    """Updates the config file for a particular set of parameters for sweep
    """
    #
    # Read in config file
    #
    sim_config = configparser.SafeConfigParser()
    sim_config_file_dir = os.path.join(folder_name, 'config.ini')
    sim_config.read(sim_config_file_dir)

    if sim_config.get("General", "BaseDirectory") == "01-watts":
        sim_config = _update_init_file_watts(sim_config,
                                             agents=kwargs.get('agents'),
                                             run=kwargs.get('run'))
    else:
        print('pass')
        pass

    #
    # Write new config file
    #
    with open(sim_config_file_dir, 'w') as update_config:
        sim_config.write(update_config)
        # print('config file updated: ', sim_config_file_dir)


def num_cores(num_cores=None):
    if num_cores is not None:
        return int(num_cores)
    else:
        cores = mp.cpu_count()
        print("Number of cores on this computer: ", cores)
        if cores <= 12:
            return cores
        else:
            return int(cores * (2/3.0))


def chmod_recursive(directory, dir_chmod=0o555, file_chmod=0o444):
    os.chmod(directory, dir_chmod)
    for root, dirs, files in os.walk(directory):
        for sim_dir in dirs:
            os.chmod(os.path.join(root, sim_dir), dir_chmod)
        for sim_file in files:
            os.chmod(os.path.join(root, sim_file), file_chmod)


def run_simulation(folder_name):
        ex_file = os.path.join(folder_name, 'main.py')
        subprocess.call(['python', ex_file])
        chmod_recursive(folder_name)
