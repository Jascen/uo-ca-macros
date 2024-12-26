"""
Name: Combat Bar parser
Description: Example code to extract values from the Combat Bar
Author: Tsai (Ultima Adventures)
Version: v1.0
"""


import System
from Assistant import Engine
import clr
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from ClassicAssist.UO.Objects.Gumps import ElementType

class XmlParser:
    @classmethod
    def GetValue(cls, xml_element, element_name):
        """
        Tries to return the inner value of an element
        """
        begin_index = xml_element.find('>') # The first instance of <{element}...'>'
        if begin_index < 0: return None

        end_index = xml_element.find(element_name, begin_index) # The start of the closing element
        if end_index < 0: return None
        
        return xml_element[begin_index + 1:end_index - 2] # Offset '>' and '</'

    @classmethod
    def GetIntValue(cls, xml_element, element_name):
        value = cls.GetValue(xml_element, element_name)
        if not value: return None

        return int(value.strip())

class CombatBar:  
    Gump_Id = 0xef79c51d
    ElementName = "BASEFONT"
    
    @classmethod
    def GetValue(cls, key):
        gump = cls.GetGump()
        if gump == None:
            return None
        
        text_items = gump.GetElementsByType(ElementType.htmlgump).Select(lambda g: g.Text).ToArray()
        if len(text_items):
            for i, row in enumerate(text_items):
                if key == XmlParser.GetValue(row, cls.ElementName): # Label element
                    return XmlParser.GetIntValue(text_items[i + 1], cls.ElementName) # Next element is Value 
        
        return None

    @classmethod
    def GetGump(cls):
        if not GumpExists(cls.Gump_Id):
            SysMessage("Failed to locate Combat Bar Gump")
            return None

        tuple = Engine.Gumps.GetGump(cls.Gump_Id)
        return tuple[1]

    @classmethod
    def Open(cls):
        Msg("[combatbar") # Ensure the gump is opened
        if not WaitForGump(cls.Gump_Id, 5000) and not cls.GetGump():
            SysMessage("Failed to detect combat bar gump")
            return False

        return True

def Main():
    CombatBar.Open()
    hunger = CombatBar.GetValue('Hunger')
    thirst = CombatBar.GetValue('Thirst')
    print('Hunger {}'.format(hunger))
    print('Thirst {}'.format(thirst))


# Execute Main()
Main()