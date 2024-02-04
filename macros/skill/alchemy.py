from entities.craftmenuitem import *
from models.skillitem import SkillItem
from services.craft import CraftServiceFactory, CraftingSkill
from utility.alias import AliasUtils


def Main():
    resource_container = "resource_container"
    AliasUtils.PromptContainer(resource_container)
    service = CraftServiceFactory.Create(CraftingSkill.Alchemy, resource_container)
    
    empty_bottle = service.GetResource("empty bottle", 10, 50)
    
    all_items = []

    # Using Nightshade
    if True:
        resources = [
            empty_bottle, 
            service.GetResource("nightshade", 50, 300)
        ]
        all_items += [
            SkillItem(LesserPoisonPotion, resources, 0, 40), # 45
            SkillItem(PoisonPotion, resources, 40, 60), # 65
            SkillItem(GreaterPoisonPotion, resources, 60, 80), # 85
            SkillItem(DeadlyPoisonPotion, resources, 80, 100), # 105
            SkillItem(LethalPoisonPotion, resources, 100, 125),
        ]

    # Using Sulfurous Ash
    if True:
        resources = [
            empty_bottle, 
            service.GetResource("sulfurous ash", 50, 300)
        ]
        all_items += [
            SkillItem(LesserExplosionPotion, resources, 5, 50), # 55
            SkillItem(ExplosionPotion, resources, 50, 80), # 85
            SkillItem(GreaterExplosionPotion, resources, 80, 110), # 115
        ]

    service.Level(all_items)


# Execute Main()
Main()