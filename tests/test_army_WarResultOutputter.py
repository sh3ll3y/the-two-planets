import army
import unittest

from army import Army, WarResultOutputter
from army_config import army_data
from collections import OrderedDict
from io import StringIO
from unittest.mock import patch

test_army_data = OrderedDict([('army',
                               OrderedDict([('enemy_army',
                                             OrderedDict([('test_battalion_one',
                                                           OrderedDict([('rank', 2),
                                                                        ('base_units', 40)])),
                                                          ('test_battalion_two',
                                                           OrderedDict([('rank', 1),
                                                                        ('base_units', 20)]))])),
                                            ('home_army',
                                             OrderedDict([('test_battalion_one',
                                                           OrderedDict([('rank', 2),
                                                                        ('base_units', 10)])),
                                                          ('test_battalion_two',
                                                           OrderedDict([('rank', 1),
                                                                        ('base_units',
                                                                         5)]))]))])),
                              ('abbrev',
                               OrderedDict([('test_battalion_one', 'TB1'),
                                            ('test_battalion_two', 'TB2')]))])


class WarResultOutputterTest(unittest.TestCase):
    """Tests for WarResultOutputter class."""

    def _set_up_test_army_and_prepares_battalions(self):
        with patch.dict(army_data, test_army_data, clear=True):
            counter_attack = OrderedDict(
                [('test_battalion_one', 40), ('test_battalion_two', 16)])
            self.test_army = Army('home_army')
            self.test_army.prepare_battalions(counter_attack)

    def test_passing_army_that_does_not_interface_with_AbstractArmy_throws_exception(
            self):
        class Army(object):  # Does not inherit AbstractArmy
            """The army class."""

            def __init__(self, army_name):
                self.army = army_name
                self.battalions = []
                self.counter_attack = None

        army_obj = Army('test_army')
        with self.assertRaises(army.InvalidArmyError):
            output = WarResultOutputter(army_obj)

    def test_print_standard_output_method_prints_in_the_expected_format(self):
        with patch.dict(army_data, test_army_data, clear=True):
            counter_attack = OrderedDict(
                [('test_battalion_one', 40), ('test_battalion_two', 16)])
            self.test_army = Army('home_army')
            self.test_army.prepare_battalions(counter_attack)
            output = WarResultOutputter(self.test_army)
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                output.print_standard_output()
                self.assertEqual(
                    fakeOutput.getvalue().strip(),
                    'Home_army deploys 10 TB1, 5 TB2 and loses')
