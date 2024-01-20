from Assistant import Engine
from ClassicAssist.UO import UOMath
from ClassicAssist.UO.Data import Direction, MapInfo , Statics, TileFlags
from System import Convert

from troubleshoot.logger import Logger


class Location:
    def __init__(self, x, y, z = None):
        self.x = x
        self.y = y
        
        if z == None: z = 0
        self.z = z


class LocationUtils:
    @classmethod
    def IncrementTowards(cls, location, direction):
        """Moves the location toward the direction by 1 tile"""
        Logger.Debug("In LocationUtils.IncrementTowards: {}".format(str(direction)))

        if (direction == Direction.North):
            location.y -= 1
        elif (direction == Direction.Northeast):
            location.x += 1
            location.y -= 1
        elif (direction == Direction.East):
            location.x += 1
        elif (direction == Direction.Southeast):
            location.x += 1
            location.y += 1
        elif (direction == Direction.South):
            location.y += 1
        elif (direction == Direction.Southwest):
            location.x -= 1
            location.y += 1
        elif (direction == Direction.West):
            location.x -= 1
        elif (direction == Direction.Northwest):
            location.x -= 1
            location.y -= 1
        else: return None
        
        return location


    @classmethod
    def DecrementAway(cls, location, direction):
        """Moves the location opposite of the direction by 1 tile"""
        Logger.Debug("In LocationUtils.DecrementAway")

        if (direction == Direction.North):
            location.y += 1
        elif (direction == Direction.Northeast):
            location.x -= 1
            location.y += 1
        elif (direction == Direction.East):
            location.x -= 1
        elif (direction == Direction.Southeast):
            location.x -= 1
            location.y -= 1
        elif (direction == Direction.South):
            location.y -= 1
        elif (direction == Direction.Southwest):
            location.x += 1
            location.y -= 1
        elif (direction == Direction.West):
            location.x += 1
        elif (direction == Direction.Northwest):
            location.x += 1
            location.y += 1
        
        return location


    @classmethod
    def FindClosestIndex(cls, locations):
        """Returns the index of the closest location"""
        Logger.Debug("In LocationUtils.FindClosestIndex")

        best_distance = None
        best_index = None
        for i, location in enumerate(locations):
            distance = cls.GetDistance(location)
            if best_distance == None or distance < best_distance:
                best_index = i
                best_distance = distance
        return best_index


    @classmethod
    def FindOppositeDirection(cls, direction):
        """Returns the inverted direction"""
        Logger.Debug("In LocationUtils.FindOppositeDirection (of {})".format(str(direction)))
        
        if (direction == Direction.North): return Direction.South
        elif (direction == Direction.Northeast): return Direction.Southwest
        elif (direction == Direction.East): return Direction.West
        elif (direction == Direction.Southeast): return Direction.Northwest
        elif (direction == Direction.South): return Direction.North
        elif (direction == Direction.Southwest): return Direction.Northeast
        elif (direction == Direction.West): return Direction.East
        elif (direction == Direction.Northwest): return Direction.Southeast
        else: return Direction.Invalid


    @classmethod
    def GetDirection(cls, x, y):
        """Finds the direction of the location, relative to the Player"""
        Logger.Debug("In LocationUtils.GetDirection")

        return UOMath.MapDirection(Engine.Player.X, Engine.Player.Y, x, y)


    @classmethod
    def GetDistance(cls, location): # Object required for Sort method
        """Calculates the distance to the point, relative to the Player"""
        Logger.Trace("In LocationUtils.GetDistance ({}, {})".format(location.x, location.y))

        return UOMath.Distance(Engine.Player.X, Engine.Player.Y, location.x, location.y)


    @classmethod
    def IsAtLocation(cls, x, y):
        """Returns `True` if the Player is at the position `X, Y`"""
        Logger.Trace("In LocationUtils.IsAtLocation ({}, {})".format(str(x), str(y)))

        return Engine.Player.X == x and Engine.Player.Y == y


    @classmethod
    def IsEmptyTile(cls, x, y):
        """Returns `True` if the location does not contain an `Impassable` land tile or static"""
        Logger.Debug("In LocationUtils.IsEmptyTile ({}, {})".format(str(x), str(y)))

        map = Convert.ChangeType(Engine.Player.Map, int)
        land_tile = MapInfo.GetLandTile(map, x, y)
        if land_tile == None: return False
        
        Logger.Trace("Found land tile: {}".format(land_tile.Name))
        if land_tile.Flags.HasFlag(TileFlags.Impassable): return False

        statics = Statics.GetStatics(map, x, y)
        if statics != None:
            for s in statics:
                Logger.Trace("Found static: {}".format(s.Name))
                if s.Flags.HasFlag(TileFlags.Impassable): return False
        
        return True


    @classmethod
    def TryGetEmptySpace(cls, origin):
        """Returns the first `Direction` of an empty tile around the `origin`"""
        Logger.Debug("In LocationUtils.TryGetEmptySpace ({}, {})".format(str(origin.x), str(origin.y)))
        
        temp = Location(origin.x, origin.y)

        cardinal_directions = [
            Direction.North,
            Direction.Northeast,
            Direction.East,
            Direction.Southeast,
            Direction.South,
            Direction.Southwest,
            Direction.West,
            Direction.Northwest,
        ]
        
        for direction in cardinal_directions:
            # Try new location
            temp.x = origin.x
            temp.y = origin.y
            cls.IncrementTowards(temp, direction)
            
            if cls.IsEmptyTile(temp.x, temp.y): return direction

        return None


    @classmethod
    def RotateClockwise(self, direction):
        """Returns the next clockwise `Direction`"""
        Logger.Debug("In LocationUtils.RotateClockwise (of {})".format(str(direction)))

        if (direction == Direction.North): return Direction.Northeast
        if (direction == Direction.Northeast): return Direction.East
        if (direction == Direction.East): return Direction.Southeast
        if (direction == Direction.Southeast): return Direction.South
        if (direction == Direction.South): return Direction.Southwest
        if (direction == Direction.Southwest): return Direction.West
        if (direction == Direction.West): return Direction.Northwest
        if (direction == Direction.Northwest): return Direction.North

        return None