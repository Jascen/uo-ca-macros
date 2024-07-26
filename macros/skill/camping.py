"""
Name: Stat/Camping skill trainer
Description: Uses kindling until you get a Strength gain (changeable at the bottom)
Author: Tsai (Ultima Adventures)
"""

class UserOptions:
    kindling_container = "backpack" # Recommended 'bank' or 'backpack'

while not Dead():
    hits = MaxHits()
    mana = MaxMana()
    stam = MaxStam()

    # Wait 15 minutes until first executing
    Pause(15000)
    for x in range(15): Pause(60000)

    kindling_id = 0xde1

    while FindType(kindling_id , -1, UserOptions.kindling_container):
        UseObject("found")
        Pause(1000)

        if hits < MaxHits(): break # Stop after Str (hitpoints) gain
        # if stam < MaxStam(): break # Stop after Dex (stamina) gain
        # if mana < MaxMana(): break # Stop after Int (mana) gain
        # if hits < MaxHits() and mana < MaxMana() and stam < MaxStam(): break