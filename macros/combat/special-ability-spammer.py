"""
Name: Special Ability Spammer
Description: Used to keep a special ability active
Author: Tsai (Ultima Adventures)
Version: v1.1
"""

import System
from Assistant import Engine
import clr
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from ClassicAssist.UO.Objects.Gumps import ElementType


class UserOptions:
    Ability_To_Spam = None # The Ability Number to keep active. If None, you will be prompted each run.
    Check_Interval = 500 # The frequency to check the if the ability is active.


class AbilityGump:  
    Special_Abilities_Gump_Id = 0xb2741653
    Ability_Set_Image_Id = 9780
    Ability_Unset_Image_Id = 9781
    
    @classmethod
    def GetAbilities(cls):
        gump = cls.GetGump()
        if gump == None: return []
        
        text_items = gump.GetElementsByType(ElementType.text).Select(lambda g: g.Text).ToArray()
        if len(text_items): return text_items
        
        abilities = []
        for i in range(6):
            image = cls.GetAbilityImage(i)
            if image == cls.Ability_Set_Image_Id or image == cls.Ability_Unset_Image_Id:
                abilities.append("Ability {}".format(i))
        
        return abilities
    
    @classmethod
    def GetGump(cls):
        if not GumpExists(cls.Special_Abilities_Gump_Id):
            SysMessage("Failed to locate Special Ability Gump")
            return None

        tuple = Engine.Gumps.GetGump(cls.Special_Abilities_Gump_Id)
        return tuple[1]

    @classmethod
    def GetAbilityImage(cls, i):
        gump = cls.GetGump()
        if gump == None: return None
        
        x_target = 15
        y_base = 8
        y_offset = 41
        y_target = y_base + y_offset * i
        element = gump.GetElementByXY(x_target, y_target)
        if element == None: return None
        
        return element.ElementID

    @classmethod
    def IsAbilitySet(cls, i):
        image = cls.GetAbilityImage(i)
        if image == None: return False

        return image == cls.Ability_Set_Image_Id
    
    @classmethod
    def SetAbility(cls, i):
        if cls.IsAbilitySet(i): return False
        
        ReplyGump(cls.Special_Abilities_Gump_Id, i)
        return True


def Main():
    Msg("[sad") # Ensure the gump is opened
    if not WaitForGump(AbilityGump.Special_Abilities_Gump_Id, 5000) and not AbilityGump.GetGump():
        SysMessage("Failed to detect ability gump")
        return

    ability_list = AbilityGump.GetAbilities()

    if UserOptions.Ability_To_Spam == None:
        confirmed, index = SelectionPrompt(ability_list, "Select an ability to keep active")
        if not confirmed: return
        
    else:
        index = UserOptions.Ability_To_Spam - 1 # Zero indexed

    while not Dead():
        if AbilityGump.SetAbility(index + 1):
            SysMessage("Set ability {}".format(ability_list[index]))
        Pause(UserOptions.Check_Interval)


# Execute Main()
Main()