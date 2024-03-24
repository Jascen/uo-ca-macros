from Assistant import Engine
from ClassicAssist.Data.Macros.Commands.AliasCommands import GetAlias
from ClassicAssist.Data.Macros.Commands.ObjectCommands import FindType, FindObject
from ClassicAssist.Data.Macros.Commands.SkillCommands import Skill
from ClassicAssist.Data.Macros.Commands.ObjectCommands import FindType, UseObject
from ClassicAssist.Data.Macros.Commands.TargetCommands import WaitForTarget, Target

from services.stock import StockService
from utility.alias import AliasUtils
from diagnostic.logger import Logger


class LogCutter:
    def __init__(self):
        self.sawmill = AliasUtils.PromptContainer("sawmill")
        self.stock_service = StockService("log container")


    def Cut(self, log_skill_item, amount, gains_only):
        if FindObject(self.stock_service.restock_container, -1 , "backpack"):
            Logger.Error("The log container cannot be in your backpack")
            raise Exception()

        # Set amounts to user-defined values
        resource = log_skill_item.resources[0].clone()
        resource.min_pack_amount = resource.restock_amount = amount
        
        Logger.Log("Processing: {}".format(resource))

        # Unload before you begin
        self.stock_service.Unload(resource)
        
        while (not gains_only or self.__CanStillGain(log_skill_item)) and FindType(resource.graphic, -1, self.stock_service.restock_container, resource.hue):
            item = Engine.Items.GetItem(GetAlias("found"))
            if item == None: continue
            if not self.stock_service.Load(resource): continue
            if not FindType(resource.graphic, -1, "backpack", resource.hue): continue
            
            item = GetAlias("found")
        
            UseObject(item)
            if not WaitForTarget(2000): continue
            
            Target(self.sawmill)


    def __CanStillGain(self, wood):
        current_skill = round(Skill("Lumberjackin"), 1)
        return wood.min_level < current_skill and current_skill < wood.max_level