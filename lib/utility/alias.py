from Assistant import Engine
from ClassicAssist.UO import UOMath
from ClassicAssist.Data.Macros.Commands.AliasCommands import FindAlias, GetAlias, PromptMacroAlias, SetMacroAlias


class AliasUtils:
    @classmethod
    def CreateCharacterAlias(cls, alias, force = False):
        """Returns an alias that is pre-pended with the character name"""
        name = Engine.Player.Name.strip() # Sometimes there's a leading/trailing space
        if not force and alias.startswith(name): return alias # Assume it was already formatted

        return "{}-{}".format(name, alias)


    @classmethod
    def Ensure(cls, alias, prepend = True):
        """Searches for the `alias` and prompts if it is not found"""
        if prepend: alias = cls.CreateCharacterAlias(alias)
        if not FindAlias(alias): return cls.Prompt(alias, False)

        return alias


    @classmethod
    def EnsureContainer(cls, alias, prepend = True):
        """Searches for the `alias` and prompts if it is not found or it is a mobile"""
        if prepend: alias = cls.CreateCharacterAlias(alias)
        if FindAlias(alias):
            backpack = cls.GetBackpackSerial(alias)
            if backpack != None: SetMacroAlias(alias, backpack)
            return alias

        return cls.PromptContainer(alias, False)


    @classmethod
    def Prompt(cls, alias, prepend = True):
        """Prompts the user to set a value for the alias"""
        if prepend: alias = cls.CreateCharacterAlias(alias)
        PromptMacroAlias(alias)

        return alias


    @classmethod
    def PromptContainer(cls, alias, prepend = True):
        """Prompts the user for the target and attempts to set the alias value to the mobile's Backpack"""
        if prepend: alias = cls.CreateCharacterAlias(alias)
        PromptMacroAlias(alias)

        backpack = cls.GetBackpackSerial(alias)
        if backpack != None:
            SetMacroAlias(alias, backpack)

        return alias


    @classmethod
    def IsMobile(cls, alias):
        """Returns `True` if the serial of the alias is in the range for Mobiles"""
        return UOMath.IsMobile(alias)


    @classmethod
    def GetBackpackSerial(cls, alias):
        """Attempts to return the Backpack of the mobile"""
        serial = GetAlias(alias)
        if cls.IsMobile(serial):
            mobile = Engine.Mobiles.GetMobile(serial)
            if mobile and mobile.Backpack: return mobile.Backpack # Set the backpack if it exists
        # TODO: If it's not a Container ... good luck. Tough determining if it's a Container
        
        return None