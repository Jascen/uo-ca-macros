class CraftMenuMaterial:
    """A material that is selectable in the crafting menu"""
    def __init__(self, name, hue, material_button, material_type_button):
        self.name = name
        self.hue = hue
        self.material_button = material_button
        self.material_type_button = material_type_button