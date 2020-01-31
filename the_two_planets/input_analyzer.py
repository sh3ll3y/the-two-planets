""" Module to analyze input format."""

import re

from army_config import army_data
from collections import OrderedDict
from operator import eq

class StandardInput(object):
    """Class that represents the pattern and details of the standard input format.
    Supports any number of battalions in this pattern including new additions."""

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


class_map = {'standard_input': StandardInput, }


class InputAnalyzerError(Exception):
    """Base class for InputAnalyzer class."""
    pass


class InputFormatError(InputAnalyzerError):
    """Exception raised when input is not in the list of accepted input formats."""
    pass


class InputAnalyzer(object):
    """Helps to match the input with their respective clases for processing."""

    def __init__(self, input_str):
        self.input_str = input_str
        self.analyzer = None

    def validate_input_format(self):
        for class_name in class_map:
            match_obj = re.match(class_map[class_name].pattern, self.input_str)
            if match_obj:
                self.analyzer = class_map[class_name](
                    self.input_str, match_obj)
                return True
        raise InputFormatError(self.input_str, "Invalid input format.")
