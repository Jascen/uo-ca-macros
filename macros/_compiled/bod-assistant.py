"""
Name: BOD Assistant
Description: Used to automate monotonous parts of completing Bulk Order Deeds
Author: Tsai (Ultima Adventures)
Version: v0.3
"""

from Assistant import Engine
from ClassicAssist.UO import UOMath

class Color:
    LightPink = 31
    LightPurple = 16
    Orange = 43
    Red = 33

class Logger:
    DEBUG = False
    TRACE = False

    TraceColor = Color.LightPink
    DebugColor = Color.LightPurple
    InfoColor = Color.Orange
    ErrorColor = Color.Red

    @classmethod
    def Trace(cls, message):
        if not Logger.TRACE: return
        SysMessage("[trace]: " + message, cls.TraceColor)

    @classmethod
    def Debug(cls, message):
        if not Logger.DEBUG: return
        SysMessage("[debug]: " + message, cls.DebugColor)

    @classmethod
    def Error(cls, message):
        SysMessage("[error]: " + message, cls.ErrorColor)

    @classmethod
    def Log(cls, message):
        SysMessage(message, cls.InfoColor)


class BODContext:
    def __init__(self):
        self.is_large = None
        self.require_exceptional = None
        self.require_amount = None
        self.require_resource = None # Optional
        self.items_counts_by_name = {}


    def __str__(self):
        values = [
            "Large BOD" if self.is_large else "Small BOD",
            "Requires exceptional" if self.require_exceptional else "Optional exceptional",
            "{}".format(self.require_resource) if self.require_resource else "unknown resource",
        ]

        require_amount = self.require_amount if self.require_amount else "unknown amount"
        for item_name, count in self.items_counts_by_name.items():
            values.append("{} ({} / {})".format(item_name, count, require_amount))

        return "\n".join(values)

    
    def GetRemainingAmount(self, item_name):
        current = self.items_counts_by_name[item_name]
        return self.require_amount - current if current != None else 0


    def GetIncompleteItem(self):
        for item_name in self.items_counts_by_name.keys():
            if 0 < self.GetRemainingAmount(item_name): return item_name

        return None


    def IsComplete(self):
        return True if self.require_amount and not self.GetIncompleteItem() else False


class BODFactory:
    @classmethod
    def Create(cls, item):
        context = BODContext()
        for property in item.Properties:
            if not cls.__is_type_set(context): # Find BOD Size
                Logger.Debug("Looking for Type: " + property.Text)
                if "large bulk order" in property.Text:
                    context.is_large = True
                elif "small bulk order" in property.Text:
                    context.is_large = False
                continue

            if not cls.__is_exceptional_set(context): # Try to set Exceptional
                Logger.Debug("Looking for Exceptional: " + property.Text)
                exceptional_line = "All items must be exceptional."
                if exceptional_line == property.Text: context.require_exceptional = True
                if cls.__is_exceptional_set(context): continue # If it's set, nothing else can be on this line

            if not cls.__is_resource_set(context): # Try to set Resource
                Logger.Debug("Looking for Resource: " + property.Text)
                resource_line = "crafted with "
                resource_index = property.Text.IndexOf(resource_line)
                if 0 <= resource_index:
                    context.require_resource = property.Text[resource_index + len(resource_line):]
                    if not cls.__is_exceptional_set(context): context.require_exceptional = False # If not set by now, Exceptional is not required
                    continue # If it's set, nothing else can be on this line

            # Discard properties until we know the amount crafted
            if not cls.__is_amount_set(context):
                Logger.Debug("Looking for Amount: " + property.Text)
                if not property.Text.startswith("amount"): continue
                amount_line = "amount to make: "
                context.require_amount = int(property.Text[len(amount_line):])
                continue


            # Items
            Logger.Debug("Looking for Item and Count: " + property.Text)
            item_name, count = property.Text.Split(":")
            context.items_counts_by_name[item_name] = int(count)
        
        return context if cls.__is_type_set(context) else None


    @staticmethod
    def __is_amount_set(context):
        return context.require_amount != None


    @staticmethod
    def __is_exceptional_set(context):
        return context.require_exceptional != None


    @staticmethod
    def __is_resource_set(context):
        return context.require_resource != None


    @staticmethod
    def __is_type_set(context):
        return context.is_large != None

class CraftResourceItem:
    """An item that is required for crafting"""
    def __init__(self, graphic, name, hue, min_pack_amount, restock_amount):
        self.graphic = graphic
        self.name = name
        self.hue = hue
        self.min_pack_amount = min_pack_amount
        self.restock_amount = restock_amount


    def clone(self):
        return CraftResourceItem(self.graphic, self.name, self.hue, self.min_pack_amount, self.restock_amount)


    def __str__(self):
        return self.name


class AliasUtils:
    @classmethod
    def CreateCharacterAlias(cls, alias, force = False):
        """Returns an alias that is pre-pended with the character name"""
        name = Engine.Player.Name.strip() # Sometimes there's a leading/trailing space
        if not force and alias.startswith(name): return alias # Assume it was already formatted

        return "{}-{}".format(name, alias)


    @classmethod
    def Ensure(cls, alias, prepend = True):
        """Searches for the `alias` and prompts if it is not found"""
        if prepend: alias = cls.CreateCharacterAlias(alias)
        if not FindAlias(alias): return cls.Prompt(alias, False)

        return alias


    @classmethod
    def EnsureContainer(cls, alias, prepend = True):
        """Searches for the `alias` and prompts if it is not found or it is a mobile"""
        if prepend: alias = cls.CreateCharacterAlias(alias)
        if FindAlias(alias):
            backpack = cls.GetBackpackSerial(alias)
            if backpack != None: SetMacroAlias(alias, backpack)
            return alias

        return cls.PromptContainer(alias, False)


    @classmethod
    def Prompt(cls, alias, prepend = True):
        """Prompts the user to set a value for the alias"""
        if prepend: alias = cls.CreateCharacterAlias(alias)
        PromptMacroAlias(alias)

        return alias


    @classmethod
    def PromptContainer(cls, alias, prepend = True):
        """Prompts the user for the target and attempts to set the alias value to the mobile's Backpack"""
        if prepend: alias = cls.CreateCharacterAlias(alias)
        PromptMacroAlias(alias)

        backpack = cls.GetBackpackSerial(alias)
        if backpack != None:
            SetMacroAlias(alias, backpack)

        return alias


    @classmethod
    def IsMobile(cls, alias):
        """Returns `True` if the serial of the alias is in the range for Mobiles"""
        return UOMath.IsMobile(alias)


    @classmethod
    def GetBackpackSerial(cls, alias):
        """Attempts to return the Backpack of the mobile"""
        serial = GetAlias(alias)
        if cls.IsMobile(serial):
            mobile = Engine.Mobiles.GetMobile(serial)
            if mobile and mobile.Backpack: return mobile.Backpack # Set the backpack if it exists
        # TODO: If it's not a Container ... good luck. Tough determining if it's a Container
        
        return None


class StockService:
    """Moves a `CraftResourceItem` between the `restock_container` and the `destination` or `source`"""
    def __init__(self, restock_container):
        self.restock_container = AliasUtils.EnsureContainer(restock_container)
        self.item_delay = 1500
        self.need_open = True # Warning: Only perform once per instance lifetimes


    def FindItem(self, name):
        if not self.__TryOpenRestock(): return None

        restock_container = Engine.Items.GetItem(GetAlias(self.restock_container))

        return self.__FindItemByName(name, restock_container.Container)


    def GetResource(self, name, min_pack_amount, restock_amount):
        item = self.FindItem(name)
        if not item:
            Logger.Error("Failed to create resource for item '{}'.".format(name))
            raise Exception()
        
        return CraftResourceItem(item.ID, item.Name, item.Hue, min_pack_amount, restock_amount)


    def Load(self, craft_resource_item_or_array, destination = "backpack"):
        if not self.__TryOpenRestock(): return False
        if not isinstance(craft_resource_item_or_array, list): craft_resource_item_or_array = [craft_resource_item_or_array] # Convert a single entity into an array

        for craft_resource in craft_resource_item_or_array:
            if craft_resource.min_pack_amount <= CountType(craft_resource.graphic, destination, craft_resource.hue):
                Logger.Trace("Sufficient amount of {}. Skipping restock.".format(craft_resource.name))
                continue
        
            Logger.Debug("Checking for {} ({})".format(craft_resource.name, self.restock_container))

            if not CountType(craft_resource.graphic, self.restock_container, craft_resource.hue):
                Logger.Error("OUT OF {} !".format(craft_resource.name).upper())
                return False

            # TODO: Pull as much as we can until we no longer have space & warn
            Logger.Trace("Attempting to move {} '{}'".format(craft_resource.restock_amount, craft_resource.name))
            MoveType(craft_resource.graphic, self.restock_container, destination, -1, -1, -1, craft_resource.hue, craft_resource.restock_amount)
            Pause(self.item_delay)

        return True


    def Unload(self, craft_resource_item_or_array, source = "backpack"):
        if not isinstance(craft_resource_item_or_array, list): craft_resource_item_or_array = [craft_resource_item_or_array] # Convert a single entity into an array

        for craft_resource in craft_resource_item_or_array:
            Logger.Debug("Unloading {} ({})".format(craft_resource.name, self.restock_container))

            if not FindType(craft_resource.graphic, 3, self.restock_container, craft_resource.hue): return False

            # Pause(self.short_pause)
            MoveType(craft_resource.graphic, source, self.restock_container, -1, -1, -1, craft_resource.hue, craft_resource.restock_amount)
            Pause(self.item_delay)
        return True


    def __FindItemByName(self, name, container):
        all_items = container.GetItems()
        name_normalized = name.ToLower()
        for item in all_items:
            if item.Name.ToLower().strip().Contains(name_normalized): return item
        
        return None

    
    def __TryOpenRestock(self):
        if not self.need_open: return True # Assume it's open already

        restock_serial = GetAlias(self.restock_container)
        if not restock_serial:
            Logger.Error("Failed to find restock container ({})".format(self.restock_container))
            return False

        Pause(self.item_delay) # This happens infrequently. Delay to guarantee it can be opened.
        UseObject(restock_serial)
        Pause(self.item_delay)
        self.need_open = False # Flip bit

        return True

class InteractionUtils:
    @classmethod
    def Prompt(cls, title, content, footer):
        return ConfirmPrompt(
            "<center>{}</center>".format(title)
            + content
            + "<br><br>" 
            + footer
            )


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


def Main():
    assistant = BodAssistant()
    assistant.Run()


# Execute Main()
#Logger.DEBUG = True
#Logger.TRACE = True
Main()
