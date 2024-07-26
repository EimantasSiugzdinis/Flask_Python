import unittest
from gas import Gas


class TestGasSuite(unittest.TestCase):
    def setUp(self):
        self.gas = Gas("2024-07-19 10:00:00", "o2", 25.0)

    def test_init_bad_value(self):
        with self.assertRaises(ValueError):
            bad_gas_initiazlion = Gas("2024-07-19 11:00:00", "o2", "I_passed_string_")

    def test_add_value(self):
        self.gas.add_value(30.0)
        self.assertEqual(self.gas.values, [25.0, 30.0])

    def test_add_invalid_value(self):
        with self.assertRaises(ValueError):
            self.gas.add_value("Im_a_string_that_wants_to_break_you")

    def test_get_average(self):
        self.gas.add_value(30.0)
        self.assertEqual(self.gas.get_average(), 27.5)

    def test_get_max(self):
        self.gas.add_value(30.0)
        self.assertEqual(self.gas.get_max(), 30.0)

    def test_get_min(self):
        self.gas.add_value(30.0)
        self.assertEqual(self.gas.get_min(), 25.0)

    def test_get_gas_type(self):
        self.assertEqual(self.gas.get_gas_type(), "o2")

    # this test is made on purpose to fail
    def test_negative_test(self):
        self.assertEqual(self.gas.get_gas_type(), "gas_gas_gas")


if __name__ == "__main__":
    unittest.main()
