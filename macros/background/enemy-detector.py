"""
Name: Automatic Enemy Detector
Description: Notifies the User of any enemies (based on Notoriety) within the designated range
Author: Tsai (Ultima Adventures)
Version: v1.0
"""

import System
from Assistant import Engine
import clr
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)


class UserOptions:
    Detection_suppression_delay = 15000 # Amount of time to do NOTHING after detecting an enemy
    Enemy_detection_range = 18 # Max number of tiles away to check for enemies
    Enemy_headmsg = "*** Enemy ***" # Message to show above enemy. Used if Colors are provided
    Enemy_alert_sounds = [ # Sounds to play. Can be empty.
        "get-to-the-chopper.wav",
        "get-to-the-chopper.wav",
        # "get-to-the-chopper.wav",
        # "Bike Horn.wav", # The only default sound file
    ]
    Enemy_headmsg_colors = [ # Colors. Can be empty.
        33,
        1162,
        1161,
    ]
    Flagged_notorieties = [ # Notorieties to flag on. At least one is required
        "Murderer",
        # "Attackable",
        "Criminal",
        # "Enemy",
        # "Innocent",
        # "Ally",
        # "Invulnerable",
        # "Invalid",
        # "Unknown"
    ]

# TODO: Identify all regions and update "Regions.json" file
regions_to_suppress = [ # A list of places to avoid running the script. Can be empty
    # "Town",
    # "Guarded",
    # "None",
    # "Jail",
    # "Wilderness",
    # "Dungeon",
    # "Special",
    # "Default",
]
#


class Enemies:
    def __init__(self, notorieties):
        IgnoreObject("self")
        self.notorieties = notorieties
        self.refresh()

    def refresh(self, search_distance=1):
        self._mobiles = self._find_enemies(search_distance)

    def are_amount_eq(self, number):
        return self._mobiles.Count() == number
        
    def current_target(self):
        if self.are_amount_eq(0):
            return None

        target = self._mobiles.First().Serial
        if target == GetAlias("self"):
            return None
        else:
            return target

    def _find_enemies(self, distance=1):
        return Engine.Mobiles.Where(lambda m: m != None
                                    and (str(m.Notoriety) in self.notorieties)
                                    and m.Distance <= distance
                                    and not InIgnoreList(m.Serial)
                                    ).OrderBy(lambda m: m.Distance)


def CheckForAnyRegion(regions, alias):
    for i, region in enumerate(regions):
        if InRegion(region, alias): return True

    return False


def Main():
    check = Enemies(UserOptions.Flagged_notorieties)

    show_enemy_headmsg = 0 < len(UserOptions.Enemy_headmsg_colors)
    play_enemy_alert_sounds = 0 < len(UserOptions.Enemy_alert_sounds)
    check_region = 0 < len(regions_to_suppress)

    last_target = None
    while not Dead():
        if check_region and CheckForAnyRegion(regions_to_suppress, "self"): continue

        check.refresh(UserOptions.Enemy_detection_range)

        target = check.current_target()
        if target and (last_target == None or target != last_target):
            if show_enemy_headmsg:
                for i, color in enumerate(UserOptions.Enemy_headmsg_colors):
                    HeadMsg(enemy_headmsg, target, color)

            if play_enemy_alert_sounds:
                for i, sound in enumerate(UserOptions.Enemy_alert_sounds):
                    SysMessage(str(i))
                    PlaySound(sound)
                    Pause(i + 1 * 1000)
            last_target = target

            Pause(UserOptions.Detection_suppression_delay)
        else:
            Pause(500) # No reason to spin CPU


# Execute Main
Main()
