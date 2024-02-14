from entities.craftmenuitem import Mace, PlatemailGorget, RoyalGorget, ShortSpear
from entities.craftresourceitem import IngotResource
from models.skillitem import SkillItem
from services.craft import CraftServiceFactory, CraftingSkill
from services.salvage import Salvager
from utility.alias import AliasUtils
from utility.skill import SkillUtils


def LoreThenSmelt(item):
    SkillUtils.ArmsLore(item, True)
    Salvager.Smelt(item)


def Main():
    resource_container = "resource_container"
    AliasUtils.PromptContainer(resource_container)
    service = CraftServiceFactory.Create(CraftingSkill.Blacksmith, resource_container)
    
    iron_ingots = [IngotResource.Iron]
    all_items = [
        SkillItem(Mace, iron_ingots, 14.5, 45.4), # 64.5 max
        SkillItem(ShortSpear, iron_ingots, 45.3, 85.3), # 95.3 max
        SkillItem(PlatemailGorget, iron_ingots, 80.4, 95.4), # 106.4 max
        SkillItem(RoyalGorget, iron_ingots, 95.4, 100.0), # 106.4 max
    ]
    
    service.Level(all_items, LoreThenSmelt)
    Pause(1000)


# Execute Main()
Main()