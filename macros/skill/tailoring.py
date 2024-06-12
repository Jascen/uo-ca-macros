from Assistant import Engine

from entities.craftmenuitem import Cloak, HalfApron, HarpoonRope, Kasa, OilCloth, Robe
from models.craftresourceitem import CraftResourceItem
from models.skillitem import SkillItem
from services.craft import CraftServiceFactory, CraftingSkill
from services.salvage import Salvager
from utility.alias import AliasUtils


# Warning: This script has not been tested
Cloth          = CraftResourceItem(0x1766, "cloth", -1, 50, 300)

def ProcessItem(item_serial):
    item = Engine.Items.GetItem(item_serial)
    if not item: return

    if item.ID == HarpoonRope.graphic:
        IgnoreItem(item_serial)
    else:
        Salvager.Cut(item_serial)

def Main():
    resource_container = "resource_container"
    AliasUtils.PromptContainer(resource_container)
    service = CraftServiceFactory.Create(CraftingSkill.Tailoring, resource_container)
    
    all_items = [
        SkillItem(HarpoonRope, Cloth, 0, 35), # 40
        SkillItem(HalfApron, Cloth, 35, 42), # 45.7
        SkillItem(Cloak, Cloth, 41.4, 60), # 66.4
        SkillItem(Robe, Cloth, 53.9, 70.1), # 78.9
        SkillItem(Kasa, Cloth, 70, 74.7), # ???
        SkillItem(OilCloth, Cloth, 74.6, 99.6), # 99.6
        

        # Cloak to 50.1 (52.2)
        # Male Kimono to 54.0 (55.4)
        # Robe to 60.1 (61.0)
        # Kasa to 70.1 (70.4)
        # Ninja Tabi to 74.7
        # Oil cloth to 90.6 (94.1) (could be 99.6)
        # Cloth Ninja Hood to 91.5
        # Royal cape to 120.4
    ]
    service.Level(all_items, ProcessItem)
    Pause(1000)


# Execute Main()
Main()