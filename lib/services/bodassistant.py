from services.bodfactory import BODFactory
from diagnostic.logger import Logger
from services.stock import StockService
from utility.alias import AliasUtils
from utility.interaction import InteractionUtils
from models.craftresourceitem import CraftResourceItem

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
        while FindType(config.bod_type_id, -1, "backpack"):     
            item = Engine.Items.GetItem(GetAlias("found"))
            bod = BODFactory.Create(item)
            if bod == None: continue # Failed to create

            while not bod.IsComplete():
                Logger.Error("I have so much work to do for this BOD...")
                print(bod)

                # Resolve Resources
                primary_resource = bod.require_resource if bod.require_resource else "Default"
                if not resources_by_key.get(primary_resource):
                    resources_by_key[primary_resource] = self.__ResolveResource(primary_resource)

                resources = [
                    resources_by_key[primary_resource]
                ]

                if not stock_service.Load(resources):
                    Pause(1000)
                    continue

                last_item_to_craft = None
                graphic_to_target = None
                while not Dead():
                    item_to_craft = bod.GetIncompleteItem()
                    if not item_to_craft: break # No work to do

                    if item_to_craft != last_item_to_craft:
                        CancelTarget() # Clear the cursor
                        stock_service.Load(resources) # Try to pre-emptively load to assist in crafting

                        suggested_graphic = None
                        if config.graphic_id_map.get(item_to_craft): suggested_graphic = config.graphic_id_map[item_to_craft]
                        graphic_to_target = self.__ResolveItemNameAsGraphic(primary_resource, item_to_craft, suggested_graphic)
                        HeadMsg("Targeting ({}) for '{}'.".format(hex(graphic_to_target), item_to_craft), "self", 31)
                        last_item_to_craft = item_to_craft

                    # Open BOD Gump if necessary
                    if not GumpExists(config.bod_gump_id):
                        UseObject(item.Serial)
                        Pause(1000)

                        if not GumpExists(config.bod_gump_id) and not WaitForGump(config.bod_gump_id, 5000):
                            Logger.Error("Failed to detect BOD gump.")
                            continue

                    CancelTarget()
                    if not TargetExists():
                        ReplyGump(config.bod_gump_id, 2) # Press Combine
                        WaitForTarget(1000)
                        if not TargetExists():
                            Logger.Error("Failed to select Combine.")
                            continue

                    ClearIgnoreList()
                    while FindType(graphic_to_target, -1, "backpack"):
                        candidate = Engine.Items.GetItem(GetAlias("found"))
                        if not config.AfterItemCrafted(candidate, bod, resources[0]): 
                            IgnoreObject(candidate.Serial)
                            continue

                        # TODO: Can we do something about guaranteeing it's selected?
                        IgnoreObject(candidate.Serial)
                        Target(candidate.Serial)
                        if not WaitForTarget(3000): break

                        Pause(250)

                    # Close
                    CancelTarget()
                    if GumpExists(config.bod_gump_id):
                        ReplyGump(config.bod_gump_id, 0) # Close

                    # TODO: Optimize this. The item is refreshed but we're brute-force rebuilding the BOD to "refresh" it
                    bod = BODFactory.Create(item) # Get the very latest

                    for i in range(min(5, bod.GetRemainingAmount(item_to_craft))): # Never exceed more than 5 at a time due to weight constraints
                        # Scan backpack and auto-select
                        while War("self"):
                            Logger.Log("War mode detected. Pausing execution...")
                            Pause(2500)

                        if not stock_service.Load(resources):
                            Logger.Error("Failed to restock resources")
                            Pause(1000) # Throttle to reduce spamming
                            continue # Comment this out if you want to use the remaining resources in your backpack

                        if not config.CraftItem(item_to_craft):
                            Logger.Error("Failed to craft item. Enabling war mode")
                            WarMode("on")
                            continue
            
            Logger.Log("Finished processing BOD.")
            config.AfterBODCompleted(item)
            IgnoreObject(item.Serial)
            Pause(1000) # Prevent CPU spinning


    def __FindItemByName(self, name, container):
        name = name.lower()
        for item in container:
            if name in item.Name.lower(): return item

        return None


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
        resource_key = resource_key.upper()
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
                return CraftResourceItem(targeted.ID, targeted.Name, targeted.Hue, 50, 300)
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
            container = Engine.Items.GetItem(GetAlias(alias))
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
    bod_gump_id = 0xa125b54a
    bod_type_id = 0x2258
    crafting_gump_id = 0x38920abd
    resources = [ # Fill this out to help for automagic resource selection
        CreateIngot("verite ingots",      2141),
    ]
    graphic_id_map = { # Only when searching by name doesn't work or has false positives
        # Blacksmithing
        'chainmail coif': 0x13BB,
        'chainmail tunic': 0x13BF,
        'chainmail leggings': 0x13BE,

        'ringmail sleeves': 0x13EE,
        'ringmail leggings': 0x13F0,
        'ringmail tunic': 0x13EC,

        # Fletching
        'crossbow': 0xF50,
        'bow': 0x13B2,
    }


    def AfterBODCompleted(self, bod_item):
        # Optimization: Maybe you want to move the BOD to another bag or a BOD book
        return


    def CraftItem(self, item_name):
        if not GumpExists(self.crafting_gump_id):
            confirmed = InteractionUtils.Prompt(
                "<center>Crafting Gump</center>",
                "Failed to find Crafting Gump.",
                "Press OKAY button when it is open."
            )
            # Optimization: Maybe you want to re-open the crafting gump
            # Optimization: Maybe you want to craft tools
            return confirmed

        # Optimization: Maybe you want to take `item_name` and map it directly to a item id instead of simply `make last`
        ReplyGump(self.crafting_gump_id, 21) # Make last
        WaitForGump(self.crafting_gump_id, 5000)

        return True


    def AfterItemCrafted(self, item_of_crafted_type, bod, primary_resource):
        if 0 <= primary_resource.hue and item_of_crafted_type.Hue != primary_resource.hue: return False
        if not bod.require_exceptional: return True

        for property in item_of_crafted_type.Properties:
            if "exceptional" in property.Text.lower(): return True
        
        return False