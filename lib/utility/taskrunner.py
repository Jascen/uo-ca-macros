class TaskRunner:
    """A lightweight abstraction to build and execute a list of functions"""

    def __init__(self):
        self.functions = []


    def Add(self, fn):
        """Add a function to the ordered list"""
        self.functions.append(fn)


    def Execute(self):
        """Synchronously executes the list of functions"""
        for fn in self.functions:
            fn()