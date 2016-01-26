from mann import agent
import mann.helper
import mann.lens_in_writer

class LensAgentWatts(agent.LensAgent):
    agent_count = 0

    def __init__(self, num_state_vars):
        self.agent_id = LensAgentWatts.agent_count
        LensAgentWatts.agent_count += 1

        # the state represents all the values
        # pos state values are the first half
        # nig state values are the second half
        assert num_state_vars % 2 == 0
        self.state = [0] * num_state_vars
        self.len_per_bank = int(num_state_vars / 2)
        self.pos_state = self.state[ :self.len_per_bank]
        self.neg_state = self.state[self.len_per_bank :]
        self.predecessors = []
        self.num_update = 0
        self.temp_new_state = None # used for simultaneous/sequential updateing

    def __hash__(self):
        return(hash(self.agent_id))

    def __eq__(self, x, y):
        return x.agent_id == y.agent_id

    def create_weight_file(self, weight_in_file_path, weight_directory,
                           ex_file_path, prototype, prototype_mutation_prob,
                           **kwargs):
        padded_agent_number = self.get_padded_agent_id()
        np = len(self.predecessors)

        ex_file_string = 'test'
        # need to see which way is easier, providing a list of values seems easier
        # we can use this to write the ex file and call lens
        self.write_lens_ex_file(
            exfile_path)
        assert False, 'fail in create weight file'

    def write_lens_ex_file(self, file_to_write,
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
