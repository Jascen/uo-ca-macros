class CraftMenuItem:
    """An item that is selectable in the crafting menu"""
    def __init__(self, graphic, button_one, button_two, name, hue = 0):
        self.graphic = graphic
        self.button_one = button_one # Category
        self.button_two = button_two # Item
        self.name = name
        self.hue = hue
        
    def __str__(self):
        return self.name