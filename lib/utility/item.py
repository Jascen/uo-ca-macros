from ClassicAssist.Data.Macros.Commands.AliasCommands import GetAlias, PromptMacroAlias
from ClassicAssist.Data.Macros.Commands.MainCommands import Pause
from ClassicAssist.Data.Macros.Commands.ObjectCommands import FindType, IgnoreObject, MoveItem, MoveItemOffset
from Assistant import Engine


class ItemUtils:
    @classmethod
    def GetAll(cls, graphic, hue, distance, source_serial_or_alias):
        items = []
        while FindType(graphic, distance, source_serial_or_alias, hue):
            items.append(GetAlias("found"))
            IgnoreObject("found")
        
        return items


    @staticmethod
    def PromptForType():
        """Prompts the User to select an item and returns the Graphic ID"""
        target_serial = PromptMacroAlias("$item_type")
        if target_serial == None: return None

        item = Engine.Items.GetItem(target_serial)
        if item == None: return None

        return item.ID


    @classmethod
    def Move(cls, graphic, hue, distance, source_serial_or_alias, destination_serial_or_alias, ignore_destination_first = False):
        """Moves the items to the destination container"""
        if ignore_destination_first:
            while FindType(graphic, distance, destination_serial_or_alias, hue): IgnoreObject("found")

        cls.__Move(graphic, hue, distance, source_serial_or_alias, lambda item: MoveItem(item, destination_serial_or_alias))


    @classmethod
    def MoveToOffset(cls, graphic, hue, distance, source_serial_or_alias, x, y, z):
        """Moves the items to the ground offset position"""
        cls.__Move(graphic, hue, distance, source_serial_or_alias, lambda item: MoveItemOffset(item, x, y, z))


    @classmethod
    def __Move(cls, graphic, hue, distance, source_serial_or_alias, move_fn):
        items = cls.GetAll(graphic, hue, distance, source_serial_or_alias)
                
        for item in items:
            move_fn(item)
            Pause(750)