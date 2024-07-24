from Assistant import Engine
from ClassicAssist.UO import UOMath
from ClassicAssist.UO.Data import Direction, MapInfo , Statics, TileFlags
from System import Convert


class Location:
    def __init__(self, x, y, z = None):
        self.x = x
        self.y = y
        
        if z == None: z = 0
        self.z = z

    def __str__(self):
        return "{}, {}".format(self.x, self.y)


class LocationUtils:
    @classmethod
    def IncrementTowards(cls, location, direction):
        """Moves the location toward the direction by 1 tile"""

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
    def FindClosestIndex(cls, locations, distance_fn):
        """Returns the index of the closest location"""

        best_distance = None
        best_index = None
        for i, location in enumerate(locations):
            distance = distance_fn(location)
            if best_distance == None or distance < best_distance:
                best_index = i
                best_distance = distance
        return best_index


    @classmethod
    def FindOppositeDirection(cls, direction):
        """Returns the inverted direction"""
        
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

        return UOMath.MapDirection(Engine.Player.X, Engine.Player.Y, x, y)


    @classmethod
    def GetDistance(cls, location): # Object required for Sort method
        """Calculates the distance to the point, relative to the Player"""

        return UOMath.Distance(Engine.Player.X, Engine.Player.Y, location.x, location.y)


    @classmethod
    def IsAtLocation(cls, x, y):
        """Returns `True` if the Player is at the position `X, Y`"""

        return Engine.Player.X == x and Engine.Player.Y == y


    @classmethod
    def IsEmptyTile(cls, x, y):
        """Returns `True` if the location does not contain an `Impassable` land tile or static"""

        map = Convert.ChangeType(Engine.Player.Map, int)
        land_tile = MapInfo.GetLandTile(map, x, y)
        if land_tile == None: return False
        
        if land_tile.Flags.HasFlag(TileFlags.Impassable): return False

        statics = Statics.GetStatics(map, x, y)
        if statics != None:
            for s in statics:
                if s.Flags.HasFlag(TileFlags.Impassable): return False
        
        return True


    @classmethod
    def TryGetEmptySpace(cls, origin):
        """Returns the first `Direction` of an empty tile around the `origin`"""
        
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

        if (direction == Direction.North): return Direction.Northeast
        if (direction == Direction.Northeast): return Direction.East
        if (direction == Direction.East): return Direction.Southeast
        if (direction == Direction.Southeast): return Direction.South
        if (direction == Direction.South): return Direction.Southwest
        if (direction == Direction.Southwest): return Direction.West
        if (direction == Direction.West): return Direction.Northwest
        if (direction == Direction.Northwest): return Direction.North

        return None