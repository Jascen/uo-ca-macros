from entities.craftmenuitem import *
from entities.craftresourceitem import BoardResource, IngotResource
from models.skillitem import SkillItem
from services.craft import CraftServiceFactory, CraftingSkill
from utility.alias import AliasUtils


def Main():
    resource_container = "resource_container"
    AliasUtils.PromptContainer(resource_container)
    service = CraftServiceFactory.Create(CraftingSkill.Alchemy, resource_container)
    
    all_items = []

    # Explosion Potions
    if True:
        resources = [
            service.GetResource("empty bottle", 10, 50), 
            service.GetResource("nightshade", 50, 300)
        ]
        all_items += [
            SkillItem(LesserPoisonPotion, resources, 0, 40), # 45
            SkillItem(PoisonPotion, resources, 40, 60), # 65
            SkillItem(GreaterPoisonPotion, resources, 60, 80), # 85
            SkillItem(DeadlyPoisonPotion, resources, 80, 100), # 105
            SkillItem(LethalPoisonPotion, resources, 100, 125),
        ]

    # Explosion Potions
    if True:
        resources = [
            service.GetResource("empty bottle", 10, 50), 
            service.GetResource("sulfurous ash", 50, 300)
        ]
        all_items += [
            SkillItem(LesserExplosionPotion, resources, 5, 50), # 55
            SkillItem(ExplosionPotion, resources, 50, 80), # 85
            SkillItem(GreaterExplosionPotion, resources, 80, 110), # 115
        ]

    # Ingot Transmutes
    if False:
        all_items += [
            SkillItem(TransmuteDullCopper, [IngotResource.Iron], 40, 60),
            SkillItem(TransmuteShadowIron, [IngotResource.DullCopper], 50, 70),
            SkillItem(TransmuteCopper, [IngotResource.ShadowIron], 60, 80),
            SkillItem(TransmuteBronze, [IngotResource.Copper], 70, 90),
        ]

    # Wood Transmutes
    if False:
        all_items += [
            SkillItem(TransmuteMohagony, [BoardResource.Hickory], 80, 95),
            SkillItem(TransmuteDriftwood, [BoardResource.Mohagony], 95, 110),
        ]

    service.Level(all_items)


# Execute Main()
Main()