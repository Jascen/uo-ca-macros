from ClassicAssist.Data.Macros.Commands.AliasCommands import GetAlias
from ClassicAssist.Data.Macros.Commands.MainCommands import Pause
from ClassicAssist.Data.Macros.Commands.MovementCommands import Pathfind, Pathfinding
from ClassicAssist.Data.Macros.Commands.ObjectCommands import FindType, IgnoreObject, MoveItem, ClearIgnoreList
from ClassicAssist.UO import UOMath
from Assistant import Engine

from utility.alias import AliasUtils
from utility.location import LocationUtils


class Scavenger:
    """Detects items on the ground, runs to them if they're out of range, and then moves them to the `destination_container`"""
    def __init__(self, destination_container):
        self.destination_container = AliasUtils.EnsureContainer(destination_container)


    def Loot(self, type_id_or_ids, distance):
        ClearIgnoreList()

        # Allow a single id or an array
        type_ids = type_id_or_ids
        if not isinstance(type_ids, list): type_ids = [type_ids]

        # Build the list of items
        items = []
        for id in type_ids:
            while FindType(id, distance):
                item = Engine.Items.GetItem(GetAlias("found"))
                items.append(item)
                IgnoreObject("found")

        # Run and loot
        max_pickup_distance = 2
        while any(items):
            # Get the nearest item
            i = LocationUtils.FindClosestIndex(items, lambda item: UOMath.Distance(Engine.Player.X, Engine.Player.Y, item.X, item.Y))
            item = items[i]

            # Move to it if necessary
            if (max_pickup_distance < abs(item.X - Engine.Player.X)) or (max_pickup_distance < abs(item.Y - Engine.Player.Y)):
                Pathfind(item)
                Pause(250)
                while Pathfinding(): Pause(250)

            # Move it
            MoveItem(item, self.destination_container)
            Pause(750)

            items.remove(item)