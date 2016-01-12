import random

from mann import agent
import mann.helper
import mann.lens_in_writer
import mann.helper_lens_ex_writer

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
                           num_ex=50, **kwargs):
        padded_agent_number = self.get_padded_agent_id()
        np = len(self.predecessors)

        prototype = prototype[0]
        print("prototype: {}".format(prototype))
        print(type(prototype))

        all_ex = []
        for i in range(num_ex):
            all_ex.append(mann.helper.mutate(prototype, prototype_mutation_prob))
        print(all_ex)

        ex_file_string = mann.helper_lens_ex_writer.create_ex_str_from_2d_list(all_ex)

        mann.helper_lens_ex_writer.write_lens_ex_file(
            ex_file_path, string_to_write=ex_file_string)

        self.call_lens(lens_in_file_dir=weight_in_file_path,
                       lens_env={'a': padded_agent_number})
        assert False, 'fail in create weight file'
