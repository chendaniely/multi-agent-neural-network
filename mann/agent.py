#!/usr/bin/env python

import random
import subprocess
import io
import os
# import sys  # used to print to stderr for unit testing
import warnings


class Error(Exception):
    '''Base class for other exceptions'''
    def __init__(self, message):
        print(message)


class BaseAgentStateError(Error):
    '''Raised when the get_state method is called from the Agent class'''


class BaseAgentSeedError(Error):
    '''Raised when the seed_agent method is called from the Agent class'''


class BaseAgentUpdateStateError(Error):
    '''Raised when the update_agent_state method
    is called from the Agent class'''

class AssignAgentIdError(Error):
    """Raised when trying to assign an agent id to an agent that
    already has an ID
    """

###############################################################################
#
# Agent Class
#
###############################################################################
class Agent(object):
    '''
    This is the agent class.
    Agents are hashable so they can be used as nodes in a network
    from the networkx package
    '''

    # variable that tracks how many instances the Agent object is created
    agent_count = 0

    def __init__(self):
        # first agent created is agent 0
        self.agent_id = Agent.agent_count
        Agent.agent_count += 1
        self.predecessors = []
        self.num_update = 0

    def __hash__(self):
        '''
        defines the hash function.
        the hash function hashes the _key()
        '''
        return hash(self._key())

    def __eq__(x, y):
        '''
        equality method
        used to implement whether 2 agents are the same
        where equality is defined by the get_key() values
        '''
        return x.get_key() == y.get_key()

    def __repr__(self):
        return str(self.__class__.__name__) + ", key: " + str(self.get_key())

    def __str__(self):
        return "A" + str(self.get_key())

    def _key(self):
        '''
        method that returns a tuple of the unique vales of the agent.
        this tuple is then used to hash and do comparisons.

        Args:
            none

        Returns:
            int: unique keys of the agent
        '''
        return self.agent_id

    def get_key(self, **kwargs):
        if kwargs.get('pad_0_left') is not None:
            padded_agent_number = "{0:06d}".format(self.get_key())
            return padded_agent_number
        else:
            return self._key()

    def set_state(self, new_state):
        raise BaseAgentStateError('Base agent class has no state')

    def get_state(self):
        raise BaseAgentStateError('Base agent class has no state')

    def set_predecessors(self, list_of_predecessors):
        '''
        Takes a list of predecessors and assigns the list to self.predecessors

        Args:
            list_of_predecessors (list): a list of predecessors

        Returns
            None
        '''
        self.predecessors = list_of_predecessors

    def has_predessor(self):
        if len(self.predecessors) == 0:
            return False
        else:
            return True

    def seed_agent(self):
        raise BaseAgentSeedError('Base agent class cannot be seeded')

    def update_agent_state(self):
        raise BaseAgentUpdateStateError(
            'Base agent class has no state to update')

###############################################################################
#
# Binary Agent Class
#
###############################################################################


class BinaryAgent(Agent):
    binary_agent_count = 0

    def __init__(self):
        self.agent_id = BinaryAgent.binary_agent_count
        BinaryAgent.binary_agent_count += 1
        self.binary_state = 0
        self.predecessors = []

    def set_binary_state(self, value):
        # binary state means 0 or 1
        assert value in [0, 1],\
            "binary state can only be 0 or 1, got %r" % value

        # make sure we are only changing the state when the value is different
        assert value != self.binary_state, "changing state to same value"

        self.binary_state = value

    def get_state(self):
        return self.binary_state

    def seed_agent(self):
        self.set_binary_state(1)

    def random_binary_state(self):
        '''
        generates a random state for the agent as it is created
        raises exception if state cannot be assign

        Returns:
            int: value of 0 or 1 for a :py:data::self.state
        '''
        random_float = random.random()
        if random_float < .5:
            return 0
        elif random_float >= .5:
            return 1
        # else:
        #     return -1
        #     raise Exception("Error in _random_state")

    def _update_agent_state_default(self):
        '''
        Looks at the list of predessors for the selected agent
        randomly picks one of them
        if the selected predessor is has a different state
        there will be a 70% chance that the selected agent will change states
        to match the predessor's state
        otherwise no state is changed
        '''
        # print('in _update_agent_state_default')
        # print("type of predecssors: ",  type(self.predecessors))  # list
        # print("container of predessors: ", self.predecessors)
        predecessor_picked = random.sample(list(self.predecessors), 1)[0]
        # print("predecessor picked: ", predecessor_picked)
        # print("predecessor picked key: ", predecessor_picked.get_key())
        if self.binary_state == predecessor_picked.binary_state:
            # print("no update required, binary states are the same")
            # print("self.binary_state = ", self.binary_state)
            # print("predecessor_picked.binary_state = ",
            #       predecessor_picked.binary_state)
            pass
        else:
            # print('updateing agent state')
            random_number = random.random()
            if random_number < 0.7:
                self.set_binary_state(predecessor_picked.binary_state)
            else:
                pass

    def update_agent_state(self, pick='default'):
        '''
        pick = 'default': uses the update_agent__state_default algorithm
        '''
        # print('in update_agent_state')
        # print('has predecessors', self.has_predessor())
        if self.has_predessor():
            if pick == 'default':
                self._update_agent_state_default()
            else:
                raise ValueError("Algorithm used for pick unknown")
        else:
            pass

###############################################################################
#
# Lens Agent Class
#
###############################################################################
class LensAgent(Agent):
    agent_count = 0
    prototypes = []

    def __init__(self, num_state_vars):
        """Creates a LensAgent instance

        :param num_state_vars: Total number of processing units in the LensAgent.
        """
        print('class prototypes: ', LensAgent.prototypes)
        print(len(LensAgent.prototypes))
        assert len(LensAgent.prototypes) >= 1,\
               "LensAgent prototypes need to be set before creating "

        self.agent_id = LensAgent.agent_count
        LensAgent.agent_count += 1

        self.state = [0] * num_state_vars
        self.predecessors = []
        self.num_update = 0

        print("All prototypes: ", str(LensAgent.prototypes))

        self.prototype = random.sample(LensAgent.prototypes, 1)[0]
        print('Agent PROTOTYPE: ', str(self.prototype))
        assert isinstance(self.prototype, list)

        self.reset_step_variables()

    def _create_prototype(num_state_vars, list_of_elements, prob_each_element):
        '''returns a prototype for the LensAgent class
        current implementation assumes only 2 elements in both the
        list_of_elements, and prob_each_element
        current implementation also does not use the second prob_each_element
        only to test that the sum is equal to 1
        '''

        assert sum(prob_each_element) == 1

        prototype = []
        for i in range(num_state_vars):
            random_number = random.random()
            if random_number < prob_each_element[0]:
                prototype.append(list_of_elements[0])
            elif random_number >= prob_each_element[0]:
                prototype.append(list_of_elements[1])
        assert isinstance(prototype, list)
        assert len(prototype) == num_state_vars
        return prototype

    def set_lens_agent_prototypes(number_of_prototypes, num_units):
        """Create prototypes for the :class:`LensAgent` class

        Args:
            number_of_prototypes (int): Number of prototypes to create

        Kwargs:
            None

        Returns:
            None

        Function does not return any value, rather, it creates prototypes and
        assigns the prototypes to :py:data:`LensAgent.prototypes`

        """
        assert isinstance(number_of_prototypes, int),\
            "number_of_prototypes is not int"
        list_of_prototypes = list(LensAgent._create_prototype(num_units,
                                                              [0, 1], [.5, .5])
                                  for x in range(number_of_prototypes))
        assert isinstance(list_of_prototypes[0], list)
        LensAgent.prototypes = list_of_prototypes[:]
        print('list of prototypes created: ', str(list_of_prototypes))

    def call_lens(self, lens_in_file_dir, **kwargs):
        """Calls LENS

        :param lens_in_file_dir: file dir of .in file to use for LENS
        :type lens_in_file_dir: str

        Typically the 'env' key is passed in the kwargs, where 'env' will
        be a variable that contains all the enviornment variables needed
        for lens to run the .in file properly
        """
        subprocess.call(['lens', '-batch', lens_in_file_dir], **kwargs)

        # subprocess.call(['lens', '-batch', lens_in_file],
        #                env=kwargs.get('env'))

    def _create_weight_training_examples(self, filename,
                                         base_example,
                                         num_train_examples,
                                         mutation_prob):
        '''return a 2d list
        where d1 is a list that represents the training example
        d2 is the individual value of the training example
        the 2d list can be used to write weight training examples
        '''
        open(filename, 'w').close()
        if mutation_prob == 0:
            return [base_example] * num_train_examples
        else:
            list_of_example_values = []
            for train_example in range(num_train_examples):
                train_list = base_example[:]
                assert isinstance(train_list[0], int)

                for idx, training_value in enumerate(train_list):
                    prob = random.random()

                    if prob < mutation_prob:
                        train_list[idx] = self._flip_1_0_value(training_value)

                    if (train_list is base_example) or\
                       (train_list == base_example):
                        warnings.warn('Mutated example is equal to prototype',
                                      UserWarning)
                list_of_example_values.append(train_list)
            return list_of_example_values

    def _get_new_state_values_from_out_file(self, file_dir, type, column=0):
        """Get new state values from .out file_d

        :returns: new state values
        :rtype: tuple
        """
        # creates a list and returns a tuple
        list_of_new_state = []

        # here = os.path.abspath(os.path.dirname(__file__))
        # read_file_path = here + '/' + file_dir
        read_file_path = file_dir
        # print('read_file_path: ', read_file_path)
        # print('files here', os.listdir("./"))

        with open(read_file_path, 'r') as f:
            start_bank1, end_bank1, start_bank2, end_bank2 = \
                self._start_end_update_out(f)
            for line_idx, line in enumerate(f):
                # print(line)
                line_num = line_idx + 1  # python starts from line 0
                if start_bank1 <= line_num <= end_bank1 or \
                   start_bank2 <= line_num <= end_bank2:
                    # in a line that I want to save information for
                    col = line.strip().split(' ')[column]
                    list_of_new_state.append(float(col))
                    # print('list of new state', list_of_new_state)
        return tuple(list_of_new_state)

    def _length_per_bank(self):
        num_elements_per_bank = len(self.get_state())/2
        assert str(num_elements_per_bank).split('.')[1] == '0'
        return int(num_elements_per_bank)

    def _start_end_update_out(self, f, sim_type='LensAgentRecurrent_attitude'):
        # enter the actual file line numbers
        # the 1 offset is used in the actual fxn call
        # f is the .out file to be read
        # TODO pass these values in from config file
        if(sim_type == 'global_cascade'):
           return tuple([5, 14, 15, 24])
        elif(sim_type == 'LensAgentRecurrent_attitude'):
           return tuple([254, 258, 260, 264])

    def _string_agent_state_to_ex(self):
        output = io.StringIO()
        output.write('name: sit1\n')
        lens_agent_state_str = self._list_to_str_delim(self.state, " ")
        input_line = 'B: ' + lens_agent_state_str + ' ;\n'
        output.write(input_line)
        contents = output.getvalue()
        output.close()
        # print(contents)
        return contents

    def _update_agent_state_default(self, lens_in_file, agent_ex_file,
                                    infl_ex_file, agent_state_out_file,
                                    criterion):
        if len(self.predecessors) > 0:
            predecessor_picked = random.sample(list(self.predecessors), 1)[0]
            predecessor_picked.write_to_ex(infl_ex_file)
            state_env = self.get_env_for_pos_neg_bank_values()
            state_env['c'] = str(criterion)
            self._call_lens(lens_in_file, env=state_env)
            self.new_state_values = self._get_new_state_values_from_out_file(
                agent_state_out_file)
            self.set_state(self.new_state_values)

            self.step_input_agent_id = predecessor_picked.get_key()
            self.step_input_state_values = predecessor_picked.get_state()
            self.step_lens_target = predecessor_picked\
                ._get_new_state_values_from_out_file(agent_state_out_file, 1)
            self.step_update_status = 1
        else:
            warnings.warn('No predecessors for LensAgent ' + str(self.get_key),
                          UserWarning)

    def _write_sit_to_ex(self, list_to_write, sit_num, f):
        '''
        parameters
        ----------
        list_to_write: list, 1d list
        '''
        f.write('name: sit' + str(sit_num) + '\n')
        lens_agent_state_str = self._list_to_str_delim(list_to_write, " ")
        # print('weight EX to write: ', lens_agent_state_str)
        input_line = 'B: ' + lens_agent_state_str + ' ;\n'
        f.write(input_line)

    def calculate_new_state_default_i(self, lens_in_file, agent_ex_file,
                                      infl_ex_file, agent_state_out_file,
                                      criterion):
        """Calculates a new state using the default influencing agent algorithm.

        The default influencing agent algorithm picks an influencing agent
        by picking a random agent in the current agent's local network.

        :returns: New state values
        :rtype: tuple
        """
        if len(self.predecessors) > 0:
            predecessor_picked = random.sample(list(self.predecessors), 1)[0]
            predecessor_picked.write_to_ex(infl_ex_file)
            state_env = self.get_env_for_pos_neg_bank_values()
            state_env['a'] = self.get_padded_agent_id()
            state_env['c'] = str(criterion)
            self._call_lens(lens_in_file, env=state_env)
            # self.new_state_values = self._get_new_state_values_from_out_file(
            #     agent_state_out_file)
            # self.set_state(self.new_state_values)

            self.step_input_agent_id = predecessor_picked.get_key()
            self.step_input_state_values = predecessor_picked.get_state()
            self.step_lens_target = predecessor_picked\
                ._get_new_state_values_from_out_file(agent_state_out_file, 1)
            self.step_update_status = 1
            return self._get_new_state_values_from_out_file(
                agent_state_out_file)

        else:
            warnings.warn('No predecessors for LensAgent ' + str(self.get_key),
                          UserWarning)


    def calculate_new_state(self, influencing_algorithm='default', **kwargs):
        """Calculates new state values

        TODO: This function is a copy/paste of update_agent_state, and needs
        to be refactored accordinly

        :returns: New state
        :rtype: tuple
        """
        # if there is an agent_state_out_file, clear it
        # this makes sure there will be nothing appended
        if kwargs.get('agent_state_out_file') is not None:
            open(kwargs.get('agent_state_out_file'), 'w').close()
            assert os.stat(kwargs.get('agent_state_out_file')).st_size == 0
        if influencing_algorithm == 'default':
            #self.num_update += 1
            new_state = self.calculate_new_state_default_i(
                kwargs.get('lens_in_file'),
                kwargs.get('agent_ex_file'),
                kwargs.get('infl_ex_file'),
                kwargs.get('agent_state_out_file'),
                kwargs.get('criterion'))
            return new_state

        else:
            raise ValueError('Algorithm used for pick unknown')


    def create_weight_file(self, weight_in_file, weight_output_dir,
                           base_example, num_train_examples,
                           prototype_mutation_prob, criterion):
        """Creates the weight file for the :py:class:`LensAgent`

        The weights are needed for LENS, as it defines the weights between each
        processing unit and the units in the hidden latery of the nerual
        network.  The weight file created is a binary file.

        :param weight_in_file: full path to the LENS .in file to generate
            weights
        :type weight_in_file: string

        :param weight_output_dir:full path where to save the binary
            weight files
        :type weight_output_dir: string

        :param base_example: comma separated string of prototype (see
            #81 in MANN issues)
        :type base_example: string

        :param num_train_examples: number of examples used to train weights
        :type num_train_examples: int

        :param prototype_mutation_prob: a.k.a delta, prob training
            example mutation from prototype
        :type prototype_mutation_prob: float

        :param criterion:criterion to stop weight training
        :type criterion: int

        :returns: None
        :rtype: None


        calls ._create_weight_training_examples to create list of training ex

        calls ._write_to_ex to write list of train ex to create the .ex files

        subprocess call to lens to create .wt weight files
        """
        # print('weight in file read: ', weight_in_file)
        # print('weight output read: ', weight_output_dir)

        # TODO make this lins a function
        padded_agent_number = "{0:06d}".format(self.get_key())
        assert len(padded_agent_number) == 6, 'padded key len in wgt file err'

        weight_ex_name = 'AgentWgt' + padded_agent_number + '.ex'
        weight_ex_dir = weight_output_dir + '/' + weight_ex_name

        # if the path does not exist, create it
        if not os.path.exists(weight_output_dir):
            os.makedirs(weight_output_dir)

        # copy current envvironment
        lens_env = os.environ

        lens_env["a"] = padded_agent_number
        lens_env["c"] = str(criterion)
        # print('a environment: ', lens_env.get('a'))
        # print('a environment: ', lens_env.get('a'), file=sys.stderr)

        # prototype = self._str_to_int_list(self.prototype)

        list_ex = self._create_weight_training_examples(
            weight_ex_dir,
            self.prototype,
            num_train_examples,
            prototype_mutation_prob)

        assert isinstance(list_ex, list), 'list_ex is not a list'
        self.write_to_ex(weight_ex_dir,
                         write_type='sit',
                         weight_ex_list=list_ex)

        # list of 'words' passed into the subprocess call
        lens_weight_command = ['lens', '-batch',  weight_in_file]
        subprocess.call(lens_weight_command, env=lens_env)

    def get_state(self):
        """Return the state of the agent

        Args:
            None

        Returns:
            :py:data:self.state
        """
        return self.state

    def reset_step_variables(self):
        """Resets variables and states that will be written to output file
        This is called after Agent Initialization to set all values to None

        Args:
            None

        Returns:
            None

        variables reset are:

        self.step_input_agent_id

        self.step_input_state_values

        self.step_lens_target

        self.step_update_status
        """
        self.step_input_state_values = [None] * len(self.get_state())
        self.step_update_status = None
        self.step_lens_target = [None] * len(self.get_state())
        self.step_input_agent_id = None
        self.temp_new_state = None

    def seed_agent_update(self, seed_list, lens_in_file,
                          self_ex_file_location, self_state_out_file,
                          criterion, epsilon):
        '''Update a seeded agent.

        Before this funciton is called, the `seed_agent_no_update` function
        needs to be called

        Args:

            seed_list (list): list of values that will be used as seed.
            Typically self.prototype will be passed in for this value, but the
            parameter exists so other values can be passed in as the seed.
            However this parameter is not needed in this funciton anymore
            because of a previous refactoring.  This is an artifact, and the
            seeding is handeled in the `seed_agent_no_update` function

            lens_in_file (string): full path to where the .in file needed to
            update the agent

            self_ex_file_location (string): full path of where the ex file is.
            since the seeded agent will use itself as the input, the self ex
            file location should be what the infl ex file location would
            normally be in the simulation

            self_state_out_file (string): full path of where the outfile will
            be.  This is the file that is written out from LENS, and is used to
            update the agent's current state

            criterion (int): criterion

            epsilon (float): probability of a mutation on each processing unit

        Returns:
            None

        '''
        self.write_to_ex(self_ex_file_location, write_type='state')
        # run lens
        state_env = self.get_env_for_pos_neg_bank_values()
        state_env['c'] = str(criterion)
        self._call_lens(lens_in_file, env=state_env)
        # capture output and set as state
        self.new_state_values = self._get_new_state_values_from_out_file(
            self_state_out_file)
        print('new', self.new_state_values)
        self.set_state(self.new_state_values)

    def seed_agent_no_update(self, seed_list, epsilon):
        '''Seeds the agent with a given value and epsilon.

        This funciton only seeds the system.  It does not prompt the agent to
        update itself after seeding.

        Args:

            seed_list (list): list of values that will be used as seed.
            Typically self.prototype will be passed in for this value, but the
            parameter exists so other values can be passed in as the seed.
            It is currently using self.prototype and needs to be fixed

            epsilon (float): probability of mutation on each processing unit

        Returns:
            None

        '''
        assert(len(self.prototype) > 0)
        assert(isinstance(self.prototype, list))
        print('prototype: ', str(self.prototype))
        print('self.prototype: ', str(self.prototype))

        if epsilon == 0:
            self.set_state(self.prototype)
            assert self.get_state() == self.prototype
        else:
            assert(epsilon >= 0 and epsilon <= 1)
            seed_values = self.mutate(self.prototype, epsilon)
            self.set_state(seed_values)

    def set_prototype(self, list_of_values):
        """Set prototype values

        Args:

            list_of_values (list): list of values to set the prototype to

        Returns:
            None
        """
        self.prototype = list_of_values[:]

    def set_state(self, list_of_values):
        """Set state values

        Args:

            list_of_values (list): list of values to set the agent state to

        Returns:

            None
        """
        # sets state to list of values
        # list slicing is the fastest according to stackoverflow:
        # http://stackoverflow.com/questions/2612802/
        # how-to-clone-or-copy-a-list-in-python
        # print('list of values length:', len(list_of_values))
        # print('state length:', len(self.state))
        if len(list_of_values) == len(self.state):
            self.state = list_of_values[:]
        else:
            raise ValueError("len of values not equal to len of state")

    def get_pos_neg_bank_values(self):
        """Get the activation values in the positive and negative banks

        Positive values are the first half of the agent state
        Negative values are the second half of the agent state

        :returns: positive values in the first index, neg values in second index
        :rtype: typle
        """
        # TODO this should be a hidden function
        # banks = ('p', 'n')
        num_units_per_bank = self._length_per_bank()
        pos = self.get_state()[:num_units_per_bank]
        neg = self.get_state()[num_units_per_bank:]
        return (pos, neg)


    def get_padded_agent_id(self, total_number_of_characters=6):
        format_string = "{{0:0{}d}}".format(total_number_of_characters)
        return format_string.format(self.get_key())


    def get_env_for_pos_neg_bank_values(self):
        # TODO this should be a hidden function
        current_env = os.environ
        # padded_agent_number = "{0:06d}".format(self.get_key())
        # padded_agent_number = self.get_padded_agent_id()
        # current_env['a'] = padded_agent_number
        for idx_bank, bank in enumerate(('p', 'n')):
            bank_values = self.get_pos_neg_bank_values()[idx_bank]
            # print(bank_values, file=sys.stderr)
            for idx_pu, j in enumerate(bank_values):
                var_key = str(bank) + str(idx_pu)
                var_value = str(bank_values[idx_pu])
                # print('key: ', var_key, '; value: ', var_value)
                # setattr(current_env, var_to_export, var_to_export)
                # current_env.putenv(var_key, var_value)
                current_env[var_key] = var_value
                # print(current_env.get(var_to_export))
                # print(current_env.get(var_key))
        return current_env

    def update_agent_state(self, pick='default', **kwargs):
        # if there is an agent_state_out_file, clear it
        # this makes sure there will be nothing appended
        if kwargs.get('agent_state_out_file') is not None:
            open(kwargs.get('agent_state_out_file'), 'w').close()
            assert os.stat(kwargs.get('agent_state_out_file')).st_size == 0
        if pick == 'default':
            self._update_agent_state_default(kwargs.get('lens_in_file'),
                                             kwargs.get('agent_ex_file'),
                                             kwargs.get('infl_ex_file'),
                                             kwargs.get(
                                                 'agent_state_out_file'),
                                             kwargs.get('criterion')
                                             )
            self.num_update += 1
        else:
            raise ValueError('Algorithm used for pick unknown')

    def write_ex_attitude(self, list_to_write, base_name_text, base_name_number,
                          fdir, **kwargs):
        """
        kwargs passed into `open()`
        """
        # print(fdir, file=sys.stderr)
        with open(fdir, kwargs['mode']) as f:
            write_string = 'name: {}{}\nI: {};\n'.format(base_name_text,
                                                       base_name_number,
                                                       self._list_to_str_delim(
                                                           list_to_write, ' '))
            f.write(write_string)

    def write_to_ex(self, file_dir, write_type='state', **kwargs):
        '''
        file_dir should be in the ./tests/lens/ folder
        usually the file will be something like
        agent.ex for the agent or
        infl.ex for the influencing agent
        '''
        write_file_path = file_dir

        if write_type == 'state':
            try:
                # print('trying to open file to write state')
                with open(write_file_path, 'w') as f:
                    '''
                    should look something like this:
                    name: sit1
                    I: 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ;
                    '''
                    f.write('name: sit1\n')
                    # assert False
                    lens_agent_state_str = self._list_to_str_delim(
                        self.state, " ")
                    input_line = 'B: ' + lens_agent_state_str + ' ;'
                    f.write(input_line)
            except:
                assert False, 'write_type == "state" failed'
        if write_type == 'sit':
            try:
                with open(file_dir, 'w') as f:
                    # print('weight_ex_list', kwargs.get('weight_ex_list'))
                    # print('type: ', type(kwargs.get('weight_ex_list')))
                    assert isinstance(kwargs.get('weight_ex_list'), list)
                    for i in range(len(kwargs.get('weight_ex_list'))):
                        self._write_sit_to_ex(kwargs.get('weight_ex_list')[i],
                                              i, f)
            except:
                assert False, 'write_type == "sit" failed'
