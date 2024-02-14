from entities.craftmenuitem import BarrelHoops, BarrelTap, Gears, Lockpick, Spyglass
from entities.craftresourceitem import IngotResource
from models.skillitem import SkillItem
from services.craft import CraftServiceFactory, CraftingSkill
from utility.alias import AliasUtils


def Main():
    output_bag = "output_bag"
    resource_container = "resource_container"
    AliasUtils.PromptContainer(output_bag)
    AliasUtils.PromptContainer(resource_container)
    service = CraftServiceFactory.Create(CraftingSkill.Tinkering, resource_container)
    
    iron_ingots = [IngotResource.Iron]
    all_items = [
        SkillItem(BarrelHoops, iron_ingots, 0, 15),
        SkillItem(Gears, iron_ingots, 15, 40),
        SkillItem(BarrelTap, iron_ingots, 35, 60),
        SkillItem(Lockpick, iron_ingots, 60, 94), # 95, got to 94.8 after 5k ingots
        SkillItem(Spyglass, iron_ingots, 94, 110),
    ]
    
    service.Level(all_items, None) #lambda item: SalvageService.Move(item, output_bag))
    Pause(1000)



# Execute Main()
Main()