class CraftableItem:
    def __init__(self, graphic, button_one, button_two, name, hue = 0):
        self.graphic = graphic
        self.button_one = button_one
        self.button_two = button_two
        self.name = name
        self.hue = hue
        
    def __str__(self):
        return self.name