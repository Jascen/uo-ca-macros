import clr
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from Assistant import Engine
from ClassicAssist.Data.Macros.Commands.AliasCommands import GetAlias
from ClassicAssist.Data.Macros.Commands.ObjectCommands import FindType
from ClassicAssist.Data.Macros.Commands.SkillCommands import Skill
from ClassicAssist.Data.Macros.Commands.ObjectCommands import FindType, UseObject
from ClassicAssist.Data.Macros.Commands.TargetCommands import WaitForTarget, Target

from craft.item import SkillItem
from craft.resource import CraftResource, CraftBoard
from items.general import GeneralItem
from items.resource import Wood, Ash, Cherry, Ebony, GoldenOak, Hickory, Mohagony, Driftwood, Oak, Pine, Rosewood, Walnut, Elven
from services.stock import StockService
from utility.alias import AliasUtils
from diagnostic.logger import Logger


Logger.DEBUG = False
Logger.TRACE = False

class UserOptions:
    LumberjackingGainsOnly = True # When `True`, only cut a wood if it can give Lumberjacking gains
    Amounts = [
        # [Amount to cut at a time, Type of wood]
        [1, Wood], # Plain logs
        [1, Ash],
        [1, Cherry],
        [1, Ebony],
        [1, GoldenOak],
        [1, Hickory],
        [1, Mohagony],
        [1, Driftwood],
        [1, Oak],
        [1, Pine],
        [1, Rosewood],
        [1, Walnut],

        # Are you really sure you want to change this?
        [1, Elven],
    ]


Log_type_id = 0x1be0
AnyBoard = GeneralItem(CraftBoard.Wood.graphic, "any board", -1)
def CreateSkillItem(resource_type, min_skill, max_skill):
    entry = UserOptions.Amounts.FirstOrDefault(lambda i: i[1] == resource_type)
    if not entry: 
        raise TypeError("Missing resource type ({})".format(resource_type))

    amount = entry[0]
    craft_resource = CraftResource(Log_type_id, resource_type.name, resource_type.hue, amount, amount)

    return SkillItem(AnyBoard, craft_resource, min_skill, max_skill)


Logs_to_chop = [
    CreateSkillItem(Wood, 0, 65.0),
    CreateSkillItem(Ash, 55, 80.0),
    CreateSkillItem(Cherry, 60, 85.0),
    CreateSkillItem(Ebony, 65, 90.0),
    CreateSkillItem(GoldenOak, 70, 95.0),
    CreateSkillItem(Hickory, 75, 100.0),
    CreateSkillItem(Mohagony, 80, 105.0),
    CreateSkillItem(Driftwood, 80, 105.0),
    CreateSkillItem(Oak, 85, 110.0),
    CreateSkillItem(Pine, 90, 115.0),
    CreateSkillItem(Rosewood, 95, 120.0),
    CreateSkillItem(Walnut, 99, 124.0),
    CreateSkillItem(Elven, 100.1, 200.1),
]


def CanStillGain(wood):
    current_skill = round(Skill("Lumberjackin"), 1)
    return wood.min_level < current_skill and current_skill < wood.max_level


def Main():
    sawmill = AliasUtils.PromptContainer("sawmill")
    
    log_container = AliasUtils.PromptContainer("log container")
    stock_service = StockService(log_container)

    for skill_item in Logs_to_chop:
        # Unload before you begin
        resource = skill_item.resources[0]
        
        Logger.Log("Processing: {}".format(resource))
        stock_service.Unload(resource)
        
        while (not UserOptions.LumberjackingGainsOnly or CanStillGain(skill_item)) and FindType(resource.graphic, -1, log_container, resource.hue):
            item = Engine.Items.GetItem(GetAlias("found"))
            if item == None: continue
            if not stock_service.Load(resource): continue
            if not FindType(resource.graphic, -1, "backpack", resource.hue): continue
            
            item = GetAlias("found")
        
            UseObject(item)
            if not WaitForTarget(2000): continue
            
            Target(sawmill)


# Execute Main()
Main()