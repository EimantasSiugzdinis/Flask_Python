import unittest
from measurements import Measurements
from gas import Gas


class TestMeasurements(unittest.TestCase):
    def setUp(self):
        self.measurements = Measurements()

    def test_add_gas_new_gas(self):
        self.measurements.add_gas("2024-07-19 10:00:00", "o2", 25.0)
        self.assertIn("o2", self.measurements.gasses)
        self.assertEqual(self.measurements.gasses["o2"].values, [25.0])

    def test_add_gas_existing_gas(self):
        self.measurements.add_gas("2024-07-19 10:00:00", "o2", 25.0)
        self.measurements.add_gas("2024-07-19 10:01:00", "o2", 30.0)
        self.assertIn("o2", self.measurements.gasses)
        self.assertEqual(self.measurements.gasses["o2"].values, [25.0, 30.0])

    def test_add_gas_new_gas(self):
        self.measurements.add_gas("2024-07-19 10:00:00", "o2", 25.0)
        self.measurements.add_gas("2024-07-19 10:01:00", "co", 30.0)
        self.assertIn("o2", self.measurements.gasses)
        self.assertEqual(self.measurements.gasses["o2"].values, [25.0])
        self.assertIn("co", self.measurements.gasses)
        self.assertEqual(self.measurements.gasses["co"].values, [30.0])

    def test_get_averages(self):
        self.measurements.add_gas("2024-07-19 10:00:00", "o2", 25.0)
        self.measurements.add_gas("2024-07-19 10:01:00", "co", 15.0)
        averages = self.measurements.get_averages()
        self.assertIn("Average of gas_type: o2 is 25.00", averages)
        self.assertIn("Average of gas_type: co is 15.00", averages)

    def test_get_averages2(self):
        self.measurements.add_gas("2024-07-19 10:00:00", "o2", 25.0)
        self.measurements.add_gas("2024-07-19 10:01:00", "o2", 30.0)
        self.measurements.add_gas("2024-07-19 10:00:00", "co", 15.0)
        self.measurements.add_gas("2024-07-19 10:01:00", "co", 20.0)
        averages = self.measurements.get_averages()
        self.assertIn("Average of gas_type: o2 is 27.50", averages)
        self.assertIn("Average of gas_type: co is 17.50", averages)

    def test_get_highest_values(self):
        self.measurements.add_gas("2024-07-19 10:00:00", "o2", 25.0)
        self.measurements.add_gas("2024-07-19 10:01:00", "o2", 30.0)
        self.measurements.add_gas("2024-07-19 10:00:00", "co", 15.0)
        self.measurements.add_gas("2024-07-19 10:01:00", "co", 20.0)
        highest_values = self.measurements.get_highest_values()
        self.assertIn("Highest value of gas_type: o2 is 30.0", highest_values)
        self.assertIn("Highest value of gas_type: co is 20.0", highest_values)

    def test_get_lowest_values(self):
        self.measurements.add_gas("2024-07-19 10:00:00", "o2", 25.0)
        self.measurements.add_gas("2024-07-19 10:01:00", "o2", 20.0)
        self.measurements.add_gas("2024-07-19 10:00:00", "co", 15.0)
        self.measurements.add_gas("2024-07-19 10:01:00", "co", 10.0)
        lowest_values = self.measurements.get_lowest_values()
        self.assertIn("Lowest value of gas_type: o2 is 20.0", lowest_values)
        self.assertIn("Lowest value of gas_type: co is 10.0", lowest_values)

    def test_invalid_gas_value(self):
        with self.assertRaises(ValueError):
            self.measurements.add_gas("2024-07-19 10:00:00", "o2", "and...broken")


if __name__ == "__main__":
    unittest.main()
