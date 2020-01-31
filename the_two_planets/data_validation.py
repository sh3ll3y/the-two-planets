""" Module to validate input data."""

import re

from army_config import army_data
from operator import eq

class ValidateAttackData(Exception):
    """Base class to represent input data validation."""


class InvalidArmyError(ValidateAttackData):
    """Exception raised when an army is invalid."""


class InvalidBattalionError(ValidateAttackData):
    """Exception raised when a battalion is invalid."""


class InsufficientUnitsError(ValidateAttackData):
    """Exception raised when attack units are more than base units."""


def validate_attack_data(army_name, attack_units):
    """Takes the army_name as string and attack_units as OrderedDict."""

    accepted_armies = army_data['army'].keys()
    if army_name not in accepted_armies:
        raise InvalidArmyError(army_name, "This is an invalid army.")
    accepted_batlns = army_data['army'][army_name].keys()
    attack_batlns = attack_units.keys()
    if not (accepted_batlns == attack_batlns and all(
            map(eq, accepted_batlns, attack_batlns))):
        raise InvalidBattalionError(attack_units, "Attack units invalid or not in order.")
    for batln in attack_units:
        if army_data['army'][army_name][batln]['base_units'] < attack_units[batln]:
            raise InsufficientUnitsError(
                batln, "Battalion attack units more than base units.")
    return True
