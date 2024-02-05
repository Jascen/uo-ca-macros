"""
Name: Lightning Strike Spammer
Description: Used to keep the Lightning Strike ability active
Author: Tsai (Ultima Adventures)
Version: v1.0
"""

while not Dead():
    ClearJournal()
    Cast("Lightning Strike")
    Pause(250)

    while BuffExists("Lightning Strike"):
        Pause(250)