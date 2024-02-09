"""
Name: Automagic miner
Description: Attempts to completely mine every spot around you.
    Overweight behavior is configurable.
Author: Tsai (Ultima Adventures)
Version: v1.2
"""


from System import Convert
from Assistant import Engine
from ClassicAssist.UO import UOMath
from ClassicAssist.UO.Data import Direction, MapInfo


class OverweightBehavior:
    Stop = 0 # Stop the script
    Smelt = 1 # Smelt the ore in a forge that you have with you
    Move = 2 # Move the ore to a bag or pack animal


# Manual Configuration - Begin
class UserOptions:
    Overweight_threshold = 10 # When your available weight is less than this value, execute Overweight behavior
    Overweight_behavior = OverweightBehavior.Smelt
    Max_retries = 100 # Default to 15
    Mining_directions = [
        Direction.North,
        Direction.Northeast,
        Direction.Southeast,
        Direction.South,
        Direction.Southwest,
        Direction.West,
        Direction.Northwest,
    ]
#UserOptions.Mining_directions = [ Direction.North ] # OVERRIDE HERE!!
# Manual Configuration - End

# IDs
crafting_gump_id = 0x38920abd
tinker_tool_id = 0x1eb8
large_ore_id = 0x19b9
shovel_id = 0xf39
pickaxe_id = 0xe85
# IDs


mountain_and_cave_tiles = {
    220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231,
    236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247,
    252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263,
    268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279,
    286, 287, 288, 289, 290, 291, 292, 293, 294, 296, 296, 297,
    321, 322, 323, 324,
    467, 468, 469, 470, 471, 472, 473, 474, 476, 477, 478, 479,
    480, 481, 482, 483, 484, 485, 486, 487,
    492, 493, 494, 495,
    543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554,
    555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566,
    567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 
    579,
    581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 
    593, 594, 595, 596, 597, 598, 599, 600, 601,
    610, 611, 612, 613,

    1010, 
    1741, 1742, 1743, 1744, 1745, 1746, 1747, 1748, 1749,
    1750, 1751, 1752, 1753, 1754, 1755, 1756,
    1757, 1771, 1772, 1773, 1774, 1775, 1776, 1777, 1778, 1779,
    1780, 1781, 1782, 1783, 1784, 1785, 1786, 1787, 1788, 1789, 
    1790, 1801, 1802, 1803, 1804, 1805, 1806, 1807, 1808, 1809,
    1811, 1812, 1813, 1814, 1815, 1816, 1817, 1818, 1819, 1820,
    1821, 1822, 1823, 1824, 
    1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1839, 1840,
    1841, 1842, 1843, 1844, 1845, 1846, 1847, 1848, 1849, 1850,
    1851, 1852, 1853, 1854,
    1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870,
    1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880,
    1881, 1882, 1883, 1884, 1981, 
    1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996,
    1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004,
    2028, 2029, 2030, 2031, 2032, 2033,
    2100, 2101, 2102, 2103, 2104, 2105,

    0x453B, 0x453C, 0x453D, 0x453E, 0x453F, 0x4540, 0x4541,
    0x4542, 0x4543, 0x4544,	0x4545, 0x4546, 0x4547, 0x4548,
    0x4549, 0x454A, 0x454B, 0x454C, 0x454D, 0x454E,	0x454F
}

DEBUG = False

##### Script Start #####
SetQuietMode(not(DEBUG))

def CheckForPause():
    while Dead() or War("self"): 
        Pause(1000)

#Make a shovel when none are left
def MakeShovel():
    if DEBUG: SysMessage("MakeShovel")
    
    if FindType(tinker_tool_id, 0, "backpack"):
        UseObject("Found")                    #Tinker Tools
        WaitForGump(crafting_gump_id, 5000)
        ReplyGump(crafting_gump_id, 8)        #Tools Option
        WaitForGump(crafting_gump_id, 5000)
        ReplyGump(crafting_gump_id, 86)       #Shovel option
        WaitForGump(crafting_gump_id, 5000)
        ReplyGump(crafting_gump_id, 0)        #Close tools
    else:
        HeadMsg("Out of Tinker Tools", "self")
        Stop()
    return


def SmeltOre():
    if DEBUG: SysMessage("Smelt Ore")
    
    Pause(1000) # In case an action previously executed
        
    while FindType(large_ore_id, 0, "backpack"):
        item = Engine.Items.GetItem(GetAlias("found"))
        if item == None: continue

        # Never Smelt Dwarven, Obsidian, Xormite, Zinc, Coal, or Mithril
        if item.Hue == 1788 or item.Hue == 1986 or item.Hue == 1991 or item.Hue == 2500 or item.Hue == 1175 or item.Hue == 2928:
            IgnoreObject("found")
            continue

        UseObject("found")
        WaitForTarget(2000)
        Target("forge")
        Pause(1000)
    return


def MoveType(type_id):
    if DEBUG: SysMessage("Move Ore")
    
    Pause(1000) # In case an action previously executed

    while FindType(type_id, 0, "backpack"):
        MoveItem("found", "ore_destination")
        Pause(750)
    return


def Mine(x_offset, y_offset):
    #Look for Shovel or Pickaxe
    if FindType(shovel_id, 0, "backpack") or FindType(pickaxe_id, 0, "backpack"):
        UseObject("found")
    else:
        MakeShovel()
        return

    if WaitForTarget(1000): TargetTileOffsetResource(x_offset, y_offset, 0)

def MineAroundYou():
    OverweightCheck()
    
    map = Convert.ChangeType(Engine.Player.Map, int)
    for direction in UserOptions.Mining_directions:
        x_offset = 0
        y_offset = 0
        if (direction == Direction.North):
            y_offset = -1
        elif (direction == Direction.Northeast):
            x_offset = -1
            y_offset = -1
        elif (direction == Direction.East):
            x_offset = 1
        elif (direction == Direction.Southeast):
            x_offset = 1
            y_offset = 1
        elif (direction == Direction.South):
            y_offset = 1
        elif (direction == Direction.Southwest):
            x_offset = -1
            y_offset = 1
        elif (direction == Direction.West):
            x_offset = -1
        elif (direction == Direction.Northwest):
            y_offset = -1

        land_tile = MapInfo.GetLandTile(map, Engine.Player.X + x_offset, Engine.Player.Y + y_offset)
        if land_tile != None:
            if land_tile.ID not in mountain_and_cave_tiles: 
                #SysMessage("Skipping ({}, {})".format(direction, Engine.Player.X, Engine.Player.Y))
                continue

            if CleanItOut(x_offset, y_offset):
                    SysMessage("HarvestNode(Direction.{}, {}, {})".format(direction, Engine.Player.X, Engine.Player.Y))


def CleanItOut(x_offset, y_offset):
    ClearJournal()
    
    attempt = 0
    while not Dead():
        CheckForPause()
        attempt += 1
        Mine(x_offset, y_offset)
        Pause(1250)
            
        #Smelt when it gets to heavy
        OverweightCheck()
        
        #Move when there is nothing to mine or when a wall is hit
        if InJournal("There is no metal here to mine", "system")  or InJournal("Target cannot be seen", "system") or InJournal("You can't mine that", "system")  or InJournal("You are not allowed to access this") or InJournal("You can't mine there"):
            ClearJournal()
            return 1 < attempt

        if attempt == UserOptions.Max_retries:
            # Bail idk why we can't hit anything
            return 1 < attempt


def OverweightCheck():
    if DiffWeight() < UserOptions.Overweight_threshold:
        if UserOptions.Overweight_behavior == OverweightBehavior.Smelt:
            SmeltOre()
        elif UserOptions.Overweight_behavior == OverweightBehavior.Move:
            MoveType(large_ore_id)
        else:
            SysMessage("Overweight. Stopping!")
            Stop()


def Main():
    if UserOptions.Overweight_behavior == OverweightBehavior.Smelt and not FindAlias("forge"): PromptMacroAlias("forge")
    if UserOptions.Overweight_behavior == OverweightBehavior.Move and not FindAlias("ore_destination"): PromptMacroAlias("ore_destination")
    
    MineAroundYou()
    HeadMsg("Complete", "self", 33)


# Execute Main()
Main()