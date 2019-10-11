import re

from army_config import army_data
from collections import OrderedDict


class InputError(Exception):
    """Base class for exceptions in this module."""
    pass


class InputFormatError(InputError):
    """Exception raised for errors in the input format."""
    pass


class StandardInput(object):
    pattern = r'(?P<army_name>[A-Z][a-z]+)( attacks with )((?:[0-9]+ [A-Z]+, )+)?([0-9]+ [A-Z]+)$'

    def validate_enemy_attack_units(self):
        batln_pattern = r'([0-9]+ [A-Z]+)'
        result = re.findall(batln_pattern, self.input_pattern)
        batlns = [_batln.split(' ') for _batln in result]
        enemy_attack_units = OrderedDict()
        for batln in batlns:


class_map = {'standard_input': StandardInput,}

class InputAnalyzer(object):
    def __init__(self, input_str):
        self.input_pattern = input_pattern
        self.formatter = None

    def validate_input_format(self):
        for class in class_map:
            if re.match(class_map[class].pattern, self.input_str):
                self.formatter = class_map[class]()
                return True
        raise InputFormatError(self.input_pattern, "Invalid input format.")
