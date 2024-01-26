from items.resource import *


class CraftResource:
    def __init__(self, graphic, name, hue, min_pack_amount, restock_amount):
        self.graphic = graphic
        self.name = name
        self.hue = hue
        self.min_pack_amount = min_pack_amount
        self.restock_amount = restock_amount


    def __str__(self):
        return self.name

    
    @staticmethod
    def fromTemplate(template, resource):
        return CraftResource(template.graphic, resource.name, resource.hue, template.min_pack_amount, template.restock_amount)


class _CraftingResourceTemplate:
    def __init__(self, graphic, min_pack_amount, restock_amount):
        self.graphic = graphic
        self.min_pack_amount = min_pack_amount
        self.restock_amount = restock_amount


_IngotTemplate = _CraftingResourceTemplate(0x1bf2, 50, 300)
class CraftIngot:
    Iron           = CraftResource.fromTemplate(_IngotTemplate, Iron)
    DullCopper     = CraftResource.fromTemplate(_IngotTemplate, DullCopper)
    ShadowIron     = CraftResource.fromTemplate(_IngotTemplate, ShadowIron)
    Copper         = CraftResource.fromTemplate(_IngotTemplate, Copper)
    Bronze         = CraftResource.fromTemplate(_IngotTemplate, Bronze)
    Golden         = CraftResource.fromTemplate(_IngotTemplate, Golden)
    Agapite        = CraftResource.fromTemplate(_IngotTemplate, Agapite)
    Verite         = CraftResource.fromTemplate(_IngotTemplate, Verite)
    Valorite       = CraftResource.fromTemplate(_IngotTemplate, Valorite)
    Nepturite      = CraftResource.fromTemplate(_IngotTemplate, Nepturite)
    Obsidian       = CraftResource.fromTemplate(_IngotTemplate, Obsidian)
    Steel          = CraftResource.fromTemplate(_IngotTemplate, Steel)
    Brass          = CraftResource.fromTemplate(_IngotTemplate, Brass)
    Mithril        = CraftResource.fromTemplate(_IngotTemplate, Mithril)
    Xormite        = CraftResource.fromTemplate(_IngotTemplate, Xormite)
    Dwarven        = CraftResource.fromTemplate(_IngotTemplate, Dwarven)


_BoardTemplate = _CraftingResourceTemplate(0x1bd7, 50, 300)
class CraftBoard:
    Wood           = CraftResource.fromTemplate(_BoardTemplate, Wood)
    Ash            = CraftResource.fromTemplate(_BoardTemplate, Ash)
    Cherry         = CraftResource.fromTemplate(_BoardTemplate, Cherry)
    Ebony          = CraftResource.fromTemplate(_BoardTemplate, Ebony)
    GoldenOak      = CraftResource.fromTemplate(_BoardTemplate, GoldenOak)
    Hickory        = CraftResource.fromTemplate(_BoardTemplate, Hickory)
    Mohagony       = CraftResource.fromTemplate(_BoardTemplate, Mohagony)
    Driftwood      = CraftResource.fromTemplate(_BoardTemplate, Driftwood)
    Oak            = CraftResource.fromTemplate(_BoardTemplate, Oak)
    Pine           = CraftResource.fromTemplate(_BoardTemplate, Pine)
    Ghost          = CraftResource.fromTemplate(_BoardTemplate, Ghost)
    Rosewood       = CraftResource.fromTemplate(_BoardTemplate, Rosewood)
    Walnut         = CraftResource.fromTemplate(_BoardTemplate, Walnut)
    Petrified      = CraftResource.fromTemplate(_BoardTemplate, Petrified)
    Elven          = CraftResource.fromTemplate(_BoardTemplate, Elven)


_LeatherTemplate = _CraftingResourceTemplate(0x1081, 50, 300)
class CraftLeather:
    Leather        = CraftResource.fromTemplate(_LeatherTemplate, Leather)
    Lizard         = CraftResource.fromTemplate(_LeatherTemplate, Lizard)
    Serpent        = CraftResource.fromTemplate(_LeatherTemplate, Serpent)
    Necrotic       = CraftResource.fromTemplate(_LeatherTemplate, Necrotic)
    Volcanic       = CraftResource.fromTemplate(_LeatherTemplate, Volcanic)
    Frozen         = CraftResource.fromTemplate(_LeatherTemplate, Frozen)
    DeepSea        = CraftResource.fromTemplate(_LeatherTemplate, DeepSea)
    Goliath        = CraftResource.fromTemplate(_LeatherTemplate, Goliath)
    Draconic       = CraftResource.fromTemplate(_LeatherTemplate, Draconic)
    Hellish        = CraftResource.fromTemplate(_LeatherTemplate, Hellish)
    Dinosaur       = CraftResource.fromTemplate(_LeatherTemplate, Dinosaur)
    Alien          = CraftResource.fromTemplate(_LeatherTemplate, Alien)