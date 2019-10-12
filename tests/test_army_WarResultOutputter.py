import army
import unittest

from army import Army, WarResultOutputter
from army_config import army_data
from collections import OrderedDict
from io import StringIO
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


class WarResultOutputterTest(unittest.TestCase):
    """Tests for WarResultOutputter class."""

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
                [('TBI', 40), ('TBII', 16)])
            self.test_army = Army('armytwo')
            self.test_army.prepare_battalions(counter_attack)
            output = WarResultOutputter(self.test_army)
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                output.print_standard_output()
                self.assertEqual(
                    fakeOutput.getvalue().strip(),
                    'Armytwo deploys 10 TBI, 5 TBII and loses')
