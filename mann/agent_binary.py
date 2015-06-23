#! /usr/bin/env python

import random
import logging

import mann.agent


class BinaryAgent(mann.agent.Agent):
    binary_agent_count = 0

    def __init__(self, threshold, max_flips):
        self.agent_id = BinaryAgent.binary_agent_count
        BinaryAgent.binary_agent_count += 1

        self.state = 0
        self.num_update = 0
        self.step_update_status = 0
        self.predecessors = [None]
        self.temp_new_state = None

        self.threshold = threshold
        self.max_flips = float(max_flips)
        self.num_flipped = 0

        self.reset_step_variables()

    # def set_binary_state(self, value):
    #     # binary state means 0 or 1
    #     assert value in [0, 1],\
    #         "binary state can only be 0 or 1, got %r" % value

    #     # make sure we are only changing the state when the value is different
    #     assert value != self.binary_state, "changing state to same value"

    #     self.binary_state = value

    # def get_state(self):
    #     return self.binary_state

    def seed_agent(self, seed_value=1):
        """Seed agent
        """
        self.state = seed_value
        return(self)

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

    def reset_step_variables(self):
        self.step_update_status = None
        self.temp_new_state = None
        return(self)

    def _update_agent_state_default(self):
        '''
        Looks at the list of predecessors for the selected agent
        randomly picks one of them
        if the selected predecessor is has a different state
        there will be a 70% chance that the selected agent will change states
        to match the predecessor's state
        otherwise no state is changed

        TODO NEEDS REVIEW
        '''
        # print('in _update_agent_state_default')
        # print("type of predecssors: ",  type(self.predecessors))  # list
        # print("container of predecessors: ", self.predecessors)
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

    def _update_agent_state_threshold_watts(self, update):
        """Update agent according to watts threshold model.
        Calculates how many prdecessors have a state of 1.
        If the proportion of predecessors with 1 is greater or equal than the
        agenet's threshold, the agent will flip to 1.
        Agents under the watts threshold do not flip back to 0
        """
        if self.has_predecessor():
            if self.state == 1:
                logging.info('skipping _update_agent_state_threshold_watts, '
                             'because self.state is 1')
                return(self)
            else:
                total_1 = 0
                total_p = 0
                for idx, predecessor in enumerate(self.predecessors):
                    if predecessor.state == 1:
                        total_1 += 1
                    total_p += 1
                logging.info('Final: total_1 / total_p: {} / {}'.
                             format(total_1, total_p))
                if total_1 / float(total_p) >= self.threshold:
                    logging.info('New state is 1')
                    self.step_update_status = 1
                    new_state = 1
                else:
                    logging.info('New state is remains 0')
                    new_state = 0
                if update == 'simultaneous':
                    logging.info('SIMULTANEOUS: Assign temp_new_state to {}'.
                                 format(new_state))
                    self.temp_new_state = new_state
                elif update == 'sequential':
                    logging.info('SEQUENTIAL: Assing state to {}'.
                                 format(new_state))
                    self.state = new_state
                return(self)
        else:
            return(self)

    def _update_agent_state_threshold_watts_flip(self, update):
        """Uses the watts threshold model to calculate state change, however
        this method allows the agent to flip back to 0, instead of just
        flipping to a 1 state.

        :param update: simultaneous or sequential updateing
        :type update: str
        """
        if self.has_predecessor():
            total_opposite = 0
            total_predecessors = 0
            if self.state == 1:
                for predecessor in self.predecessors:
                    if predecessor.state == 0:
                        total_opposite += 1
                    total_predecessors += 1
            elif self.state == 0:
                for predecessor in self.predecessors:
                    if predecessor.state == 1:
                        total_opposite += 1
                    total_predecessors += 1
            else:
                raise ValueError("Unknown state for watts flip")

            assert total_predecessors == len(self.predecessors)
            prop_opposite = total_opposite / float(total_predecessors)
            if prop_opposite >= self.threshold:
                if self.state == 1:
                    new_state = 0
                elif self.state == 0:
                    new_state = 1
                else:
                    ValueError("Unknown state")
            else:
                logging.info("State unchanged: {}".format(self.state))
                new_state = self.state

            if update == 'simultaneous':
                logging.info('SIMULTANEOUS: Assign temp_new_state to {}'.
                             format(new_state))
                self.temp_new_state = new_state

            elif update == 'sequential':
                logging.info('SEQUENTIAL: Assing state to {}'.
                             format(new_state))
                self.state = new_state
            else:
                raise ValueError("Unknown update type")
        else:
            logging.info("Agent {} has no predecessors".format(self.agent_id))
            return(self)

    def update_agent_state(self, update, pick='default'):
        '''
        update: simultaneous or sequential
        pick = 'default': uses the update_agent__state_default algorithm
        can be 'threshold_watts'
        '''
        # print('in update_agent_state')
        # print('has predecessors', self.has_predecessor())
        if self.has_predecessor():
            if pick == 'default':
                self._update_agent_state_default()
            elif pick == 'threshold_watts':
                self._update_agent_state_threshold_watts(update)
            elif pick == 'threshold_watts_flip':
                self._update_agent_state_threshold_watts_flip(update)
            else:
                raise ValueError("Algorithm used for pick unknown")
        else:
            logging.warning('Agent {} has no precessors.'.
                            format(self.agent_id))

    @property
    def agent_id(self):
        return self._agent_id

    @agent_id.setter
    def agent_id(self, id_value):
        self._agent_id = id_value

    @property
    def num_update(self):
        return self._num_update

    @num_update.setter
    def num_update(self, num):
        assert num == 0 or num == self._num_update + 1,\
            "Tried to increment num_update by {}, which is not 1".\
            format(str(num))
        self._num_update = num

    @property
    def num_flipped(self):
        return self._num_flipped

    @num_flipped.setter
    def num_flipped(self, value):
        self._num_flipped = value

    @property
    def max_flips(self):
        return self._max_flip

    @max_flips.setter
    def max_flips(self, value):
        assert value >= 0,\
            "Max flip needs to be greater than 0, {} given".format(value)
        self._max_flip = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        assert new_state in [0, 1, None], \
            "New state for BinaryAgent must be 0, 1, or None.  "\
            "Tried to set a value of {}".\
            format(str(new_state))
        self._state = new_state

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, threshold):
        self._threshold = threshold
