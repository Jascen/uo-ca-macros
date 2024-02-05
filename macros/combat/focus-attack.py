"""
Name: Focus Attack Spammer
Description: Used to keep the Focus Attack ability active
Author: Tsai (Ultima Adventures)
Version: v1.0
"""

while not Dead():
    ClearJournal()
    Cast("Focus Attack")
    Pause(1000)

    if InJournal("prepare to focus"):
        while not Dead():
            if InJournal("You focus all"): break
                
            Pause(1000)