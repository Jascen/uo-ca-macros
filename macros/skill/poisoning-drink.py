from entities.craftmenuitem import PoisonPotion, GreaterPoisonPotion, DeadlyPoisonPotion, LethalPoisonPotion
from models.craftresourceitem import CraftResourceItem
from models.skillitem import SkillItem
from services.stock import StockService
from utility.alias import AliasUtils
from diagnostic.logger import Logger


# ***************************
# WARNING - Attended macro
# Poison damage CAN kill you.
# ***************************

def CreatePotionResource(potion, min_skill, max_skill):
    resource = CraftResourceItem(potion.graphic, potion.name, potion.hue, 1, 10)
    return SkillItem(potion, resource, min_skill, max_skill)


def Main():
    resource_container = "resource_container"
    AliasUtils.PromptContainer(resource_container)
    
    stock_service = StockService(resource_container)
    skill_items = [
        CreatePotionResource(PoisonPotion, 0, 60),
        CreatePotionResource(GreaterPoisonPotion, 60, 70),
        CreatePotionResource(DeadlyPoisonPotion, 70, 80),
        CreatePotionResource(LethalPoisonPotion, 80, 90),
    ]

    skill_name = "Poisonin"
    current_index = 0
    total_items = len(skill_items)
    skill_value = Skill(skill_name)
    skill_cap = SkillCap(skill_name)
    skill_item = skill_items[current_index]
    while 0 < skill_cap - skill_value:
        skill_value = Skill(skill_name)
        if skill_value < skill_item.max_level:
            Logger.Trace("Drinking ({})".format(skill_item.item.name))
            stock_service.Load(skill_item.resources)

            UseType(skill_item.item.graphic)
            Pause(1000)
        else:
            current_index += 1
            if current_index < total_items:
                Logger.Log("No longer gaining from item ({})".format(skill_item.item.name))
                stock_service.Unload(skill_item.resources)
                skill_item = skill_items[current_index]

# Execute Main()
Main()

# ***************************
# WARNING - Attended macro
# Poison damage CAN kill you.
# ***************************