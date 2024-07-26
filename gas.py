class Gas:
    def __init__(self, timestamp, gas_type, value):
        self.gas = gas_type
        self.timestamp = [timestamp]
        self.values = []
        self.add_value(value)

    def add_value(self, value):
        try:
            value = float(value)
            self.values.append(value)
        except ValueError:
            raise ValueError(f"The value '{value}' is not a valid float")

    def get_average(self):
        return sum(self.values) / len(self.values) if self.values else 0.0

    def get_max(self):
        return max(self.values) if self.values else 0.0

    def get_min(self):
        return (
            min(self.values) if self.values else 0.0
        )  # return null? for the ones above as well?

    def get_gas_type(self):
        return self.gas
