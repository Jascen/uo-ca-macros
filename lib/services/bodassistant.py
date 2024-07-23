from services.bodfactory import BODFactory
from diagnostic.logger import Logger
from services.stock import StockService
from utility.alias import AliasUtils
from utility.interaction import InteractionUtils
from models.craftresourceitem import CraftResourceItem
from utility.item import ItemUtils

from Assistant import Engine
from ClassicAssist.Data.Macros.Commands.TargetCommands import CancelTarget
from ClassicAssist.Data.Macros.Commands.ObjectCommands import FindType


class BodAssistant:    
    def Run(self):
        config = BodAssistantConfig()
        alias = "restock_container"
        self.__ResolveResourceContainer(alias)
        stock_service = StockService(alias)
        resources_by_key = {}

        # Add user-defined resources
        for resource in config.resources:
            resources_by_key[resource.name] = resource

        ClearIgnoreList()
        bod_item_serials = ItemUtils.GetAll(config.bod_type_id, -1, -1, "backpack")
        bod_serials_by_resource_by_item = self.__GroupBodsByResourceByItems(bod_item_serials) # { [resource]: { [item]: serial[] } }
        
        ClearIgnoreList()
        for serial in bod_item_serials:
            source_bod = self.__TryCreateBod(serial)
            if source_bod == None: continue
            if source_bod.IsComplete(): continue

            Logger.Error("I have so much work to do for this BOD...")
            print(source_bod)
            
            # Resolve Resources
            primary_resource = source_bod.require_resource
            if not resources_by_key.get(primary_resource):
                resources_by_key[primary_resource] = self.__ResolveResource(primary_resource)

            resources = [
                resources_by_key[primary_resource]
            ]
        
            while not source_bod.IsComplete():
                for item_name in source_bod.items_counts_by_name.keys():
                    # Ensure the item needs to be crafted before we prompt the User
                    if source_bod.GetRemainingAmount(item_name) <= 0: continue
                    
                    CancelTarget() # Clear the cursor
                    stock_service.Load(resources) # Try to pre-emptively load to assist in crafting

                    suggested_graphic = None
                    if config.graphic_id_map.get(item_name): suggested_graphic = config.graphic_id_map[item_name]
                    
                    first_resource = resources[0] # Assume this is the most important one to show the User
                    graphic_to_target = self.__ResolveItemNameAsGraphic(first_resource, item_name, suggested_graphic)
                    HeadMsg("Targeting ({}) for '{}'.".format(hex(graphic_to_target), item_name), "self", 31)

                    for bod_serial in bod_serials_by_resource_by_item[first_resource.name][item_name]:
                        bod_to_fill = Engine.Items.GetItem(bod_serial)

                        while not Dead():
                            if not stock_service.Load(resources):
                                Pause(1000)
                                continue

                            if self.__TryCraftAndFillItem(item_name, graphic_to_target, bod_to_fill, resources, stock_service, config): break
                            
                            Pause(1000) # Prevent CPU spinning
            
                # TODO: Optimize this. The item is refreshed but we're brute-force rebuilding the BOD to "refresh" it
                source_item = Engine.Items.GetItem(serial)
                source_bod = BODFactory.Create(source_item) # Get the very latest

            Logger.Log("Finished processing BOD.")
            config.AfterBODCompleted(Engine.Items.GetItem(serial))
            # stock_service.Unload(resources) # TODO: Potentially unload resources


    def __TryCreateBod(self, serial):
        source_item = Engine.Items.GetItem(serial)
        if source_item == None: return None # No longer exists

        source_bod = BODFactory.Create(source_item) # Refresh to latest state
        if source_bod == None: return None # Failed to create

        return source_bod

            
    def __TryCraftAndFillItem(self, item_to_craft, graphic_to_target, bod_item, resources, stock_service, config):
            bod = BODFactory.Create(bod_item)
            if bod == None: return False # Failed to create

            bod_gump_id = config.bod_large_gump_id if bod.is_large else config.bod_small_gump_id
            while 0 < bod.GetRemainingAmount(item_to_craft):
                # Open BOD Gump if necessary
                if not GumpExists(bod_gump_id):
                    UseObject(bod_item.Serial)
                    Pause(1000)

                    if not GumpExists(bod_gump_id) and not WaitForGump(bod_gump_id, 5000):
                        Logger.Error("Failed to detect BOD gump.")
                        continue

                CancelTarget()
                if not TargetExists():
                    ReplyGump(bod_gump_id, 2) # Press Combine
                    WaitForTarget(1000)
                    if not TargetExists():
                        Logger.Error("Failed to select Combine.")
                        continue

                ClearIgnoreList()
                while FindType(graphic_to_target, -1, "backpack"):
                    candidate = Engine.Items.GetItem(GetAlias("found"))
                    if not config.ShouldCombineItem(candidate, bod, resources[0]): 
                        IgnoreObject(candidate.Serial)
                        continue

                    # TODO: Can we do something about guaranteeing it's selected?
                    IgnoreObject(candidate.Serial)
                    Target(candidate.Serial)
                    if not WaitForTarget(3000): break

                    Pause(250)

                # Close
                CancelTarget()
                if GumpExists(bod_gump_id):
                    ReplyGump(bod_gump_id, 0) # Close

                # TODO: Optimize this. The item is refreshed but we're brute-force rebuilding the BOD to "refresh" it
                bod = BODFactory.Create(bod_item) # Get the very latest

                for i in range(min(5, bod.GetRemainingAmount(item_to_craft))): # Never exceed more than 5 at a time due to weight constraints
                    # Scan backpack and auto-select
                    while War("self"):
                        Logger.Log("War mode detected. Pausing execution...")
                        Pause(2500)

                    if not stock_service.Load(resources):
                        Logger.Error("Failed to restock resources")
                        Pause(1000) # Throttle to reduce spamming
                        continue # Comment this out if you want to use the remaining resources in your backpack

                    if not config.BeforeItemCrafted(resources):
                        Logger.Error("Failed item crafting prerequisite")
                        continue

                    config.CraftItem(item_to_craft)
            
            return True


    def __FindItemByName(self, name, container):
        name = name.lower()
        for item in container:
            if name in item.Name.lower(): return item

        return None


    def __GroupBodsByResourceByItems(self, bod_serials):
        bod_serials_by_resource_by_item = {} # { [resource]: { [item]: serial[] } }

        for serial in bod_serials:
            item = Engine.Items.GetItem(serial)
            bod = BODFactory.Create(item)
            if bod == None: continue # Failed to create

            primary_resource = bod.require_resource if bod.require_resource else "Default"
            if not bod_serials_by_resource_by_item.get(primary_resource):
                bod_serials_by_resource_by_item[primary_resource] = {}


            for item_name in bod.items_counts_by_name.keys(): # items()
                if not bod_serials_by_resource_by_item[primary_resource].get(item_name):
                    bod_serials_by_resource_by_item[primary_resource][item_name] = []

                bod_serials_by_resource_by_item[primary_resource][item_name].append(serial)
        
        return bod_serials_by_resource_by_item


    def __ResolveItemNameAsGraphic(self, resource_name, item_name, suggested_graphic = None):
        targeted = None
        backpack = Engine.Items.GetItem(GetAlias("backpack"))
        if backpack.Container == None:
            WaitForContents(backpack.Container, 5000)

        # Ensure Make Last is set
        InteractionUtils.Prompt(
            "<center>The Item</center>",
            "Press any button once you select your <basefont color=blue>Resource</basefont> and set your <basefont size=10>Make Last</basefont> to:",
            "<basefont size=10>'{}'</basefont>".format(resource_name)
            + "<br>"
            + "<basefont size=10>'{}'</basefont>".format(item_name)
        )

        item_name = item_name.upper()

        # Search for the item
        confirmed = False
        targeted = None
        if suggested_graphic: # Take user input as priority
            if FindType(suggested_graphic, 0, "backpack"):
                targeted = Engine.Items.GetItem(GetAlias("found"))
        else:
            targeted = self.__FindItemByName(item_name, backpack.Container)

        if targeted:
            # Prompt User for affirmation
            confirmed = InteractionUtils.Prompt(
                "<center>The Item</center>",
                "The system found an item. Press OKAY to confirm it matches:"
                + "<br>"
                + "<basefont size=10>{}</basefont>".format(item_name),
                targeted.Name
            )
        else:
            InteractionUtils.Prompt(
                "<center>The Item</center>",
                "Please target <basefont size=10>'{}'</basefont>".format(item_name),
                "Press any button to continue."
            )

        alias = "$item_type__{}".format(item_name)
        if not confirmed:
            target_serial = None
            while True:
                if not confirmed: target_serial = PromptMacroAlias(alias)
                else: target_serial = None
                if targeted and not target_serial: break
                if not target_serial: continue

                targeted = Engine.Items.GetItem(target_serial)
                confirmed = InteractionUtils.Prompt(
                    "<center>The Item</center>",
                    "Press OKAY to confirm it matches <basefont size=10>{}</basefont>".format(item_name),
                    "{}".format(targeted.Name.upper())
                )
                if not confirmed: targeted = None

        UnsetAlias(alias)
        return targeted.ID


    def __ResolveResource(self, resource_key):
        CancelTarget() # Clear the cursor
        InteractionUtils.Prompt(
            "<center>The Resource</center>",
            "Please target <basefont size=10>{}</basefont>".format(resource_key),
            "Press any button to continue."
        )

        targeted = None
        confirmed = False
        alias = "$resource_type__{}".format(resource_key)
        while True:
            if not confirmed: target_serial = PromptMacroAlias(alias)
            else: target_serial = None
            if targeted and not target_serial:
                UnsetAlias(alias)
                return CraftResourceItem(targeted.ID, resource_key, targeted.Hue, 50, 300)
            if not target_serial: continue

            targeted = Engine.Items.GetItem(target_serial)
            description = [ targeted.Name ]
            for property in targeted.Properties:
                if targeted.Name == property.Text: continue
                description.append(property.Text)

            confirmed = InteractionUtils.Prompt(
                "<center>The Resource</center>",
                "Press OKAY to confirm this is <basefont size=10>{}</basefont>".format(resource_key),
                "{}".format("<br>".join(description))
            )
            if not confirmed: targeted = None


    def __ResolveResourceContainer(self, alias):
        CancelTarget() # Clear the cursor
        character_alias = AliasUtils.CreateCharacterAlias(alias)
        
        if FindAlias(character_alias):
            container = Engine.Items.GetItem(GetAlias(character_alias))
            if container != None:
                # Prompt User for affirmation
                confirmed = InteractionUtils.Prompt(
                    "<center>Resource Container</center>",
                    "The system found your resource container. Press OKAY to confirm it matches:",
                    "<basefont size=10>{}</basefont>".format(container.Name)
                )
                if confirmed: return

        targeted = None
        confirmed = False
        alias = "$resource_container"
        while True:
            if not confirmed: target_serial = PromptMacroAlias(alias)
            else: target_serial = None
            if targeted and not target_serial:
                SetMacroAlias(character_alias, targeted.Serial)
                UnsetAlias(alias)
                return
            if not target_serial: continue

            targeted = Engine.Items.GetItem(target_serial)
            description = [ targeted.Name ]
            for property in targeted.Properties:
                if targeted.Name == property.Text: continue
                description.append(property.Text)

            confirmed = InteractionUtils.Prompt(
                "<center>Resource Container</center>",
                "Press OKAY to confirm this is your <basefont size=10>Resource Container</basefont>",
                "{}".format("<br>".join(description))
            )
            if not confirmed: targeted = None


def CreateIngot(name, hue):
    return CraftResourceItem(0x1bf2, name, hue, 50, 300)


def CreateLeather(name, hue):
    return CraftResourceItem(0x1081, name, hue, 50, 300)


def CreateBoard(name, hue):
    return CraftResourceItem(0x1bd7, name, hue, 50, 300)


class BodAssistantConfig:
    bod_large_gump_id = 0xa125b54a
    bod_small_gump_id = 0x5afbd742
    bod_type_id = 0x2258
    crafting_gump_id = 0x38920abd
    resources = [ # Fill this out to help for automagic resource selection
        CreateIngot("dull copper ingots", 2741),
        CreateIngot("shadow ingots",      2739),
        CreateIngot("copper ingots",      2840),
        CreateIngot("bronze ingots",      2236),
        CreateIngot("golden ingots",      2458),
        CreateIngot("agapite ingots",     2794),
        CreateIngot("verite ingots",      2141),
        CreateIngot("valorite ingots",    2397),
        CreateIngot("nepturite ingots",   2376),
        CreateIngot("obsidian ingots",    1986),
        CreateIngot("steel ingots",       2463),
        CreateIngot("brass ingots",       2451),
        CreateIngot("mithril ingots",     2928),
        CreateIngot("xormite ingots",     1991),
        CreateIngot("dwarven ingots",     1788),

        CreateBoard("ash wood",           1191),
        CreateBoard("cherry wood",        1863),
        CreateBoard("ebony wood",         2412),
        CreateBoard("golden oak wood",    2010),
        CreateBoard("hickory wood",       1045),
        CreateBoard("mahogany wood",      2312),
        CreateBoard("driftwood",          2419),
        CreateBoard("oak wood",           1810),
        CreateBoard("pine wood",          461),
        CreateBoard("ghost wood",         2498),
        CreateBoard("rosewood",           2115),
        CreateBoard("walnut wood",        1872),
        CreateBoard("petrified wood",     2708),
        CreateBoard("elven wood",         2618),

        CreateLeather("lizard leather",   2736),
        CreateLeather("serpent leather",  2841),
        CreateLeather("necrotic leather", 1968),
        CreateLeather("volcanic leather", 2873),
        CreateLeather("frozen leather",   2907),
        CreateLeather("deep sea leather", 2747),
        CreateLeather("goliath leather",  2154),
        CreateLeather("draconic leather", 2740),
        CreateLeather("hellish leather",  2810),
        CreateLeather("dinosaur leather", 2333),
        CreateLeather("alien leather",    2300),
    ]
    graphic_id_map = { # Only when searching by name doesn't work or has false positives
        # Blacksmithing
        "chainmail coif": 0x13BB,
        "chainmail tunic": 0x13BF,
        "chainmail leggings": 0x13BE,

        "ringmail sleeves": 0x13EE,
        "ringmail leggings": 0x13F0,
        "ringmail tunic": 0x13EC,

        # Carpentry

        # Fletching
        "crossbow": 0xF50,
        "bow": 0x13B2,

        # Tailoring
        "studded legs": 0x13DA,
        "studded tunic": 0x13DB,
        "studded sleeves": 0x13DC,
        "female leather armor": 0x1C06,
        "studded armor": 0x1C02,
    }


    def __EnsureElixir(self, resources):
        if not UserOptions.Require_Elixir: return True

        skill = None
        for r in resources:
            if "wood" in r.name: skill = "Fletchin" # Assumes Fletching only right now
            # if ("wood" in r.name): skill = "Carpentr" # TODO: Carpentry
            elif ("ingot" in r.name ): skill = "Blacksmithin" # Tongs
            elif ("leather" in r.name): skill = "Tailorin" # Sewing Kits
            if skill: break

        if skill:
            if 125 <= round(Skill(skill), 1): return True

            success = False
            if skill == "Fletchin": success = FindType(0x1fd9, 0, "backpack", 105)
            # elif skill == "Carpentr": success = FindType(0x1fd9, 0, "backpack", 1150)
            # elif skill == "Blacksmithin": success = FindType(0x1fd9, 0, "backpack", )
            # elif skill == "Tailorin": success = FindType(0x1fd9, 0, "backpack", )

            if success:
                UseObject("found")
                Pause(1000)
            if 125 <= round(Skill(skill), 1): return True

        InteractionUtils.Prompt(
            "<center>Elixir</center>",
            "Failed to apply Elixir.",
            "Press any button to continue."
        )

        return False


    def __EnsureTool(self, resources):
        if not UserOptions.Auto_Use_New_Tool: return GumpExists(self.crafting_gump_id)

        # Try to automagically open the gump
        tool = None
        for r in resources:
            if "wood" in r.name: tool = 0x1f2c # Assumes Fletching only right now
            # if ("wood" in r.name): tool = 0x0 # TODO: Carpentry
            elif ("ingot" in r.name ): tool = 0xfbb # Tongs
            elif ("leather" in r.name): tool = 0x4c81 # Sewing Kits
            if tool: break

        if tool and FindType(tool, 0, "backpack", -1):
            if GumpExists(self.crafting_gump_id): return True

            UseObject("found")
            Pause(1000)

            if GumpExists(self.crafting_gump_id) or WaitForGump(self.crafting_gump_id, 5000): return True
        
        return False


    def AfterBODCompleted(self, bod_item):
        # Optimization: Maybe you want to move the BOD to another bag or a BOD book
        return


    def BeforeItemCrafted(self, resources):
        # If less than 50 stones are free, stop crafting
        if DiffWeight() < 50:
            InteractionUtils.Prompt(
                "<center>Weight failure</center>",
                "The weight check has failed.",
                "Press any button to continue."
            )
            return False # Skip the crafting attempt

        # Check if the crafting gump is open
        if not GumpExists(self.crafting_gump_id):
            if self.__EnsureTool(resources): return True

            confirmed = InteractionUtils.Prompt(
                "<center>Crafting Gump</center>",
                "Failed to find Crafting Gump.",
                "Press OKAY button when it is open."
            )

            # Optimization: Maybe you want to re-open the crafting gump
            # Optimization: Maybe you want to craft tools
            return confirmed

        if not self.__EnsureElixir(resources): return False
        
        return True


    def CraftItem(self, item_name):
        # Optimization: Maybe you want to take `item_name` and map it directly to a item id instead of simply `make last`
        ReplyGump(self.crafting_gump_id, 21) # Make last
        WaitForGump(self.crafting_gump_id, 5000)


    def ShouldCombineItem(self, item_of_crafted_type, bod, primary_resource):
        if 0 <= primary_resource.hue and item_of_crafted_type.Hue != primary_resource.hue: return False
        if not bod.require_exceptional: return True

        for property in item_of_crafted_type.Properties:
            if "exceptional" in property.Text.lower(): return True
        
        # Optimization: The BOD requires Exceptional but the item isn't Exceptional
        
        return False


class UserOptions:
    Require_Elixir = False # If True, stop executing when no Elixirs are found
    Auto_Use_New_Tool = False # If the crafting gump is not detected, try to open it.