"""Module that holds the Battalion class."""


class BattalionError(Exception):
    """Base class for Battalion exceptions."""
    pass


class RequiredUnitsNotIntegerError(BattalionError):
    """Exception raised if battalion units is not an integer."""
    pass


class Battalion(object):
    """Class that represents a battalion."""

    def __init__(
            self,
            army_name,
            battalion_initials,
            battalion_name,
            rank,
            base_units,
            required_units):
        self.army_name = army_name
        self.battalion_initials = battalion_initials
        self.battalion_name = battalion_name
        self.rank = rank
        self.base_units = base_units
        self.required_units = required_units

    def is_deficient(self):
        return self.required_units > self.base_units

    def get_deficient_units(self):
        if self.is_deficient():
            return self.required_units - self.base_units
        return 0

    def add_to_required_units(self, units):
        if not isinstance(units, int):
            raise RequiredUnitsNotIntegerError(
                units, 'Required units to add should be an integer.')
        self.required_units += units

    def update_required_units(self, units):
        if not isinstance(units, int):
            raise RequiredUnitsNotIntegerError(
                units, 'Required units to update should be an integer.')
        self.required_units = units

    def remove_from_required_units(self, units):
        if not isinstance(units, int):
            raise RequiredUnitsNotIntegerError(
                units, 'Units to remove should be an integer.')
        self.required_units -= units
