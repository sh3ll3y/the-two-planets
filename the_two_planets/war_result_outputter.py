""" Class that outputs the result of the war. """

class WarResultOutputterException(Exception):
    """Exception raised if army does not comply with AbstractArmy."""
    pass


class InvalidArmyError(WarResultOutputterException):
    """Exception raised if army does not comply with AbstractArmy."""
    pass


class WarResultOutputter(object):
    """Outputs the result of the war."""

    def __init__(self, army_object):
        # if not isinstance(army_object, AbstractArmy):
        #     raise InvalidArmyError(army_object, "This is an invalid army.")
        self.army_obj = army_object

    def __build_standard_output_pattern(self, batlns_len):
        prefix = '{} deploys '
        mid = '{} {}, ' * batlns_len
        mid = mid[:-2]
        suffix = ' and {}'
        return prefix + mid + suffix

    def print_standard_output(self):
        """Prints the output of war in standard format."""
        army_name, attack_units, result = self.army_obj.calibrate()
        output_pattern = self.__build_standard_output_pattern(
            len(attack_units))
        inject = []
        for batln in attack_units:
            inject.append(attack_units[batln])
            inject.append(batln)
        outcome = 'wins' if result else 'loses'
        print(output_pattern.format(army_name.capitalize(), *inject, outcome))
