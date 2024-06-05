from entities.craftmenuitem import BarkFragment, BarrelLid, BarrelStaves, Bokuto, Fukiya, Tetsubo, WoodenChair
from entities.craftresourceitem import BoardResource
from models.skillitem import SkillItem
from services.craft import CraftServiceFactory, CraftingSkill
from utility.alias import AliasUtils
from utility.item import ItemUtils
from utility.skill import SkillUtils


output_bag = AliasUtils.PromptContainer("output_bag")
resource_container = AliasUtils.PromptContainer("resource_container")

def LoreThenMove(item_serial):
    SkillUtils.ArmsLore(item_serial, True)
    ItemUtils.Move(item_serial, output_bag)


def Main():
    service = CraftServiceFactory.Create(CraftingSkill.Carpentry, resource_container)

    wood_boards = [BoardResource.Wood]
    
    all_items = [
        SkillItem(BarrelStaves, wood_boards, 0, 20),
        SkillItem(BarrelLid, wood_boards, 11, 25), # 36
        SkillItem(WoodenChair, wood_boards, 21, 40), # 46
        #SkillItem(MediumCrate, wood_boards, 31, 40), # 56 -- Logs only??
        SkillItem(BarkFragment, wood_boards, 40, 70), # 67.6
        SkillItem(Fukiya, wood_boards, 60, 82), # 85
        SkillItem(Bokuto, wood_boards, 82, 90), # 95
        SkillItem(Tetsubo, wood_boards, 90, 140.3), # 140 # ... 90.5 to 91.0, Gnarled Staves for 300 wood
    ]
    
    service.Level(all_items, LoreThenMove)
    Pause(1000)


# Execute Main()
Main()