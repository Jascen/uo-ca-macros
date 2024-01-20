from items.resource import *


class CraftMaterial:
    def __init__(self, name, hue, material_button, material_type_button):
        self.name = name
        self.hue = hue
        self.material_button = material_button
        self.material_type_button = material_type_button


    @staticmethod
    def fromResource(resource, material_type_button):
         # Note: Material button on all craft menus is '7'
        return CraftMaterial(resource.name, resource.hue, 7, material_type_button)


class Material:
# *************************
# Wood
# *************************
    Wood           = CraftMaterial.fromResource(Wood, 6)
    Ash            = CraftMaterial.fromResource(Ash, 13)
    Cherry         = CraftMaterial.fromResource(Cherry, 20)
    Ebony          = CraftMaterial.fromResource(Ebony, 27)
    GoldenOak      = CraftMaterial.fromResource(GoldenOak, 34)
    Hickory        = CraftMaterial.fromResource(Hickory, 41)
    Mohagony       = CraftMaterial.fromResource(Mohagony, 48)
    Driftwood      = CraftMaterial.fromResource(Driftwood, 55)
    Oak            = CraftMaterial.fromResource(Oak, 62)
    Pine           = CraftMaterial.fromResource(Pine, 69)
    Ghost          = CraftMaterial.fromResource(Ghost, 76)
    Rosewood       = CraftMaterial.fromResource(Rosewood, 83)
    Walnut         = CraftMaterial.fromResource(Walnut, 90)
    Petrified      = CraftMaterial.fromResource(Petrified, 97)
    Elven          = CraftMaterial.fromResource(Elven, 104)


# *************************
# Metal
# *************************
    Iron           = CraftMaterial.fromResource(Iron, 6)
    DullCopper     = CraftMaterial.fromResource(DullCopper, 13)
    ShadowIron     = CraftMaterial.fromResource(ShadowIron, 20)
    Copper         = CraftMaterial.fromResource(Copper, 27)
    Bronze         = CraftMaterial.fromResource(Bronze, 34)
    Golden         = CraftMaterial.fromResource(Golden, 41)
    Agapite        = CraftMaterial.fromResource(Agapite, 48)
    Verite         = CraftMaterial.fromResource(Verite, 55)
    Valorite       = CraftMaterial.fromResource(Valorite, 62)
    Nepturite      = CraftMaterial.fromResource(Nepturite, 69)
    Obsidian       = CraftMaterial.fromResource(Obsidian, 76)
    Steel          = CraftMaterial.fromResource(Steel, 83)
    Brass          = CraftMaterial.fromResource(Brass, 90)
    Mithril        = CraftMaterial.fromResource(Mithril, 97)
    Xormite        = CraftMaterial.fromResource(Xormite, 104)
    Dwarven        = CraftMaterial.fromResource(Dwarven, 111)


# *************************
# Leather
# *************************
    Leather        = CraftMaterial.fromResource(Leather, 6)
    Lizard         = CraftMaterial.fromResource(Lizard, 13)
    Serpent        = CraftMaterial.fromResource(Serpent, 20)
    Necrotic       = CraftMaterial.fromResource(Necrotic, 27)
    Volcanic       = CraftMaterial.fromResource(Volcanic, 34)
    Frozen         = CraftMaterial.fromResource(Frozen, 41)
    DeepSea        = CraftMaterial.fromResource(DeepSea, 48)
    Goliath        = CraftMaterial.fromResource(Goliath, 55)
    Draconic       = CraftMaterial.fromResource(Draconic, 62)
    Hellish        = CraftMaterial.fromResource(Hellish, 69)
    Dinosaur       = CraftMaterial.fromResource(Dinosaur, 76)
    Alien          = CraftMaterial.fromResource(Alien, 83)