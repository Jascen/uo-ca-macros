from entities.resourcetype import LeatherResourceType, MetalResourceType, WoodResourceType
from entities.generalitem import Board, Ingot, Leather
from models.craftresourceitem import CraftResourceItem


class _CraftResourceItemFactory:
    @staticmethod
    def create_ingot(resource):
        return CraftResourceItem(Ingot.graphic, resource.name, resource.hue, 50, 300)


    @staticmethod
    def create_leather(resource):
        return CraftResourceItem(Leather.graphic, resource.name, resource.hue, 50, 300)


    @staticmethod
    def create_board(resource):
        return CraftResourceItem(Board.graphic, resource.name, resource.hue, 50, 300)


class LeatherResource:
    Leather        = _CraftResourceItemFactory.create_leather(LeatherResourceType.Leather)
    Lizard         = _CraftResourceItemFactory.create_leather(LeatherResourceType.Lizard)
    Serpent        = _CraftResourceItemFactory.create_leather(LeatherResourceType.Serpent)
    Necrotic       = _CraftResourceItemFactory.create_leather(LeatherResourceType.Necrotic)
    Volcanic       = _CraftResourceItemFactory.create_leather(LeatherResourceType.Volcanic)
    Frozen         = _CraftResourceItemFactory.create_leather(LeatherResourceType.Frozen)
    DeepSea        = _CraftResourceItemFactory.create_leather(LeatherResourceType.DeepSea)
    Goliath        = _CraftResourceItemFactory.create_leather(LeatherResourceType.Goliath)
    Draconic       = _CraftResourceItemFactory.create_leather(LeatherResourceType.Draconic)
    Hellish        = _CraftResourceItemFactory.create_leather(LeatherResourceType.Hellish)
    Dinosaur       = _CraftResourceItemFactory.create_leather(LeatherResourceType.Dinosaur)
    Alien          = _CraftResourceItemFactory.create_leather(LeatherResourceType.Alien)


class IngotResource:
    Iron           = _CraftResourceItemFactory.create_ingot(MetalResourceType.Iron)
    DullCopper     = _CraftResourceItemFactory.create_ingot(MetalResourceType.DullCopper)
    ShadowIron     = _CraftResourceItemFactory.create_ingot(MetalResourceType.ShadowIron)
    Copper         = _CraftResourceItemFactory.create_ingot(MetalResourceType.Copper)
    Bronze         = _CraftResourceItemFactory.create_ingot(MetalResourceType.Bronze)
    Golden         = _CraftResourceItemFactory.create_ingot(MetalResourceType.Golden)
    Agapite        = _CraftResourceItemFactory.create_ingot(MetalResourceType.Agapite)
    Verite         = _CraftResourceItemFactory.create_ingot(MetalResourceType.Verite)
    Valorite       = _CraftResourceItemFactory.create_ingot(MetalResourceType.Valorite)
    Nepturite      = _CraftResourceItemFactory.create_ingot(MetalResourceType.Nepturite)
    Obsidian       = _CraftResourceItemFactory.create_ingot(MetalResourceType.Obsidian)
    Steel          = _CraftResourceItemFactory.create_ingot(MetalResourceType.Steel)
    Brass          = _CraftResourceItemFactory.create_ingot(MetalResourceType.Brass)
    Mithril        = _CraftResourceItemFactory.create_ingot(MetalResourceType.Mithril)
    Xormite        = _CraftResourceItemFactory.create_ingot(MetalResourceType.Xormite)
    Dwarven        = _CraftResourceItemFactory.create_ingot(MetalResourceType.Dwarven)


class BoardResource:
    Wood           = _CraftResourceItemFactory.create_board(WoodResourceType.Wood)
    Ash            = _CraftResourceItemFactory.create_board(WoodResourceType.Ash)
    Cherry         = _CraftResourceItemFactory.create_board(WoodResourceType.Cherry)
    Ebony          = _CraftResourceItemFactory.create_board(WoodResourceType.Ebony)
    GoldenOak      = _CraftResourceItemFactory.create_board(WoodResourceType.GoldenOak)
    Hickory        = _CraftResourceItemFactory.create_board(WoodResourceType.Hickory)
    Mohagony       = _CraftResourceItemFactory.create_board(WoodResourceType.Mohagony)
    Driftwood      = _CraftResourceItemFactory.create_board(WoodResourceType.Driftwood)
    Oak            = _CraftResourceItemFactory.create_board(WoodResourceType.Oak)
    Pine           = _CraftResourceItemFactory.create_board(WoodResourceType.Pine)
    Ghost          = _CraftResourceItemFactory.create_board(WoodResourceType.Ghost)
    Rosewood       = _CraftResourceItemFactory.create_board(WoodResourceType.Rosewood)
    Walnut         = _CraftResourceItemFactory.create_board(WoodResourceType.Walnut)
    Petrified      = _CraftResourceItemFactory.create_board(WoodResourceType.Petrified)
    Elven          = _CraftResourceItemFactory.create_board(WoodResourceType.Elven)