"""
Name: Auto Bandy
Description: Bandage yourself or the pre-configured target ASAP
Author: Tsai (Ultima Adventures)
Version: v1.0
"""


cure_potion_id = 0x24ea # Graphic for Greater Cure Potion

class UserOptions:
    Target = "self" # Who to use bandages on
    Hitpoint_threshold = 0 # When below this number, apply bandages
    Pause_on_warmode = False # Do not heal when in warmode
    Drink_cure_on_poison = True # When targeting yourself, drink cure potions after applying bandages
    Drink_cure_healing_threshold_milliseconds = 500 # Wait until Bandage timer is under this amount of milliseconds before drinking the cure potion. A value of 0 will instantly drink.
    Healing_buff_packet_delay = 1000 # The amount of time to wait after healing


def Main():
    targeting_self = UserOptions.Target == "self"
    while not Dead():
        # Optional pause
        if UserOptions.Pause_on_warmode:
            while War("self"):
                SysMessage("War mode detected. Delaying bandages...")
                Pause(1000)
        
        # Bandage if necessary
        if Poisoned(UserOptions.Target) or UserOptions.Hitpoint_threshold < DiffHits(UserOptions.Target):
            # Try to Bandage
            if not BuffExists("Healing"):
                if targeting_self:
                    Msg("[bandself")
                else:
                    Msg("[bandother")
                    if not WaitForTarget(2000): continue

                    Target(UserOptions.Target)
                
                # Rudimentary delay in case the packet hasn't arrived yet
                Pause(UserOptions.Healing_buff_packet_delay)

        # Try to cure
        if Poisoned(UserOptions.Target) and targeting_self and UserOptions.Drink_cure_on_poison:
            # Cure instantly or when Healing duration is sufficiently low
            if UserOptions.Drink_cure_healing_threshold_milliseconds < 1 or (BuffExists("Healing") and BuffTime("Healing") < UserOptions.Drink_cure_healing_threshold_milliseconds):
                UseType(cure_potion_id)
                
        # Small delay to avoid spamming the CPU
        Pause(250)


# Execute Main
Main()