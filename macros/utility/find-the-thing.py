"""
Name: Find The Thing
Description: Temporarily points to the XY location of a thing (that you specify). Also logs additional location details.
Author: Tsai (Ultima Adventures)
Version: v1.0
"""

from Assistant import Engine
from ClassicAssist.UO import UOMath


### FILL OUT THIS METHOD ###
def find_the_thing():
    FindType(0x1081, -1, "backpack") # In your backpack
    #FindType(0x1081, 3) # On the ground

    # You must return an Alias or Serial!
    return "found"
### FILL OUT THIS METHOD ###


def point_to_thing(alias_or_serial):
    serial = alias_or_serial
    if not serial:
        print("Please provide an Alias or Serial")
        return
    
    if not isinstance(serial, int): serial = GetAlias(serial)

    item = Engine.Items.GetItem(serial)
    if not item:
        print("Failed to find an item by Serial ({})".format(serial))
        return
    
    print("Found item:")
    print(item)
    
    # If it's in a Container, get the Container
    if item.Owner:
        if UOMath.IsMobile(item.Owner):
            item = Engine.Mobiles.GetMobile(item.Owner)
            print("The item is on a Mobile")
            print(item)
        else:
            item = Engine.Items.GetItem(item.Owner)
            print("The item is in a Container")
            print(item)
            
    if item.RootOwner:
        if UOMath.IsMobile(item.RootOwner):
            item = Engine.Mobiles.GetMobile(item.RootOwner)
            print("The item is on a Mobile")
            print(item)
        else:
            item = Engine.Items.GetItem(item.RootOwner)
            print("The item is in a Container")
            print(item)
    
    # add pointer
    DisplayQuestPointer(item.X, item.Y, True)
    
    Pause(2000)
    
    # remove pointer
    DisplayQuestPointer(item.X, item.Y, False)


thing_alias_or_serial = find_the_thing()
point_to_thing(thing_alias_or_serial)