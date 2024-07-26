from gas import Gas


class Measurements:
    def __init__(self):
        self.gasses = {}

    def add_gas(self, timestamp, gas_type, value):
        if gas_type in self.gasses:
            self.gasses[gas_type].add_value(value)
        else:
            self.gasses[gas_type] = Gas(timestamp, gas_type, value)

    def get_averages(self):

        averages = [
            f"Average of gas_type: {gas.get_gas_type()} is {gas.get_average():.2f}"
            for gas in self.gasses.values()
        ]
        return f"[{', '.join(averages)}]"

    def get_highest_values(self):

        highest_values = [
            f"Highest value of gas_type: {gas.get_gas_type()} is {gas.get_max()}"
            for gas in self.gasses.values()
        ]
        return f"[{', '.join(highest_values)}]"

    def get_lowest_values(self):

        lowest_values = [
            f"Lowest value of gas_type: {gas.get_gas_type()} is {gas.get_min()}"
            for gas in self.gasses.values()
        ]
        return f"[{', '.join(lowest_values)}]"
