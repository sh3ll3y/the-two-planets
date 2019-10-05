import unittest

from collections import OrderedDict
import the_two_planets as tp


class ValidateInputTest(unittest.TestCase):
    """Validates user input."""

    def test_validate_input_with_correct_format(self):
        input_str = "Falicornia attacks with 100 H, 101 E, 20 AT, 5 SG"
        observed_result = tp.validate_input_format(
            input_str)
        self.assertTrue(observed_result)

    def test_validate_input_with_incorrect_format(self):
        input_str = "California attacks with 100 H, 101 E, 20 AT, 5 SG"
        with self.assertRaises(tp.InputFormatError):
            tp.validate_input_format(input_str)

    def test_falicornia_attack_units_with_sufficient_base_passes_validation(
            self):
        fal_attack_units = OrderedDict(
            [('horses', 250), ('elephants', 50), ('armoured_tanks', 20), ('sling_guns', 15)])
        observed_result = tp.validate_fal_attack_units(fal_attack_units)
        self.assertEqual(fal_attack_units, observed_result)

    def test_falicornia_attack_units_with_insufficient_base_raises_exception(
            self):
        fal_attack_units = OrderedDict(
            [('horses', 999), ('elephants', 50), ('armoured_tanks', 20), ('sling_guns', 15)])
        with self.assertRaises(tp.InsufficientUnitsError):
            tp.validate_fal_attack_units(fal_attack_units)
