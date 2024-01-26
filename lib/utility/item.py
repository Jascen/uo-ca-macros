from ClassicAssist.Data.Macros.Commands.AliasCommands import GetAlias
from ClassicAssist.Data.Macros.Commands.MainCommands import Pause
from ClassicAssist.Data.Macros.Commands.ObjectCommands import FindType, IgnoreObject, MoveItem, MoveItemOffset


class ItemUtils:
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
        items = []
        while FindType(graphic, distance, source_serial_or_alias, hue):
            items.append(GetAlias("found"))
            IgnoreObject("found")
                
        for item in items:
            move_fn(item)
            Pause(750)