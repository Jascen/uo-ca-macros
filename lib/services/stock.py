from Assistant import Engine
from ClassicAssist.Data.Macros.Commands.AliasCommands import GetAlias
from ClassicAssist.Data.Macros.Commands.MainCommands import Pause
from ClassicAssist.Data.Macros.Commands.ObjectCommands import UseObject, CountType, FindType, MoveType

from models.craftresourceitem import CraftResourceItem
from utility.alias import AliasUtils
from diagnostic.logger import Logger


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