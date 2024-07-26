from ClassicAssist.Data.Macros.Commands.EntityCommands import DirectionTo, Distance
from ClassicAssist.Data.Macros.Commands.MainCommands import Pause
from ClassicAssist.Data.Macros.Commands.MovementCommands import Run


class Movement:
    @staticmethod
    def MoveTo(serial, stop_distance = 2, max_attempts = 50):
        i = 0
        while Distance(serial) > stop_distance and i < max_attempts:
            Run(DirectionTo(serial))
            Pause(250)
            i += 1
        
        return Distance(serial) <= stop_distance