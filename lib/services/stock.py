from ClassicAssist.Data.Macros.Commands.AliasCommands import GetAlias
from ClassicAssist.Data.Macros.Commands.MainCommands import Pause
from ClassicAssist.Data.Macros.Commands.ObjectCommands import UseObject, CountType, MoveType

from utility.alias import AliasUtils
from diagnostic.logger import Logger


class StockService:
    def __init__(self, restock_container):
        self.restock_container = AliasUtils.EnsureContainer(restock_container)
        self.item_delay = 1500
        self.need_open = True


    def Load(self, material, destination = "backpack"):
        if self.need_open:
            restock_serial = GetAlias(self.restock_container)
            if not restock_serial:
                Logger.Error("Failed to find restock container ({})".format(self.restock_container))
                return False

            Pause(self.item_delay) # This happens infrequently. Delay to guarantee it can be opened.
            UseObject(restock_serial)
            Pause(self.item_delay)
            self.need_open = False # Flip bit

        if material.minPackAmt <= CountType(material.graphic, destination, material.hue):
            Logger.Trace("Sufficient amount of {}. Skipping restock.".format(material.name))
            return True
    
        Logger.Debug("Checking for {} ({})".format(material.name, self.restock_container))

        if not CountType(material.graphic, self.restock_container, material.hue):
            Logger.Error("OUT OF {} !".format(material.name).upper())
            return False

        Logger.Trace("Attempting to move {}".format(material.restockAmt))
        MoveType(material.graphic, self.restock_container, destination, -1, -1, -1, material.hue, material.restockAmt)
        Pause(self.item_delay)

        return True


    def Unload(self, material, source = "backpack"):
        Logger.Debug("Unloading {} ({})".format(material.name, self.restock_container))

        # Pause(self.short_pause)
        MoveType(material.graphic, source, self.restock_container, -1, -1, -1, material.hue, material.restockAmt)
        Pause(self.item_delay)