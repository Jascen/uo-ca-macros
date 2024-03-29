"""
Name: BOD Assistant
Description: Used to automate monotonous parts of completing Bulk Order Deeds
Author: Tsai (Ultima Adventures)
Version: v0.4
"""

from services.bodassistant import BodAssistant


def Main():
    assistant = BodAssistant()
    assistant.Run()


# Execute Main()
#Logger.DEBUG = True
#Logger.TRACE = True
Main()