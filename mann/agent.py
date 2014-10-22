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

#    def get_agent_step_info(self):
#        '''
#        THIS FUNCTION IS NOT USED
#        returns
#        -------
#        a dictionary of values to be saved on each step of a model run
#        '''
#        return {
#            'key': self.get_key(),
#            'binary_state': self.binary_state
#        }


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
        print('in _update_agent_state_default')
        print("type of predecssors: ",  type(self.predecessors))  # list
        print("container of predessors: ", self.predecessors)
        predecessor_picked = random.sample(list(self.predecessors), 1)[0]
        print("predecessor picked: ", predecessor_picked)
        print("predecessor picked key: ", predecessor_picked.get_key())
        if self.binary_state == predecessor_picked.binary_state:
            print("no update required, binary states are the same")
            print("self.binary_state = ", self.binary_state)
            print("predecessor_picked.binary_state = ",
                  predecessor_picked.binary_state)
            pass
        else:
            print('updateing agent state')
            random_number = random.random()
            if random_number < 0.7:
                self.set_binary_state(predecessor_picked.binary_state)
            else:
                pass

    def update_agent_state(self, pick='default'):
        '''
        pick = 'default': uses the update_agent__state_default algorithm
        '''
        print('in update_agent_state')
        print('has predecessors', self.has_predessor())
        if self.has_predessor():
            if pick == 'default':
                self._update_agent_state_default()
            else:
                raise ValueError("Algorithm used for pick unknown")
        else:
            pass


class LensAgent(Agent):
    lens_agent_count = 0

    def __init__(self, num_state_vars):
        '''
        num_state_vars is the total number of elements the agent has as a state
        for LENS, this is the total number of processing units per agent
        that is, the number of positive valence bank units
        and the number of negative valence bank units
        '''
        self.agent_id = LensAgent.lens_agent_count
        LensAgent.lens_agent_count += 1

        self.state = [0] * num_state_vars
        self.predecessors = []

    # def set_lens_agent_state(self, list_of_processing_unit_activations):
    #     print(len(list_of_processing_unit_activations))
    #     print(len(self.state))
    #     is_len_equal = len(list_of_processing_unit_activations) ==\
    #         len(self.state)

    #     print(is_len_equal)

    #     if():
    #         self.state = list_of_processing_unit_activations[:]
    #     else:
    #         raise ValueError("length of processing units to assign state\
    #                          not equal to lengh of state")

    def get_state(self):
        return self.state

    def _list_to_str_delim(self, list_to_convert, delim):
        '''
        takes in a list and returns a string of list by the delim
        used to write out agent state out to file
        '''
        return delim.join(map(str, list_to_convert))

    def seed_agent(self):
        self.state = [1] * len(self.state)

    def set_state(self, list_of_values):
        # sets state to list of values
        # list slicing is the fastest according to stackoverflow:
        # http://stackoverflow.com/questions/2612802/
        # how-to-clone-or-copy-a-list-in-python
        print('list of values length:', len(list_of_values))
        print('state length:', len(self.state))
        if len(list_of_values) == len(self.state):
            self.state = list_of_values[:]
        else:
            raise ValueError("len of values not equal to len of state")

    def create_weight_file(self, weight_in_file, weight_output_dir,
                           base_example, num_train_examples,
                           num_train_mutations):
        # print('weight in file read: ', weight_in_file)
        # print('weight output read: ', weight_output_dir)

        # TODO make this lins a function
        padded_agent_number = "{0:06d}".format(self.get_key())
        assert len(padded_agent_number) == 6, 'padded key len in wgt file err'

        weight_file_name = 'AgentWgt' + padded_agent_number + '.wt'
        weight_file_dir = weight_output_dir + '/' + weight_file_name

        # if the path does not exist, create it
        if not os.path.exists(weight_output_dir):
            os.makedirs(weight_output_dir)
        # print('weight file name: ', weight_file_name)
        # print('weight file dir: ', weight_file_dir)

        # copy current envvironment
        lens_env = os.environ
        # export variable w into environment as the padded agent number
        # TODO make env 'w' env 'a' to match in file name
        lens_env["w"] = padded_agent_number
        print('w environment: ', lens_env.get('w'))
        print('w environment: ', lens_env.get('w'), file=sys.stderr)

        self._train_weights(base_example,
                            num_train_examples,
                            num_train_mutations)

        # list of 'words' passed into the subprocess call
        lens_weight_command = ['lens', ' -nogui',  weight_in_file]
        # print('lens weight list: ', lens_weight_command)
        subprocess.call(['lens', '-nogui', weight_in_file], env=lens_env)
        # print('ls call: ', subprocess.call(['ls']))
        # return weight_file_name

    def _call_lens(self, lens_in_file, **kwargs):
        # pass
        subprocess.call(['lens', '-nogui', lens_in_file],
                        env=kwargs.get('env'))
        # '/home/dchen/Desktop/ModelTesting/MainM1PlautFix2.in'])

    def _start_end_update_out(self, f):
        # enter the actual file line numbers
        # the 1 offset is used in the actual fxn call
        # f is the .out file to be read
        return tuple([122, 126, 128, 132])

    def _get_new_state_values_from_out_file(self, file_dir):
        list_of_new_state = []

        # here = os.path.abspath(os.path.dirname(__file__))
        # read_file_path = here + '/' + file_dir
        read_file_path = file_dir
        print('read_file_path: ', read_file_path)
        print('files here', os.listdir("./"))

        with open(read_file_path, 'r') as f:
            start_bank1, end_bank1, start_bank2, end_bank2 = \
                self._start_end_update_out(f)
            for line_idx, line in enumerate(f):
                print(line)
                line_num = line_idx + 1  # python starts from line 0
                if start_bank1 <= line_num <= end_bank1 or \
                   start_bank2 <= line_num <= end_bank2:
                    # in a line that I want to save information for
                    first_col = line.strip().split(' ')[0]
                    list_of_new_state.append(float(first_col))
                    print('list of new state', list_of_new_state)
        return list_of_new_state

    def _length_per_bank(self):
        num_elements_per_bank = len(self.get_state())/2
        assert str(num_elements_per_bank).split('.')[1] == '0'
        return int(num_elements_per_bank)

    def get_pos_neg_bank_values(self):
        banks = ('p', 'n')
        num_units_per_bank = self._length_per_bank()
        pos = self.get_state()[:num_units_per_bank]
        neg = self.get_state()[num_units_per_bank:]
        return (pos, neg)

    def _pad_agent_id(self):
        pass  # TODO

    def get_env_for_pos_neg_bank_values(self):
        current_env = os.environ
        padded_agent_number = "{0:06d}".format(self.get_key())
        current_env['a'] = padded_agent_number
        for idx_bank, bank in enumerate(('p', 'n')):
            bank_values = self.get_pos_neg_bank_values()[idx_bank]
            print(bank_values, file=sys.stderr)
            for idx_pu, j in enumerate(bank_values):
                var_key = str(bank) + str(idx_pu)
                var_value = str(bank_values[idx_pu])
                print('key: ', var_key, '; value: ', var_value)
                # setattr(current_env, var_to_export, var_to_export)
                # current_env.putenv(var_key, var_value)
                current_env[var_key] = var_value
                # print(current_env.get(var_to_export))
                print(current_env.get(var_key))
        return current_env

    def _update_agent_state_default(self, lens_in_file, agent_ex_file,
                                    infl_ex_file, agent_state_out_file):
        if len(self.predecessors) > 0:
            predecessor_picked = random.sample(list(self.predecessors), 1)[0]
            # predecessor_picked.write_to_ex('../tests/lens/infl.ex')
            predecessor_picked.write_to_ex(infl_ex_file)
            # self.write_to_ex('../tests/lens/agent.ex')
            # self.write_to_ex(agent_ex_file)
            state_env = self.get_env_for_pos_neg_bank_values()
            self._call_lens(lens_in_file, env=state_env)
            # self.new_state_values = self._get_new_state_values_from_out_file(
            #     '../tests/lens/AgentState.out')
            self.new_state_values = self._get_new_state_values_from_out_file(
                agent_state_out_file)

            self.set_state(self.new_state_values)
        else:
            # print('no predecessors')
            warnings.warn('No predecessors for LensAgent ' + str(self.get_key),
                          UserWarning)

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
                                             kwargs.get('agent_state_out_file')
                                             )
        else:
            raise ValueError('Algorithm used for pick unknown')

    def _string_agent_state_to_ex(self):
        output = io.StringIO()
        output.write('name: sit1\n')
        lens_agent_state_str = self._list_to_str_delim(self.state, " ")
        input_line = 'I: ' + lens_agent_state_str + ' ;\n'
        output.write(input_line)
        contents = output.getvalue()
        output.close()
        print(contents)
        return contents

    # def write_to_ex(self, file_dir):
    def write_to_ex(self, file_dir, type='state'):
        '''
        file_dir should be in the ./tests/lens/ folder
        usually the file will be something like
        agent.ex for the agent or
        infl.ex for the influencing agent
        '''

        # here = os.path.abspath(os.path.dirname(__file__))
        # write_file_path = here + '/' + file_dir
        # print(here)
        # print(write_file_path)
        write_file_path = file_dir

        try:
            with open(write_file_path, 'w') as f:
                '''
                should look something like this:
                name: sit1
                I: 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ;
                '''
                f.write('name: sit1\n')

                lens_agent_state_str = self._list_to_str_delim(self.state, " ")
                input_line = 'I: ' + lens_agent_state_str + ' ;'
                f.write(input_line)
        except:
            pass

    def _flip_1_0_value(self, number):
        if number == 0:
            return 1
        if number == 1:
            return 0
        else:
            raise ValueError('Number to flip not 0 or 1')

    def _create_weight_training_examples(self, filename,
                                         base_example,
                                         num_train_examples,
                                         num_train_mutations):
        list_of_example_values = []
        open(filename, 'w').close()
        for train_example in range(num_train_examples):
            # train_list = []
            train_list = base_example[:]
            random_idx = random.randint(0, len(train_list) - 1)
            # print('random int: ', random_idx, file=sys.stderr)
            # print('train list pre : ', train_list, file=sys.stderr)
            new_value = self._flip_1_0_value(train_list[random_idx])
            # print('new value:', new_value, file=sys.stderr)
            # print('list idx value: ', train_list[random_idx],
            #       file=sys.stderr)
            train_list[random_idx] = new_value
            # print('train list post: ', train_list, file=sys.stderr)
            assert train_list is not base_example, 'lists are equal'
            list_of_example_values.append(train_list)
        return list_of_example_values

