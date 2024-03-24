from Assistant import Engine

max = None
max = 40

def CheckItemCount():
    for property in Engine.Player.Backpack.Properties:
        #SysMessage("[debug]:property: " + property.Text)
        if property.Text.startswith("Contents"): # Contents: #min/#max items, #min/max stones
            #for arg in property.Arguments: SysMessage("[debug]:argument: " + arg)
            args = property.Arguments
            return int(args[0]) < int(args[1]) # Current/Max
    return False

i = 0
while CheckItemCount():
    ReplyGump(0x54f555df, 5)
    if not WaitForGump(0x54f555df, 5000): break
    if max == None: continue
    
    i = i + 1
    if max <= i: break