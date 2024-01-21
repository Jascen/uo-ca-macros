class CraftableItem:
    def __init__(self, graphic, button_one, button_two, name, hue = 0):
        self.graphic = graphic
        self.button_one = button_one
        self.button_two = button_two
        self.name = name
        self.hue = hue
        
    def __str__(self):
        return self.name


class SkillItem:
    def __init__(self, item, material, min_level, max_level):
        self.item = item
        self.min_level = min_level
        self.max_level = max_level

        if not isinstance(material, list): material = [material] # Convert a single entity into an array
        self.material = material
        
    def __str__(self):
        return "{} ({} to {})".format(self.item.name, self.min_level, self.max_level)