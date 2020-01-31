import data_validation as dv
import unittest

from army_config import army_data
from collections import OrderedDict
from unittest.mock import patch
from .test_data import test_army_data


class TestValidateAttackData(unittest.TestCase):
    """Tests to validate attack data."""

    def test_validate_attack_data_method_raises_if_invalid_army_is_passed(
            self):
        attack_units = OrderedDict([('TBI', 40), ('TBII', 16)])
        with patch.dict(army_data, test_army_data, clear=True):
            with self.assertRaises(dv.InvalidArmyError):
                dv.validate_attack_data('invalid_army_name', attack_units)

    def test_validate_attack_data_method_raises_if_invalid_battalion_is_passed(
            self):
        attack_units = OrderedDict(
            [('IAM_AN_INVALID_BATTALION', 40), ('TBII', 16)])
        with patch.dict(army_data, test_army_data, clear=True):
            with self.assertRaises(dv.InvalidBattalionError):
                dv.validate_attack_data('armyone', attack_units)

    def test_validate_attack_data_method_raises_if_valid_battalions_passed_in_invalid_order(
            self):
        attack_units = OrderedDict(
            [('TBII', 16), ('TBI', 40)])
        with patch.dict(army_data, test_army_data, clear=True):
            with self.assertRaises(dv.InvalidBattalionError):
                dv.validate_attack_data('armyone', attack_units)

    def test_validate_attack_data_method_raises_if_insufficient_attack_units_is_passed(
            self):
        attack_units = OrderedDict([('TBI', 99999), ('TBII', 16)])
        with patch.dict(army_data, test_army_data, clear=True):
            with self.assertRaises(dv.InsufficientUnitsError):
                dv.validate_attack_data('armyone', attack_units)

    def test_validate_attack_data_method_returns_True_if_all_validataions_pass(
            self):
        attack_units = OrderedDict([('TBI', 9), ('TBII', 16)])
        with patch.dict(army_data, test_army_data, clear=True):
            self.assertTrue(dv.validate_attack_data('armyone', attack_units))
