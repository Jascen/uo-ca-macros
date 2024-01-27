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

from entities.skillitem import LumberjackSkillItem
from services.stock import StockService
from utility.alias import AliasUtils
from diagnostic.logger import Logger


Logger.DEBUG = False
Logger.TRACE = False

class UserOptions:
    LumberjackingGainsOnly = True # When `True`, only cut a wood if it can give Lumberjacking gains
    LogsToChop = [
        # [Amount to cut at a time, Type of wood]
        [1, LumberjackSkillItem.Wood], # Plain logs
        [1, LumberjackSkillItem.Ash],
        [1, LumberjackSkillItem.Cherry],
        [1, LumberjackSkillItem.Ebony],
        [1, LumberjackSkillItem.GoldenOak],
        [1, LumberjackSkillItem.Hickory],
        [1, LumberjackSkillItem.Mohagony],
        [1, LumberjackSkillItem.Driftwood],
        [1, LumberjackSkillItem.Oak],
        [1, LumberjackSkillItem.Pine],
        [1, LumberjackSkillItem.Rosewood],
        [1, LumberjackSkillItem.Walnut],

        # Are you really sure you want to change this?
        [1, LumberjackSkillItem.Elven],
    ]


def CanStillGain(wood):
    current_skill = round(Skill("Lumberjackin"), 1)
    return wood.min_level < current_skill and current_skill < wood.max_level


def Main():
    sawmill = AliasUtils.PromptContainer("sawmill")
    
    log_container = AliasUtils.PromptContainer("log container")
    stock_service = StockService(log_container)

    for original in UserOptions.LogsToChop:
        # Set amounts to user-defined values
        amount = original[0]
        skill_item = original[1]
        resource = skill_item.resources[0].clone()
        resource.min_pack_amount = resource.restock_amount = amount
        
        Logger.Log("Processing: {}".format(resource))

        # Unload before you begin
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