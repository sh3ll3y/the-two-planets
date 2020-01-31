import army
import unittest

from army import Army
from army_config import army_data
from collections import OrderedDict
from io import StringIO
from unittest.mock import patch
from .test_data import test_army_data
from war_result_outputter import WarResultOutputter


class WarResultOutputterTest(unittest.TestCase):
    """Tests for WarResultOutputter class."""


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
