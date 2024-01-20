from ClassicAssist.Data.Macros.Commands.MobileCommands import Hits, MaxHits, Poisoned


class HealthUtils:
    @classmethod
    def Poisoned(cls):
        """Returns `True` if the Player is poisoned"""
        return Poisoned("self")


    @classmethod
    def Damaged(cls, delta = 10):
        """Returns `True` if the Player is missing health"""
        return delta < MaxHits("self") - Hits("self")


    @classmethod
    def Healthy(cls, health_delta = 10):
        """Returns if the Player is poisoned or missing health"""
        return not cls.Poisoned() and not cls.Damaged(health_delta)