"""Module that holds the Army class."""

import json
import utils as _utils

from army_config import army_data
from battalion import Battalion
from collections import OrderedDict
from operator import eq

class ArmyError(Exception):
    """Base class for army exceptions."""
    pass


class BattalionsMismatchError(ArmyError):
    """Exception raised if there is a mismatch between the battlalions of two armies."""
    pass


class Army(object):
    """The army class."""

    def __init__(self, army_name):
        self.army_name = army_name
        self.battalions = []
        self.counter_attack = None

    def validate_counter_attack(self, counter_attack):
        """Validates the counter attack battalions and order."""
        home_batlns = army_data['army'][self.army_name]
        counter_batlns = counter_attack
        if counter_batlns.keys() == home_batlns.keys() and all(
                map(eq, home_batlns, counter_batlns)):
            return True
        raise BattalionsMismatchError(
            counter_attack, 'Mismatch between battalions of two armies.')

    @staticmethod
    def _calibrate_adj_bat(batln_x, batln_y, factor, reverse_factor):
        """Employs substitution and substitution choice rules to calibrate between two adjacent battalions."""
        units_to_batln_y = _utils.round_up(
            factor * batln_x.get_deficient_units())
        batln_y.add_to_required_units(units_to_batln_y)
        batln_x.update_required_units(batln_x.base_units)
        if batln_y.is_deficient():
            units_to_batln_x = _utils.round_up(
                batln_y.get_deficient_units() * reverse_factor)
            batln_x.add_to_required_units(units_to_batln_x)
            batln_y.remove_from_required_units(batln_y.get_deficient_units())

    @staticmethod
    def deploy_units(batln):
        """Deploys final attack units of the battalions."""
        if batln.is_deficient():
            batln.update_required_units(batln.base_units)
            return False
        else:
            return True

    def calibrate(self):
        """Employs all the four rules of the war to calibrate battalions."""
        LOWER_CONVERSION = 0.5
        HIGHER_CONVERSION = 2

        result = True
        total_batlns = len(self.battalions)

        for index in range(total_batlns - 1):
            low_rank_batln = self.battalions[index]
            high_rank_batln = self.battalions[index + 1]
            if low_rank_batln.is_deficient() and not high_rank_batln.is_deficient():
                self._calibrate_adj_bat(
                    low_rank_batln,
                    high_rank_batln,
                    LOWER_CONVERSION,
                    HIGHER_CONVERSION)
            if high_rank_batln.is_deficient() and not low_rank_batln.is_deficient():
                self._calibrate_adj_bat(
                    high_rank_batln,
                    low_rank_batln,
                    HIGHER_CONVERSION,
                    LOWER_CONVERSION)
            result &= self.deploy_units(low_rank_batln)
        result &= self.deploy_units(high_rank_batln)

        batlns = OrderedDict()
        for bat in self.battalions:
            batlns[bat.battalion_initials] = bat.required_units
        return self.army_name, batlns, result

    def prepare_battalions(self, counter_attack):
        """Prepares all the battalions in order using power rule."""
        if self.validate_counter_attack(counter_attack):
            # Helps to know what the counter attack is if needed later.
            self.counter_attack = counter_attack
            for batln_name in self.counter_attack:
                required_units = _utils.round_up(
                    counter_attack[batln_name], half_it=True)
                batln = Battalion(army_name=self.army_name,
                                  battalion_initials=batln_name,
                                  **army_data['army'][self.army_name][batln_name],
                                  required_units=required_units)
                self.battalions.append(batln)
