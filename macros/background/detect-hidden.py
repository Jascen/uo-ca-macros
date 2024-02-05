"""
Name: Automatic Detect Hidden
Description: Detects hidden when there is no cursor and the Player is in Peace mode.
    War mode may be disabled if no attackable enemies are within the configured distance.
Author: Tsai (Ultima Adventures)
Version: v1.0
"""

import System
from Assistant import Engine
import clr
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)


class UserOptions:
    Enemy_detection_range = 18 # Max number of tiles away to check for enemies
    Flagged_notorieties = [ # Notorieties to flag on. At least one is required
        "Murderer",
        "Attackable",
        "Criminal",
        "Enemy",
        # "Innocent",
        # "Ally",
        # "Invulnerable",
        # "Invalid",
        # "Unknown"
    ]


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


def DetectHidden():
    UseSkill("Detect Hidde")
    if not WaitForTarget(5000): return

    if TargetExists("Neutral"):
        TargetTileRelative("self", 1, False)
        Pause(6000)
    else:
        Pause(500) # Avoid spinning


def Main():
    check = Enemies(UserOptions.Flagged_notorieties)
    
    while not Dead():
        if TargetExists("Any"):
            HeadMsg("Detect skipped (cursor)")
            Pause(1000) # No reason to spin CPU
            continue

        if War("self"):
            check.refresh(UserOptions.Enemy_detection_range)
            
            target = check.current_target()
            if target:
                HeadMsg("Detect skipped (enemy)")
                Pause(1000) # No reason to spin CPU
                continue
        
            # No enemies nearby
            HeadMsg("No nearby enemies. Disabling war mode.")
            WarMode("off") # Disable war mode
        
        DetectHidden()


# Execute Main
Main()