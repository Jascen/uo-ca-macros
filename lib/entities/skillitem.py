from models.skillitem import SkillItem
from entities.craftresourceitem import CraftResourceItem, BoardResource
from entities.generalitem import Log, Board
from entities.resourcetype import WoodResourceType


class _SkillItemFactory:
    @staticmethod
    def create_lumberjack(resource_type, min_skill, max_skill):
        craft_resource = CraftResourceItem(Log.graphic, resource_type.name, resource_type.hue, 1, 1)

        return SkillItem(Board, craft_resource, min_skill, max_skill)


class LumberjackSkillItem:
    Wood          = _SkillItemFactory.create_lumberjack(WoodResourceType.Wood, 0, 65.0)
    Ash           = _SkillItemFactory.create_lumberjack(WoodResourceType.Ash, 55, 80.0)
    Cherry        = _SkillItemFactory.create_lumberjack(WoodResourceType.Cherry, 60, 85.0)
    Ebony         = _SkillItemFactory.create_lumberjack(WoodResourceType.Ebony, 65, 90.0)
    GoldenOak     = _SkillItemFactory.create_lumberjack(WoodResourceType.GoldenOak, 70, 95.0)
    Hickory       = _SkillItemFactory.create_lumberjack(WoodResourceType.Hickory, 75, 100.0)
    Mohagony      = _SkillItemFactory.create_lumberjack(WoodResourceType.Mohagony, 80, 105.0)
    Driftwood     = _SkillItemFactory.create_lumberjack(WoodResourceType.Driftwood, 80, 105.0)
    Oak           = _SkillItemFactory.create_lumberjack(WoodResourceType.Oak, 85, 110.0)
    Pine          = _SkillItemFactory.create_lumberjack(WoodResourceType.Pine, 90, 115.0)
    Rosewood      = _SkillItemFactory.create_lumberjack(WoodResourceType.Rosewood, 95, 120.0)
    Walnut        = _SkillItemFactory.create_lumberjack(WoodResourceType.Walnut, 99, 124.0)
    Elven         = _SkillItemFactory.create_lumberjack(WoodResourceType.Elven, 100.1, 125.1)