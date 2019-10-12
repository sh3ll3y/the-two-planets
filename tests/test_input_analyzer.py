import input_analyzer as ia
import unittest
import re

from army_config import army_data
from collections import OrderedDict
from input_analyzer import InputAnalyzer, StandardInput
from unittest.mock import patch


test_army_data = OrderedDict([('army',
                               OrderedDict([('armyone',
                                             OrderedDict([('TBI',
                                                           OrderedDict([('battalion_name', 'test_battalion_one'),
                                                                        ('rank', 2),
                                                                        ('base_units', 40)])),
                                                          ('TBII',
                                                           OrderedDict([('battalion_name', 'test_battalion_two'),
                                                                        ('rank', 1),
                                                                        ('base_units', 20)]))])),
                                            ('armytwo',
                                             OrderedDict([('TBI',
                                                           OrderedDict([('battalion_name', 'test_battalion_one'),
                                                                        ('rank', 2),
                                                                        ('base_units', 10)])),
                                                          ('TBII',
                                                           OrderedDict([('battalion_name', 'test_battalion_two'),
                                                                        ('rank', 1),
                                                                        ('base_units',
                                                                         5)]))]))])),
                                                                                    ])


class TestInputAnalyzer(unittest.TestCase):
    """Tests for the InputAnalyzer class."""

    def _set_up_test_InputAnalyser(self):
        self.input_str = 'Testarmy attacks with 10 A, 20 B'
        self.test_obj = InputAnalyzer(self.input_str)

    def test_set_up_InputAnalyser_initiation(self):
        self._set_up_test_InputAnalyser()
        self.assertEqual(self.test_obj.input_str, self.input_str)
        self.assertIsNone(self.test_obj.analyzer)

    def test_validate_input_with_an_acceptable_format(self):
        self._set_up_test_InputAnalyser()
        #The input string passed to InputAnalyzer in set_up method is in the standard input format and we expect this validation to pass.
        result = self.test_obj.validate_input_format()
        self.assertTrue(result)

    def test_validate_input_with_invalid_format_raises_exception(self):
        test_obj = InputAnalyzer('This is an input string in an invalid format')
        #The input string is in invalid format and we expect to raise an exception.
        with self.assertRaises(ia.InputFormatError):
            result = test_obj.validate_input_format()


class TestStandardInput(unittest.TestCase):
    """Tests for the StandardInput class."""

    def _set_up_test_StandardInput(self):
        std_input_pattern = r'(?P<army_name>[A-Z][a-z]+)( attacks with )((?:[0-9]+ [A-Z]+, )+)?([0-9]+ [A-Z]+)$'
        self.input_str = 'Enemy attacks with 40 TBI, 16 TBII'
        self.match_obj = re.match(std_input_pattern, self.input_str)
        self.analyzer = StandardInput(self.input_str, self.match_obj)

    def test_StandardInput_initiation(self):
        self._set_up_test_StandardInput()
        self.assertEqual(self.analyzer.input_str, self.input_str)
        self.assertEqual(self.analyzer.match_obj, self.match_obj)

    def test_get_attack_details_returns_expected_output(self):
        self._set_up_test_StandardInput()
        expected_army_name = 'enemy'
        expected_battalions = OrderedDict([('TBI', 40), ('TBII', 16)])
        received_army_name, received_battalions = self.analyzer.get_attack_details()
        self.assertEqual(expected_army_name, received_army_name)
        self.assertEqual(expected_battalions, received_battalions)


class TestValidateAttackData(unittest.TestCase):
    """Tests to validate attack data."""

    def test_validate_attack_data_method_raises_if_invalid_army_is_passed(self):
        attack_units = OrderedDict([('TBI', 40), ('TBII', 16)])
        with patch.dict(army_data, test_army_data, clear=True):
            with self.assertRaises(ia.InvalidArmyError):
                ia.validate_attack_data('invalid_army_name', attack_units)

    def test_validate_attack_data_method_raises_if_invalid_battalion_is_passed(self):
        attack_units = OrderedDict([('IAM_AN_INVALID_BATTALION', 40), ('TBII', 16)])
        with patch.dict(army_data, test_army_data, clear=True):
            with self.assertRaises(ia.InvalidBattalionError):
                ia.validate_attack_data('armyone', attack_units)

    def test_validate_attack_data_method_raises_if_insufficient_attack_units_is_passed(self):
        attack_units = OrderedDict([('TBI', 99999), ('TBII', 16)])
        with patch.dict(army_data, test_army_data, clear=True):
            with self.assertRaises(ia.InsufficientUnitsError):
                ia.validate_attack_data('armyone', attack_units)

    def test_validate_attack_data_method_returns_True_if_all_validataions_pass(self):
        attack_units = OrderedDict([('TBI', 9), ('TBII', 16)])
        with patch.dict(army_data, test_army_data, clear=True):
            self.assertTrue(ia.validate_attack_data('armyone', attack_units))
