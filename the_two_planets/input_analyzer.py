import re

from army_config import army_data
from collections import OrderedDict


class StandardInput(object):
    """Class that represents the pattern and details of the standard input format. Supports any number of battalions including new additions."""
    pattern = r'(?P<army_name>[A-Z][a-z]+)( attacks with )((?:[0-9]+ [A-Z]+, )+)?([0-9]+ [A-Z]+)$'

    def __init__(self, input_str, match_obj):
        self.input_str = input_str
        self.match_obj = match_obj

    def get_attack_details(self):
        """Analyses the input data and returns the army and battalion details."""
        input_army_name = self.match_obj.groupdict()['army_name']
        batln_pattern = r'([0-9]+ [A-Z]+)'
        result = re.findall(batln_pattern, self.input_str)
        batlns = [_batln.split(' ') for _batln in result]
        batln_units = OrderedDict()
        for batln in batlns:
            batln_name = batln[1]
            batln_attack_units = int(batln[0])
            batln_units[batln_name] = batln_attack_units

        return input_army_name.lower(), batln_units


class_map = {'standard_input': StandardInput,}


class InputAnalyzerError(Exception):
    """Base class for InputAnalyzer class."""
    pass


class InputFormatError(InputAnalyzerError):
    """Exception raised when input is not in the list of accepted input format."""
    pass


class InputAnalyzer(object):
    def __init__(self, input_str):
        self.input_str = input_str
        self.analyzer = None

    def validate_input_format(self):
        for class_name in class_map:
            match_obj = re.match(class_map[class_name].pattern, self.input_str)
            if match_obj:
                self.analyzer = class_map[class_name](self.input_str, match_obj)
                return True
        raise InputFormatError(self.input_str, "Invalid input format.")


class ValidateAttackData(Exception):
    """Base class to represent input data validation."""


class InvalidArmyError(ValidateAttackData):
    """Exception raised when an army is invalid."""


class InvalidBattalionError(ValidateAttackData):
    """Exception raised when a battalion is invalid."""


class InsufficientUnitsError(ValidateAttackData):
    """Exception raised when attack units are more than base units."""


def validate_attack_data(army_name, attack_units):
    """Validates the attack units of an army."""
    accepted_armies = army_data['army'].keys()
    if army_name not in accepted_armies:
        raise InvalidArmyError(army_name, "This is an invalid army.")
    accepted_batlns = army_data['army'][army_name].keys()
    for batln in attack_units:
        if batln not in accepted_batlns:
            raise InvalidBattalionError(batln, "This is an invalid battalion.")
        if army_data['army'][army_name][batln]['base_units'] < attack_units[batln]:
            raise InsufficientUnitsError(batln, "Battalion attack units more than base units.")
    return True
