import army
import unittest

from army import Battalion


class BattalionTest(unittest.TestCase):
    """Tests for the Battalion class."""

    def _set_up_test_battalion(self):
        self.army_name = 'test_army'
        self.battalion_initials = 'TB'
        self.battalion_name = 'test_battalion'
        self.rank = 1
        self.base_units = 1000
        self.required_units = 500
        self.batln = Battalion(
            self.army_name,
            self.battalion_initials,
            self.battalion_name,
            self.rank,
            self.base_units,
            self.required_units)

    def test_battalion_class_initiation(self):
        self._set_up_test_battalion()
        self.assertEqual(self.batln.army_name, self.army_name)
        self.assertEqual(self.batln.battalion_initials, self.battalion_initials)
        self.assertEqual(self.batln.battalion_name, self.battalion_name)
        self.assertEqual(self.batln.rank, self.rank)
        self.assertEqual(self.batln.base_units, self.base_units)
        self.assertEqual(self.batln.required_units, self.required_units)

    def test_is_deficient_returns_false_when_enough_base_units(self):
        self._set_up_test_battalion()
        observed = self.batln.is_deficient()
        # Here base units is 1000 and required units is 500
        self.assertEqual(False, observed)

    def test_is_deficient_returns_true_when_not_enough_base_units(self):
        self._set_up_test_battalion()
        self.batln.required_units = 999999
        observed = self.batln.is_deficient()
        # Here base units is 1000 and required units is 999999
        self.assertEqual(True, observed)

    def test_get_deficient_units_return_zero_if_not_deficient(self):
        self._set_up_test_battalion()
        observed = self.batln.get_deficient_units()
        # Here base units is 1000 and required units is 500
        self.assertEqual(0, observed)

    def test_to_add_required_units_to_the_battalion(self):
        self._set_up_test_battalion()
        self.batln.add_to_required_units(50)
        # Original required units is 500
        self.assertEqual(550, self.batln.required_units)

    def test_to_udpate_required_units_in_the_battalion(self):
        self._set_up_test_battalion()
        self.batln.update_required_units(99)
        # Original required units is 500
        self.assertEqual(99, self.batln.required_units)

    def test_to_remove_required_units_in_the_battalion(self):
        self._set_up_test_battalion()
        self.batln.remove_from_required_units(100)
        # Original required units is 500
        self.assertEqual(400, self.batln.required_units)

    def test_add_to_require_units_raises_if_invalid_units_data_type_passed(
            self):
        self._set_up_test_battalion()
        with self.assertRaises(army.RequiredUnitsNotIntegerError):
            self.batln.add_to_required_units('fifty')

    def test_udpate_required_units_raises_if_invalid_units_data_type_passed(
            self):
        self._set_up_test_battalion()
        with self.assertRaises(army.RequiredUnitsNotIntegerError):
            self.batln.update_required_units('sixty')

    def test_remove_required_units_raises_if_invalid_units_data_type_passed(
            self):
        self._set_up_test_battalion()
        with self.assertRaises(army.RequiredUnitsNotIntegerError):
            self.batln.remove_from_required_units('hundred')
