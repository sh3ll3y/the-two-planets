
import json
import re

from army import Army, WarResultOutputter
from army_config import army_data
from collections import OrderedDict


class ValidationError(Exception):
    """Base class for exceptions in this module."""
    pass


class InputFormatError(ValidationError):
    """Exception raised for errors in the input format."""
    pass


class InsufficientUnitsError(ValidationError):
    """Exception raised if attack units is more than base units."""
    pass


def validate_input_format(input_str):
    """Validates the format of the input received."""

    input_pattern = (r'Falicornia attacks with (?P<horses>[0-9]+) H, '
                     r'(?P<elephants>[0-9]+) E, '
                     r'(?P<armoured_tanks>[0-9]+) AT, '
                     r'(?P<sling_guns>[0-9]+) SG$')

    match_obj = re.match(input_pattern, input_str)
    if not match_obj:
        raise InputFormatError(input_str, "Error in input format.")
    return match_obj


def validate_fal_attack_units(attack_units):
    """Validates the attack units of Falicornia army."""
    fal_batlns = army_data['army']['falicornia']
    for bat in fal_batlns:
        if fal_batlns[bat]['base_units'] > attack_units[bat]:
            continue
        else:
            raise InsufficientUnitsError(
                attack_units, "One or more attack units more than base units.")
    return attack_units


def main(input_str):
    match_obj = validate_input_format(input_str)
    fal_attack = match_obj.groupdict()

    fal_attack_units = OrderedDict()
    for order in army_data['army']['falicornia'].keys():
        fal_attack_units[order] = int(fal_attack[order])

    fal_attack_units = validate_fal_attack_units(
        fal_attack_units)
    print(fal_attack_units)
    leng_army = Army('lengaburu')
    leng_army.prepare_battalions(fal_attack_units)
    output = WarResultOutputter(leng_army)
    output.print_standard_output()


if __name__ == '__main__':
    input_str = input()
    main(input_str)
