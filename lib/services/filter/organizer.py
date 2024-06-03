class Organizer:
    def __init__(self, source, destination, filters):
        self.source = source
        self.destination = destination
        self.filters = filters


    def Test(self, item):
        for filter in self.filters:
            if filter.Test(item): return True
        return False