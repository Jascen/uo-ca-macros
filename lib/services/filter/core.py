class MultiFilterBase:
    def __init__(self, filters):
        self.filters = filters

    def __str__(self):
        return ", ".join(map(str, self.filters))

class MetaFilterBase:
    def __init__(self, filter):
        self.filter = filter

    def __str__(self):
        return str(self.filter)