from ClassicAssist.Data.Macros.Commands.AliasCommands import GetAlias
from ClassicAssist.Data.Macros.Commands.MainCommands import Pause
from ClassicAssist.Data.Macros.Commands.ObjectCommands import FindType, IgnoreObject, MoveItem, MoveItemOffset


class ItemUtils:
    @classmethod
    def Move(cls, graphic, hue, distance, source, destination, ignore_destination_first = False):
        if ignore_destination_first:
            while FindType(graphic, distance, destination, hue): IgnoreObject("found")

        cls.__Move(graphic, hue, distance, source, lambda item: MoveItem(item, destination))


    @classmethod
    def MoveToOffset(cls, graphic, hue, distance, source, destination):
        cls.__Move(graphic, hue, distance, source, lambda item: MoveItemOffset(item, destination.x, destination.y, destination.z))


    @classmethod
    def __Move(cls, graphic, hue, distance, source, move_fn):
        items = []
        while FindType(graphic, distance, source, hue):
            items.append(GetAlias("found"))
            IgnoreObject("found")
                
        for item in items:
            move_fn(item)
            Pause(750)