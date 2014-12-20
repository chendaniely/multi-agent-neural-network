#!/usr/bin/env python

import random
import subprocess
import io
import os
import sys
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

        parameters
        ----------
        none

        return
        ------
        a tuple that represents the unique keys of the agent
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

        parameters
        ----------
        a lit of predecessors

        returns
        -------
        none
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

        returns
        -------
        returns an integer value of 0 or 1 for a state
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


class LensAgent(Agent):
    agent_count = 0
    prototypes = []

    def __init__(self, num_state_vars):
        '''
        num_state_vars is the total number of elements the agent has as a state
        for LENS, this is the total number of processing units per agent
        that is, the number of positive valence bank units
        and the number of negative valence bank units
        '''
        assert(len(LensAgent.prototypes) > 0,
               "LensAgent prototypes need to be set before creating "
               "LensAgent instance")

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

    def set_lens_agent_prototypes(number_of_prototypes):
        list_of_prototypes = list(LensAgent._create_prototype(20,
                                                              [0, 1], [.5, .5])
                                  for x in range(number_of_prototypes))
        assert isinstance(list_of_prototypes[0], list)
        LensAgent.prototypes = list_of_prototypes
        print('list of prototypes created: ', str(list_of_prototypes))

    def _call_lens(self, lens_in_file, **kwargs):
        # pass
        subprocess.call(['lens', '-batch', lens_in_file],
                        env=kwargs.get('env'))
        # '/home/dchen/Desktop/ModelTesting/MainM1PlautFix2.in'])

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

    def _flip_1_0_value(self, number):
        assert isinstance(number, int), 'number to flip is not int'
        if number == 0:
            return 1
        elif number == 1:
            return 0
        else:
            raise ValueError('Number to flip not 0 or 1')

    def _get_new_state_values_from_out_file(self, file_dir, column=0):
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
        return list_of_new_state

    def _length_per_bank(self):
        num_elements_per_bank = len(self.get_state())/2
        assert str(num_elements_per_bank).split('.')[1] == '0'
        return int(num_elements_per_bank)

    def _list_to_str_delim(self, list_to_convert, delim):
        '''
        takes in a list and returns a string of list by the delim
        used to write out agent state out to file
        '''
        return delim.join(map(str, list_to_convert))

    def _pad_agent_id(self):
        pass  # TODO

    def _start_end_update_out(self, f):
        # enter the actual file line numbers
        # the 1 offset is used in the actual fxn call
        # f is the .out file to be read
        # TODO pass these values in from config file
        return tuple([5, 14, 15, 24])

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

    def _str_to_int_list(self, string):
        '''Returns a list of ints from a comma separated string of int values
        used for creating a prototype list from a config file (which is a str)
        '''
        return list(int(s) for s in string.strip().split(','))

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

    def create_weight_file(self, weight_in_file, weight_output_dir,
                           base_example, num_train_examples,
                           prototype_mutation_prob, criterion):
        '''
        calls ._create_weight_training_examples to create list of training ex
        calls ._write_to_ex to write list of train ex to create the .ex files
        calls lens to create .wt weight files

        Returns
        -------
        None
        '''
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
        return self.state

    def reset_step_variables(self):
        '''Variables and states that will be written to output file
        This is called after Agent Initialization to set all values to None
        '''
        self.step_input_state_values = [None] * len(self.get_state())
        self.step_update_status = None
        self.step_lens_target = [None] * len(self.get_state())
        self.step_input_agent_id = None

    def seed_agent_update(self, seed_list, lens_in_file,
                          self_ex_file_location, self_state_out_file,
                          criterion, epsilon):
        '''Seed agent
        before this funciton is called, the seed_agent_no_update function
        needs to be called
        This is really hacky code that should be fixed.
        '''
        # self.state = [1] * len(self.state)
        # train weights already done during the network creating process
        # set input as base example

        # list_of_values = self._str_to_int_list(weightBaseExample)
        # TODO this is why i'm complaining of hacky code
        # this assumes the seed_no_update has already been ran
        # prototype = self._str_to_int_list(weightBaseExample)
        # assert(prototype == self.prototype)
        # if epsilon == 0:
        #     assert self.get_state() == self.prototype
        #     self.set_state(self.prototype)
        # else:
        #     assert(epsilon >= 0 and epsilon <= 1)
        #     seed_values = self.mutate(prototype, epsilon)
        #     self.set_state(seed_values)
        # self.set_state(list_of_values)

        # self.seed_agent_no_update(weightBaseExample, epsilon)

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
        '''Set the agent state to weightBaseExample
        however do not call lens get output based on trained weights
        '''
        # TODO THIS IS HACKY AS HELL becuase the seed_agent sets this
        # and updates, this funciton should be the 'seed'
        # and we call the update on this agent independently
        # currently we are double setting the state
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
        self.prototype = list_of_values[:]

    def set_state(self, list_of_values):
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
        # TODO this should be a hidden function
        # banks = ('p', 'n')
        num_units_per_bank = self._length_per_bank()
        pos = self.get_state()[:num_units_per_bank]
        neg = self.get_state()[num_units_per_bank:]
        return (pos, neg)

    def get_env_for_pos_neg_bank_values(self):
        # TODO this should be a hidden function
        current_env = os.environ
        padded_agent_number = "{0:06d}".format(self.get_key())
        current_env['a'] = padded_agent_number
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

    def mutate(self, list_to_mutate, mutation_prob):
        '''Mutates each element of a list by the mutation_prob
        Mutating means flipping the 1 to a 0 or vice versa

        This calculation is usually used to create the training situations
        by mutating the prototype to create training examples

        This is used by the seeding function to mutate the prototype by
        the mutation_prob to do the initial seed.

        if the mutation_prob == 0, then the prototype is returned
        else, there is a probabliy that prototype is still returned
        '''
        if mutation_prob > 0.0 and mutation_prob <= 1:
            post_mutation_list = list_to_mutate[:]
            for idx, value in enumerate(list_to_mutate):
                prob = random.random()
                if prob <= mutation_prob:
                    post_mutation_list[idx] = self._flip_1_0_value(value)
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
