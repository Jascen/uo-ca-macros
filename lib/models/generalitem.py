class GeneralItem:
    """Basic details for a single type of item"""
    def __init__(self, graphic, name, hue = -1):
        self.graphic = graphic
        self.name = name
        self.hue = hue