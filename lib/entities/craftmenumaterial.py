from entities.resourcetype import *
from models.craftmenumaterial import CraftMenuMaterial


class _CraftMaterialFactory:
    @staticmethod
    def create(resource, material_type_button):
         # Note: Material button on all craft menus is '7'
        return CraftMenuMaterial(resource.name, resource.hue, 7, material_type_button)


class LeatherMenuMaterial:
    Leather        = _CraftMaterialFactory.create(LeatherResourceType.Leather, 6)
    Lizard         = _CraftMaterialFactory.create(LeatherResourceType.Lizard, 13)
    Serpent        = _CraftMaterialFactory.create(LeatherResourceType.Serpent, 20)
    Necrotic       = _CraftMaterialFactory.create(LeatherResourceType.Necrotic, 27)
    Volcanic       = _CraftMaterialFactory.create(LeatherResourceType.Volcanic, 34)
    Frozen         = _CraftMaterialFactory.create(LeatherResourceType.Frozen, 41)
    DeepSea        = _CraftMaterialFactory.create(LeatherResourceType.DeepSea, 48)
    Goliath        = _CraftMaterialFactory.create(LeatherResourceType.Goliath, 55)
    Draconic       = _CraftMaterialFactory.create(LeatherResourceType.Draconic, 62)
    Hellish        = _CraftMaterialFactory.create(LeatherResourceType.Hellish, 69)
    Dinosaur       = _CraftMaterialFactory.create(LeatherResourceType.Dinosaur, 76)
    Alien          = _CraftMaterialFactory.create(LeatherResourceType.Alien, 83)


class MetalMenuMaterial:
    Iron           = _CraftMaterialFactory.create(MetalResourceType.Iron, 6)
    DullCopper     = _CraftMaterialFactory.create(MetalResourceType.DullCopper, 13)
    ShadowIron     = _CraftMaterialFactory.create(MetalResourceType.ShadowIron, 20)
    Copper         = _CraftMaterialFactory.create(MetalResourceType.Copper, 27)
    Bronze         = _CraftMaterialFactory.create(MetalResourceType.Bronze, 34)
    Golden         = _CraftMaterialFactory.create(MetalResourceType.Golden, 41)
    Agapite        = _CraftMaterialFactory.create(MetalResourceType.Agapite, 48)
    Verite         = _CraftMaterialFactory.create(MetalResourceType.Verite, 55)
    Valorite       = _CraftMaterialFactory.create(MetalResourceType.Valorite, 62)
    Nepturite      = _CraftMaterialFactory.create(MetalResourceType.Nepturite, 69)
    Obsidian       = _CraftMaterialFactory.create(MetalResourceType.Obsidian, 76)
    Steel          = _CraftMaterialFactory.create(MetalResourceType.Steel, 83)
    Brass          = _CraftMaterialFactory.create(MetalResourceType.Brass, 90)
    Mithril        = _CraftMaterialFactory.create(MetalResourceType.Mithril, 97)
    Xormite        = _CraftMaterialFactory.create(MetalResourceType.Xormite, 104)
    Dwarven        = _CraftMaterialFactory.create(MetalResourceType.Dwarven, 111)


class WoodMenuMaterial:
    Wood           = _CraftMaterialFactory.create(WoodResourceType.Wood, 6)
    Ash            = _CraftMaterialFactory.create(WoodResourceType.Ash, 13)
    Cherry         = _CraftMaterialFactory.create(WoodResourceType.Cherry, 20)
    Ebony          = _CraftMaterialFactory.create(WoodResourceType.Ebony, 27)
    GoldenOak      = _CraftMaterialFactory.create(WoodResourceType.GoldenOak, 34)
    Hickory        = _CraftMaterialFactory.create(WoodResourceType.Hickory, 41)
    Mohagony       = _CraftMaterialFactory.create(WoodResourceType.Mohagony, 48)
    Driftwood      = _CraftMaterialFactory.create(WoodResourceType.Driftwood, 55)
    Oak            = _CraftMaterialFactory.create(WoodResourceType.Oak, 62)
    Pine           = _CraftMaterialFactory.create(WoodResourceType.Pine, 69)
    Ghost          = _CraftMaterialFactory.create(WoodResourceType.Ghost, 76)
    Rosewood       = _CraftMaterialFactory.create(WoodResourceType.Rosewood, 83)
    Walnut         = _CraftMaterialFactory.create(WoodResourceType.Walnut, 90)
    Petrified      = _CraftMaterialFactory.create(WoodResourceType.Petrified, 97)
    Elven          = _CraftMaterialFactory.create(WoodResourceType.Elven, 104)