from entities.craftmenuitem import Bow, Crossbow, HeavyCrossbow, RepeatingBow, Shaft, WoodlandShortbow
from entities.craftresourceitem import BoardResource
from models.skillitem import SkillItem
from services.craft import CraftServiceFactory, CraftingSkill
from utility.alias import AliasUtils
from utility.item import ItemUtils
from utility.skill import SkillUtils


output_bag = AliasUtils.PromptContainer("output_bag")

def LoreThenMove(item_serial):
    SkillUtils.ArmsLore(item_serial, True)        
    ItemUtils.Move(item_serial, output_bag)


def Main():
    resource_container = "resource_container"
    AliasUtils.PromptContainer(resource_container)
    service = CraftServiceFactory.Create(CraftingSkill.Fletching, resource_container)
    
    wood_boards = [BoardResource.Wood]
    service.Level([
        SkillItem(Shaft, wood_boards, 0, 40),
    ], lambda item: IgnoreObject(item))

    all_items = [
        SkillItem(Bow, wood_boards, 30, 50), # 70
        SkillItem(WoodlandShortbow, wood_boards, 50, 60), # 80
        SkillItem(Crossbow, wood_boards, 60, 80), # 100
        SkillItem(HeavyCrossbow, wood_boards, 80, 90), # 120
        SkillItem(RepeatingBow, wood_boards, 90, 130),
    ]
    service.Level(all_items, LoreThenMove)
    Pause(1000)


# Execute Main()
Main()