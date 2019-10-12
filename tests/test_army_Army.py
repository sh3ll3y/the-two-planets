import army
import unittest

from army import Army
from army_config import army_data
from collections import OrderedDict
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
                                                                         5)]))]))]))])


class ArmyTest(unittest.TestCase):
    """Tests for the Army class."""

    def _set_up_test_Army(self):
        self.army_name = 'armytwo'
        self.test_army = Army(self.army_name)

    def test_army_class_initiation(self):
        self._set_up_test_Army()
        self.assertEqual(self.test_army.army_name, self.army_name)
        self.assertEqual(self.test_army.battalions, [])
        self.assertIsNone(self.test_army.counter_attack)

    def test_prepare_battalions_adds_same_number_of_battalions_to_armytwo(
            self):
        self._set_up_test_Army()
        with patch.dict(army_data, test_army_data, clear=True):
            counter_attack = OrderedDict(
                [('TBI', 20), ('TBII', 10)])
            self.test_army.prepare_battalions(counter_attack)
            self.assertEqual(len(self.test_army.battalions), 2)

    def test_prepare_battalions_with_invalid_counter_battalions_raises_exception(
            self):
        self._set_up_test_Army()
        with patch.dict(army_data, test_army_data, clear=True):
            counter_attack = OrderedDict(
                [('invalid_battalion', 20), ('TBII', 10)])
            with self.assertRaises(army.InvalidCounterBattalionsError):
                self.test_army.prepare_battalions(counter_attack)

    def test_prepare_battalions_with_valid_counter_battalions_but_invalid_order_raises_exception(
            self):
        self._set_up_test_Army()
        with patch.dict(army_data, test_army_data, clear=True):
            counter_attack = OrderedDict(
                [('TBII', 10), ('TBI', 20)])
            with self.assertRaises(army.InvalidCounterBattalionsError):
                self.test_army.prepare_battalions(counter_attack)

    def test_prepare_battalions_prepares_home_battalions_using_power_rule(
            self):
        self._set_up_test_Army()
        with patch.dict(army_data, test_army_data, clear=True):
            counter_attack = OrderedDict(
                [('TBI', 20), ('TBII', 10)])
            self.test_army.prepare_battalions(counter_attack)
            # Required units of home battalions are half of the counter
            # battalions.
            self.assertEqual(self.test_army.battalions[0].required_units, 10)
            self.assertEqual(self.test_army.battalions[1].required_units, 5)

    def test_two_adjacent_battalions_complies_with_substitution_and_substitution_choice_rules_when_lower_rank_is_deficient_and_higher_rank_is_not(
            self):
        self._set_up_test_Army()
        with patch.dict(army_data, test_army_data, clear=True):
            counter_attack = OrderedDict(
                [('TBI', 22), ('TBII', 10)])
            LOWER_CONVERSION = 0.5
            HIGHER_CONVERSION = 2
            self.test_army.prepare_battalions(counter_attack)
            home_batln_one = self.test_army.battalions[0]
            home_batln_two = self.test_army.battalions[1]
            self.test_army._calibrate_adj_bat(
                home_batln_one,
                home_batln_two,
                LOWER_CONVERSION,
                HIGHER_CONVERSION)
            # We deploy only lower rank battalion as higher rank battalion can
            # still calibrate with the next adjacent battalion.
            self.test_army.deploy_units(home_batln_one)
            self.assertEqual(self.test_army.battalions[0].required_units, 10)
            self.assertEqual(self.test_army.battalions[1].required_units, 5)

    def test_two_adjacent_battalions_complies_with_substitution_and_substitution_choice_rules_when_higher_rank_is_deficient_and_lower_rank_is_not(
            self):
        self._set_up_test_Army()
        with patch.dict(army_data, test_army_data, clear=True):
            counter_attack = OrderedDict(
                [('TBI', 20), ('TBII', 16)])
            LOWER_CONVERSION = 0.5
            HIGHER_CONVERSION = 2
            self.test_army.prepare_battalions(counter_attack)
            home_batln_one = self.test_army.battalions[0]
            home_batln_two = self.test_army.battalions[1]
            self.test_army._calibrate_adj_bat(
                home_batln_two,
                home_batln_one,
                HIGHER_CONVERSION,
                LOWER_CONVERSION)
            # We deploy only lower rank battalion as higher rank battalion can
            # still calibrate with the next adjacent battalion.
            self.test_army.deploy_units(home_batln_one)
            self.assertEqual(self.test_army.battalions[0].required_units, 10)
            self.assertEqual(self.test_army.battalions[1].required_units, 8)

    def test_final_deploy_units_returns_true_if_required_units_is_less_than_base_units(
            self):
        self._set_up_test_Army()
        with patch.dict(army_data, test_army_data, clear=True):
            counter_attack = OrderedDict(
                [('TBI', 20), ('TBII', 16)])
            self.test_army.prepare_battalions(counter_attack)
            # required units of this is 10 which is equal to base units.
            test_batln = self.test_army.battalions[0]
            self.assertTrue(self.test_army.deploy_units(test_batln))

    def test_final_deploy_units_returns_false_if_required_units_is_less_than_base_units(
            self):
        self._set_up_test_Army()
        with patch.dict(army_data, test_army_data, clear=True):
            counter_attack = OrderedDict(
                [('TBI', 40), ('TBII', 16)])
            self.test_army.prepare_battalions(counter_attack)
            # required units of this is 20 which is more than base units.
            test_batln = self.test_army.battalions[0]
            self.assertFalse(self.test_army.deploy_units(test_batln))

    def test_calibrate_battalions_and_loses(self):
        self._set_up_test_Army()
        with patch.dict(army_data, test_army_data, clear=True):
            counter_attack = OrderedDict(
                [('TBI', 40), ('TBII', 16)])
            self.test_army.prepare_battalions(counter_attack)
            expected_army_name = 'armytwo'
            expected_attack_units = OrderedDict(
                [('TBI', 10), ('TBII', 5)])
            expected_result = False
            army_name, attack_units, result = self.test_army.calibrate()
            self.assertEqual(army_name, expected_army_name)
            self.assertEqual(attack_units, expected_attack_units)
            self.assertEqual(result, expected_result)

    def test_calibrate_battalions_and_wins(self):
        self._set_up_test_Army()
        with patch.dict(army_data, test_army_data, clear=True):
            counter_attack = OrderedDict(
                [('TBI', 22), ('TBII', 2)])
            self.test_army.prepare_battalions(counter_attack)
            expected_army_name = 'armytwo'
            expected_attack_units = OrderedDict(
                [('TBI', 10), ('TBII', 2)])
            expected_result = True
            army_name, attack_units, result = self.test_army.calibrate()
            self.assertEqual(army_name, expected_army_name)
            self.assertEqual(attack_units, expected_attack_units)
            self.assertEqual(result, expected_result)
