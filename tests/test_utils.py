import utils
import unittest

class UtilsTest(unittest.TestCase):
    """Validates the utils module."""

    def test_check_a_number_and_a_half_is_rouded_to_the_next_whole_number(self):
        observed = utils.round_up(6.5)
        self.assertEqual(7, observed)

    def test_check_a_number_is_halfed_rouded_to_the_next_whole_number(self):
        observed = utils.round_up(5, half_it=True)
        self.assertEqual(3, observed)
