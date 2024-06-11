from ClassicAssist.Data.Macros.Commands.MainCommands import SysMessage
from ClassicAssist.Data.Macros.Commands.GumpCommands import ReplyGump, WaitForGump, GumpExists
from ClassicAssist.Data.Macros.Commands.MainCommands import Pause
from ClassicAssist.Data.Macros.Commands.ObjectCommands import FindType, UseObject
from ClassicAssist.Data.Macros.Commands.TargetCommands import WaitForTarget, Target

from entities.craftmenuitem import Scissors, Tongs
from diagnostic.logger import Logger


class Salvager:
    smith_gump_id = 0x38920abd

    @classmethod
    def Smelt(cls, item):
        Logger.Debug("In Salvager.Smelt")

        if not FindType(Tongs.graphic, -1, "backpack"): 
            Logger.Error("Failed to salvage. Could not find Tongs.")
            return

        if not GumpExists(cls.smith_gump_id):
            UseObject("found")
            # Pause(750)
            if not WaitForGump(cls.smith_gump_id, 1000):
                Logger.Error("Failed to salvage. Could not open smith gump.")
                return

        ReplyGump(Salvager.smith_gump_id, 14) # Smelt
        if not WaitForTarget(5000):
            Logger.Error("Failed to salvage. Could not open smith gump.")
            return

        Target(item)
        Pause(1000)


    @staticmethod
    def Cut(item):
        Logger.Debug("In Salvager.Cut")
        if not FindType(Scissors.graphic, -1, "backpack"): 
            SysMessage("Failed to salvage. Could not find Scissors.")
            return

        UseObject("found")
        if not WaitForTarget(5000): return

        Target(item)
        Pause(1000)