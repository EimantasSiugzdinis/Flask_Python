from gas import gas

class measurements:
    def __init__(self):
        self.gasses = {}

    def add_gas(self, timestamp, gas_type, value):
        if gas_type in self.gasses:
            self.gasses[gas_type].add_value(value)
        else:
            self.gasses[gas_type] = gas(timestamp, gas_type, value)
    
    def get_averages(self):
        string_to_return = "["
        for gas_type in self.gasses:
            string_to_return += f"Average of gas_type: {self.gasses[gas_type].get_gas_type()} is {self.gasses[gas_type].get_average():.2f}"
            if gas_type != list(self.gasses.keys())[-1]:  # Check if it's not the last item
                string_to_return += ", "
        string_to_return += "]"

        return string_to_return

    def get_highest_values(self):
        string_to_return = "["
        for gas_type in self.gasses:
            string_to_return += f"Highest value of gas_type: {self.gasses[gas_type].get_gas_type()} is {self.gasses[gas_type].get_max()}"
            if gas_type != list(self.gasses.keys())[-1]:  # Check if it's not the last item
                string_to_return += ", "
        string_to_return += "]"

        return string_to_return

    def get_lowest_values(self):
        string_to_return = "["
        for gas_type in self.gasses:
            string_to_return += f"Highest value of gas_type: {self.gasses[gas_type].get_gas_type()} is {self.gasses[gas_type].get_min()}"
            if gas_type != list(self.gasses.keys())[-1]:  # Check if it's not the last item
                string_to_return += ", "
        string_to_return += "]"

        return string_to_return