from ClassicAssist.Data.Macros.Commands.MainCommands import SysMessage
from diagnostic.color import Color

class Logger:
    DEBUG = False
    TRACE = False

    TraceColor = Color.LightPink
    DebugColor = Color.LightPurple
    InfoColor = Color.Orange
    ErrorColor = Color.Red

    @classmethod
    def Trace(cls, message):
        if not Logger.TRACE: return
        SysMessage("[trace]: " + message, cls.TraceColor)

    @classmethod
    def Debug(cls, message):
        if not Logger.DEBUG: return
        SysMessage("[debug]: " + message, cls.DebugColor)

    @classmethod
    def Error(cls, message):
        SysMessage("[error]: " + message, cls.ErrorColor)

    @classmethod
    def Log(cls, message):
        SysMessage(message, cls.InfoColor)