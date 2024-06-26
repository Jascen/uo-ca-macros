"""
Name: Location Decoder
Description: Convert Sextant coordinates to Facet XY coordinates
Shard: Ultima Adventures
Author: Tsai
Version: v2.0
"""

import re
from Assistant import Engine


class UserOptions:
    Prompt_For_Target = True # If you want to target a specific item
    Check_Open_Gumps = True # If you want all open gumps to be checked


def GetFacets():
    # Warning: Order matters and it's index must directly match CA
    return [
        Facet("Lodoria", 2560, 2047),
        Facet("Sosaria", 2560, 1563),
        # Facet("Darkmoor", None, None), # Does not support Sextant
        Facet("Serpent Island", 935, 1023),
        Facet("Isle of Dread", 723, 723, 1448, 1448),
        Facet("Savaged Empire", 648, 900),  
    ]

def GetParsers():
    return [
        # Encoded Messages - Facet is random
        GumpParser(
            [
                0x4CC6,
                0x4CC7,
            ], # Graphic Ids
            0x9ddfb810, # Gump Id
            1, # Element Number
            DMSRegexParser.ParseSpaced
        ),
        
        # SOS - Facet should be where you found it
        GumpParser(
            [
                0x14ed,
            ], # Graphic Ids
            0x550a461b, # Gump Id
            2, # Element Number
            DMSRegexParser.ParseUnspaced
        ),
        
        # Treasure Map - Facet is random
        PropertyParser(
            [
                0x14ec,
            ], # Graphic Ids
            DMSRegexParser.ParseSpaced
        ),
    ]

#------------------------
# Parsers
#------------------------
class AutoGumpParser:
    def Parse(self, gump):
        for element in gump.GumpElements:
            if not element.Text: continue
            if "°" not in element.Text: continue            

            coordinates = DMSRegexParser.ParseUnspaced(element.Text)
            if not coordinates: coordinates = DMSRegexParser.ParseSpaced(element.Text)
            if not coordinates: print("Failed to parse coordinates: {}".format(element.Text))

            return coordinates

class GumpParser:
    def __init__(self, item_type_ids, gump_id, gump_element_number, parse_fn):
        self.item_type_ids = item_type_ids
        self.gump_id = gump_id
        self.gump_element_number = gump_element_number
        self.gump_timeout = 5000
        self.parse_fn = parse_fn
        
    def Parse(self, item):
        # Use item
        i = 0
        UseObject(item)
        while not WaitForGump(self.gump_id, self.gump_timeout):
            UseObject(item)
            Pause(1000)
            i += 1
            if i > 3:
                print("Failed to open item ({})".format(item.Serial))
                return None
        
        found, gump = Engine.Gumps.GetGump(self.gump_id)
        if not found:
            print("Failed to get gump ({})".format(self.gump_id))
            return None
            
        value = gump.GumpElements[self.gump_element_number].Text
        if not value:
            print("Failed to get gump value ({})".format(self.gump_id))
            return None
            
        coordinate = self.parse_fn(value)
        if coordinate == None:
            print("Failed to parse coordinate")
            print(value)
            return None
        
        return coordinate

class PropertyParser:
    def __init__(self, item_type_ids, parse_fn):
        self.item_type_ids = item_type_ids
        self.parse_fn = parse_fn
        
    def Parse(self, item):
        for property in item.Properties:
            coordinate = self.parse_fn(property.Text)
            if coordinate: return coordinate

        return None
        
class DMSRegexParser:
    regex = re.compile("([0-9]+)°([0-9]+)'([N|S]),([0-9]+)°([0-9]+)'([W|E])")
    regex_spaced = re.compile("([0-9]+)° ([0-9]+)'([N|S]), ([0-9]+)° ([0-9]+)'([W|E])")
    
    @classmethod
    def Parse(cls, dms_value, regex):
        matches = regex.finditer(dms_value)
        if matches == None: return None

        results = []
        for m in matches:
            xLong = int(m.group(4))
            xMins = int(m.group(5))
            xEast = m.group(6) == "E"
            yLat = int(m.group(1))
            yMins = int(m.group(2))
            ySouth = m.group(3) == "S"
            results.append(DMSCoordinate(xLong, xMins, xEast, yLat, yMins, ySouth))
        
        return results
        
    @classmethod
    def ParseSpaced(cls, dms_value):
        return cls.Parse(dms_value, cls.regex_spaced)
    
    @classmethod
    def ParseUnspaced(cls, dms_value):
        return cls.Parse(dms_value, cls.regex)

#------------------------
# Models
#------------------------
class Facet:
    def __init__(self, name, center_x, center_y, width = 5120, height = 4096):
        self.name = name
        # The X/Y coordinates at 0°0'(N|S),0°0'(E|W)
        self.center_x = center_x
        self.center_y = center_y
        # The full dimensions of the Facet
        self.width = width
        self.height = height

class DMSCoordinate:
    def __init__(self, x_longitude, x_mins, is_east, y_latitude, y_mins, is_south):
        self.y_latitude = y_latitude
        self.y_mins = y_mins
        self.is_east = is_east
        self.x_longitude = x_longitude
        self.x_mins = x_mins
        self.is_south = is_south

    def AsXY(self, facet):
        longitude = self.x_longitude + self.x_mins / 60
        latitude = self.y_latitude + self.y_mins / 60
        
        # Translate if necessary
        if not self.is_east: longitude = 360 - longitude
        if not self.is_south: latitude = 360 - latitude

        x = facet.center_x + longitude * facet.width / 360
        y = facet.center_y + latitude * facet.height / 360

        # Roll over boundaries
        if x < 0: x += facet.width
        if y < 0: y += facet.height
        if x > facet.width: x -= facet.width
        if y > facet.height: y -= facet.height

        return (x, y)

    def __str__(self):
        lon_dir = "E" if self.is_east else "W"
        lat_dir = "S" if self.is_south else "N"
        return "{}° {}'{}, {}° {}'{}".format(self.y_latitude, self.y_mins, lat_dir, self.x_longitude, self.x_mins, lon_dir)

#------------------------
# Main
#------------------------
def Main():
    if UserOptions.Check_Open_Gumps:
        print("Checking all open gumps...")
        parser = AutoGumpParser()
        success, gumps = Engine.Gumps.GetGumps()
        if not success:
            SysMessage("Failed to find any open gumps", 33)
            return

        for gump in gumps:
            coordinates = parser.Parse(gump)
            if not coordinates:
                print("Gump ({}) has no coordinates".format(hex(gump.Serial)))
                continue

            print("-- Gump Results ({}) --".format(hex(gump.ID)))
            for coordinate in coordinates:
                SysMessage("Coordinate: {}".format(coordinate), 33)
                for facet in GetFacets():
                    x, y = coordinate.AsXY(facet)
                    SysMessage('({}) X: {}, Y: {}'.format(facet.name, x, y), 43)
    
    if UserOptions.Prompt_For_Target:
        UnsetAlias("$Target")
        PromptMacroAlias("$Target")
        item = Engine.Items.GetItem(GetAlias("$Target"))
        if item == None:
            SysMessage("Failed to find targeted item", 33)
            return
        
        for parser in GetParsers():
            if not item.ID in parser.item_type_ids:
                SysMessage("Unsupported item id: {}".format(item.ID), 33)
                continue
            
            coordinates = parser.Parse(item)
            if not coordinates:
                print("Item '{}' has no coordinates".format(item.Name))
                continue

            print("-- Item Results --")
            for coordinate in coordinates:
                for facet in GetFacets():
                    x, y = coordinate.AsXY(facet)
                    SysMessage('({}) X: {}, Y: {}'.format(facet.name, x, y), 43)
            break

            
# Execute Main
Main()