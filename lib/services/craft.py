from ClassicAssist.Data.Macros.Commands.MainCommands import Pause, SysMessage
from ClassicAssist.Data.Macros.Commands.GumpCommands import ReplyGump, WaitForGump, GumpExists
from ClassicAssist.Data.Macros.Commands.AliasCommands import GetAlias
from ClassicAssist.Data.Macros.Commands.ObjectCommands import FindType, CountType, UseType
from ClassicAssist.Data.Macros.Commands.SkillCommands import Skill, SkillCap

from entities.craftresourceitem import IngotResource
from entities.craftmenuitem import MortarAndPestle, Tongs, Hammer, FletchingTool, SewingKit, TinkerTool, ScribesPen, MapmakersPen, Skillet
from services.stock import StockService
from diagnostic.logger import Logger


class CraftingSkill:
    Alchemy = 1
    Blacksmith = 2
    Carpentry = 3
    # CarpentryFurniture = 4
    Cartography = 5
    Cooking = 6
    Fletching = 7
    # Glassblowing = 8
    Inscription = 9
    # Masonry = 10
    Tailoring = 11
    Tinkering = 12


class CraftServiceFactory:
    @classmethod
    def Create(self, skill, restock_container = None):
        stock_service = None
        if restock_container != None: stock_service = StockService(restock_container)

        tool = None
        
        if skill == CraftingSkill.Alchemy: tool = MortarAndPestle
        elif skill == CraftingSkill.Blacksmith: tool = Tongs
        elif skill == CraftingSkill.Carpentry: tool = Hammer
        elif skill == CraftingSkill.Cartography: tool = MapmakersPen
        elif skill == CraftingSkill.Cooking: tool = Skillet
        elif skill == CraftingSkill.Fletching: tool = FletchingTool
        elif skill == CraftingSkill.Inscription: tool = ScribesPen
        elif skill == CraftingSkill.Tailoring: tool = SewingKit
        elif skill == CraftingSkill.Tinkering: tool = TinkerTool
        
        if tool == None: raise Exception("Invalid Skill ({}) specified.".format(skill))

        return CraftService(CraftServiceBase(skill, tool, stock_service))


class CraftService:
    def __init__(self, craft_service_base):
        self.service = craft_service_base


    def CraftItem(self, item, resources):
        return self.service.CraftItem(item, resources)


    def Level(self, all_items, after_created_fn = None):
        filtered_items = self.__RemoveTrivialItems(all_items)
        if len(filtered_items) < 1:
            Logger.Log("No craftable items")
            return

        self.service.Level(filtered_items, after_created_fn)


    def __RemoveTrivialItems(self, all_items):
        skill_value = Skill(self.service.skill_name)
        skill_items = []

        # Trim the unnecessary items
        for skill_item in all_items:
            if skill_value <= skill_item.max_level:
                skill_items.append(skill_item)

        # Sort
        skill_items.sort(key=lambda item: item.min_level)

        return skill_items


class CraftServiceBase:
    def __init__(self, skill, crafting_tool, stock_service):
        self.skill = skill
        self.skill_name = self.__GetSkillName(skill)
        self.crafting_tool = crafting_tool
        self.stock_service = stock_service
        self.crafting_gump_id = 0x38920abd # TODO: Same for everyone??
        self.gump_timeout = 5000
        self.short_pause = 500
        # Always use Iron Ingots for crafting Tools using Tinkering
        iron_ingot = IngotResource.Iron.clone()
        iron_ingot.min_pack_amount = 10
        iron_ingot.restock_amount = 50
        self.iron_ingot = iron_ingot


    def Level(self, skill_items, after_created_fn = None):
        Logger.Debug("In CraftServiceBase.Level")

        total_items = len(skill_items)
        current_index = 0
        skill_value = Skill(self.skill_name)
        skill_cap = SkillCap(self.skill_name)
        skill_item = skill_items[current_index]
        while 0 < skill_cap - skill_value:
            skill_value = Skill(self.skill_name)
            if skill_value < skill_item.max_level:
                Logger.Trace("Crating item ({})".format(skill_item.item.name))
                if self.CraftItem(skill_item.item, skill_item.resources): 
                    if after_created_fn:
                        if not self.EnsureTool():
                            Logger.Error("Failed to create Tool. Stopping!") 
                            return False

                        while FindType(skill_item.item.graphic, -1, "backpack"):
                            Logger.Trace("Found item. Executing post-creation callback.")
                            after_created_fn(GetAlias("found"))
                Pause(self.short_pause)
            else:
                current_index += 1
                if current_index < total_items:
                    Logger.Log("No longer gaining from item ({})".format(skill_item.item.name))
                    self.stock_service.Unload(skill_item.resources)
                    skill_item = skill_items[current_index]
                    continue


    def EnsureTool(self):
        Logger.Debug("In CraftServiceBase.EnsureTool")

        if self.skill == CraftingSkill.Tinkering:
            Logger.Trace("Crafting Tinker Tools...")
            if not self.MakeTinkerTools(): return False
        else:
            while not FindType(self.crafting_tool.graphic, -1, "backpack", self.crafting_tool.hue):
                Logger.Trace("Crafting tool ({})".format(self.crafting_tool.name))
                if not self.MakeTinkerTools():
                    Logger.Error("Failed to craft Tinker Tool")
                    return False

                if not self.__Craft(TinkerTool, self.crafting_tool, self.iron_ingot):
                    Logger.Error("Failed to craft Tool")
                    return False

        # Reopen after crafting a new one
        Pause(self.short_pause)
        UseType(self.crafting_tool.graphic, self.crafting_tool.hue)
        if not WaitForGump(self.crafting_gump_id, self.gump_timeout): return False

        return True


    def CraftItem(self, item, resources, set_material = False):
        Logger.Debug("In CraftServiceBase.CraftItem")

        # TODO: Add ability to set the material
        if not self.EnsureTool(): return False

        return self.__Craft(self.crafting_tool, item, resources)


    def MakeTinkerTools(self):
        Logger.Debug("In CraftServiceBase.MakeTinkerTools")

        if not FindType(TinkerTool.graphic, -1, "backpack", TinkerTool.hue): return False # Very bad
        
        if GumpExists(self.crafting_gump_id): ReplyGump(self.crafting_gump_id, 0)  # Close gump
        
        # Always keep at least three
        while CountType(TinkerTool.graphic, "backpack", TinkerTool.hue) < 3:
            SysMessage("Making Tinker Tools...")
            self.__Craft(TinkerTool, TinkerTool, self.iron_ingot)

        return True


    def __Craft(self, tool, item, resources):
        Logger.Debug("In CraftServiceBase.__Craft")

        if self.stock_service != None and not self.stock_service.Load(resources): return False

        Logger.Log("Crafting item ({})...".format(item.name))
        # Make sure correct gump is open
        UseType(tool.graphic, tool.hue)
        if not WaitForGump(self.crafting_gump_id, self.gump_timeout): return False

        # Craft item
        ReplyGump(self.crafting_gump_id, item.button_one)
        WaitForGump(self.crafting_gump_id, self.gump_timeout)
        ReplyGump(self.crafting_gump_id, item.button_two)
        WaitForGump(self.crafting_gump_id, self.gump_timeout)

        Pause(self.short_pause)

        return True


    def __GetSkillName(self, skill):
        if skill == CraftingSkill.Alchemy: return "Alchem"
        if skill == CraftingSkill.Blacksmith: return "Blacksmithin"
        if skill == CraftingSkill.Carpentry: return "Carpentr"
        if skill == CraftingSkill.Cartography: return "Cartograph"
        if skill == CraftingSkill.Cooking: return "Cookin"
        if skill == CraftingSkill.Fletching: return "Fletchin"
        if skill == CraftingSkill.Inscription: return "Inscriptio"
        if skill == CraftingSkill.Tailoring: return "Tailorin"
        if skill == CraftingSkill.Tinkering: return "Tinkerin"

        return None