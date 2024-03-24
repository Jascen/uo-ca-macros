# Name: Smith Bod Filler
# Description: This will fill all BODs from a Source BOD Book.
# Author: raveX
# Era: Any
# Servers: ServUO and RunUO tested

from _models import CraftableItem
from Assistant import Engine

# ****************************************
# To turn off/on the ingame help prompts *
# ****************************************
DEBUG = True
FORCE_PROMPT_ALIAS = False
# ****************************************
SetQuietMode(not(DEBUG))
# ****************************************
#                  GLOBALS                
# ****************************************
craftMalePlatemailArmor = False
stopOnOutOfResource = False

textColor = 43
errorTextColor = 33
debugTextColor = 16

# ****PAUSES*****
shortPause = 500
mediumPause = 1000
longPause = 1500
gumpTimeout = 5000
targetTimeout = 5000

# *****GUMPS*****
smithGump  = 0x38920abd # TODO
tinkerGump  = 0x38920abd
BODBookGump = 0x54f555df
smithSmeltResponse = 14
smithMaterialResponse = 7
smithIronResponse = 6
smithDullCopperResponse = 13
smithShadowIronResponse = 20
smithCopperResponse = 27
smithBronzeResponse = 34
smithGoldenResponse = 41
smithAgapiteResponse = 48
smithVeriteResponse = 55
smithValoriteResponse = 62

# *****BOD*******

# ****************************************
PromptAlias("smith bod source")
if FORCE_PROMPT_ALIAS or not FindAlias("smith bod destination"): PromptMacroAlias("smith bod destination")      
if FORCE_PROMPT_ALIAS or not FindAlias("smith uncompletable bod book"): PromptMacroAlias("smith uncompletable bod book")
# PromptAlias("smith uncompletable bod book")
if FORCE_PROMPT_ALIAS or not FindAlias("smith restock container"): PromptMacroAlias("smith restock container")
if FORCE_PROMPT_ALIAS or not FindAlias("smith bod trash"): PromptMacroAlias("smith bod trash")


# *************************
# ******  MATERIALS  ******
# *************************     
class Material:
    outOfIron   = False
    outOfDullCopper = False
    outOfShadowIron = False
    outOfCopper = False
    outOfBronze = False
    outOfGolden = False
    outOfAgapite = False
    outOfVerite = False
    outOfValorite = False

    def __init__(self, graphic, name, hue, minPackAmt, restockAmt):
        self.graphic = graphic
        self.name = name
        self.hue = hue
        self.minPackAmt = minPackAmt
        self.restockAmt = restockAmt


    def __str__(self):
        return self.name


    @classmethod
    def SetMaterialOut(cls, material):
        if DEBUG: SysMessage("[DEBUG]:In Material.SetMaterialOut", debugTextColor)
        if material == "iron": cls.outOfIron = True
        elif material == "dull copper": cls.outOfDullCopper = True
        elif material == "shadow": cls.outOfShadowIron = True
        elif material == "copper": cls.outOfCopper = True
        elif material == "bronze": cls.outOfBronze = True
        elif material == "golden": cls.outOfGolden = True
        elif material == "agapite": cls.outOfAgapite = True
        elif material == "verite": cls.outOfVerite = True
        elif material == "valorite": cls.outOfValorite = True


# *************************
# FORMAT: Material(graphic, name, hue, minPackAmt, restockAmt)
# *************************
Ingots  = Material(0x1bf2, "ingots", 0, 2, 50)
Iron  = Material(0x1bf2, "iron", 0, 50, 300)
DullCopper  = Material(0x1bf2, "dull copper", 2741, 50, 300)
ShadowIron  = Material(0x1bf2, "shadow", 2739, 50, 300)
Copper  = Material(0x1bf2, "copper", 2840, 50, 300)
Bronze  = Material(0x1bf2, "bronze", 2236, 50, 300)
Golden  = Material(0x1bf2, "golden", 2458, 50, 300)
Agapite  = Material(0x1bf2, "agapite", 2794, 50, 300)
Verite  = Material(0x1bf2, "verite", 2141, 50, 300)
Valorite  = Material(0x1bf2, "valorite", 2397, 50, 300)


# *************************
# ****** CRAFT ITEMS ******
# *************************
class CraftableItem2:
    def __init__(self, graphic, gumpResponse1, gumpResponse2, name):
        self.graphic = graphic
        self.gumpResponse1 = gumpResponse1
        self.gumpResponse2 = gumpResponse2
        self.name = name
        self.defaultHue = 0
        
    def __str__(self):
        return self.name


# *************************
# For your server, YOUR GUMP RESPONSES MAY BE DIFFERENT than those listed here.
# You can easily determine what they should be by creating a test macro,
# record crafting each item, and replacing the values below.  The itemGraphics should
# not need to change (unless you are on a very custom shard)
# *************************
# FORMAT: CraftableItem(graphic, gumpResponse1, gumpResponse2, name)
# *************************
# *****Tools******
TinkerTool          = CraftableItem(0x1eb8, 8, 23, "tinker tool")
Tongs               = CraftableItem(0xfbb, 8, 114, "tongs")
## ***** Chain/Ring/Banded *****
ChainmailCoif        = CraftableItem(0x13bb, 1, 2, "chainmail coif") # TODO: Verify
ChainmailLeggings    = CraftableItem(0x13be, 1, 9, "chainmail leggings")
ChainmailTunic       = CraftableItem(0x13bf, 1, 16, "chainmail tunic")
RingmailGloves       = CraftableItem(0x13eb, 1, 23, "ringmail gloves")
RingmailLeggings     = CraftableItem(0x13f0, 1, 30, "ringmail leggings")
RingmailSleeves      = CraftableItem(0x13ee, 1, 37, "ringmail sleeves")
RingmailTunic        = CraftableItem(0x13ec, 1, 44, "ringmail tunic")
## ***** Platemail *****
PlatemailArms        = CraftableItem(0x304, 8, 2, "platemail arms") # TODO: Verify
PlatemailGloves      = CraftableItem(0x1414, 8, 9, "platemail gloves") # TODO: Verify
PlatemailGorget      = CraftableItem(0x1413, 8, 16, "platemail gorget") # TODO: Verify
PlatemailLeggings    = CraftableItem(0x1411, 8, 23, "platemail legs") # TODO: Verify
PlatemailTunic       = CraftableItem(0x1415, 8, 37, "platemail tunic") # TODO: Verify
PlatemailTunicFemale = CraftableItem(0x1c04, 8, 44, "female plate") # TODO: Verify
## ***** Royal Armor *****
## ***** Scalemail *****
## ***** Helmets *****
Bascinet             = CraftableItem(0x140c, 29, 2, "bascinet")
CloseHelmet          = CraftableItem(0x1408, 29, 9, "close helmet")
Helmet               = CraftableItem(0x140a, 29, 16, "helmet")
NorseHelm            = CraftableItem(0x140e, 29, 23, "norse helm")
PlateHelm            = CraftableItem(0x1412, 29, 30, "plate helm")
## ***** Shields *****
Buckler              = CraftableItem(0x1b73, 36, 2, "buckler")
RoundShield          = CraftableItem(0x1b72, 36, 9, "bronze shield") # TODO: Verify
HeaterShield         = CraftableItem(0x1b76, 36, 16, "heater shield")
MetalShield          = CraftableItem(0x1b7b, 36, 23, "metal shield")
MetalKiteShield      = CraftableItem(0x1b74, 36, 30, "metal kite shield")
TearKiteShield       = CraftableItem(0x1b79, 36, 37, "tear kite shield")
ChaosShield          = CraftableItem(0x1bc3, 36, 93, "chaos shield") # TODO: Verify
OrderShield          = CraftableItem(0x1bc4, 36, 100, "order shield") # TODO: Verify
## ***** Bladed *****
BarbarianSword       = CraftableItem(0x13b9, 43, 16, "viking sword")
Broadsword           = CraftableItem(0xf5e, 43, 23, "broadsword")
CrescentBlade        = CraftableItem(0x26c1, 43, 30, "crescent blade") # TODO: Verify
Cutlass              = CraftableItem(0x1441, 43, 37, "cutlass")
Dagger               = CraftableItem(0xf52, 43, 44, "dagger")
Katana               = CraftableItem(0x13ff, 43, 58, "katana")
Kryss                = CraftableItem(0x1401, 43, 65, "kryss")
Longsword            = CraftableItem(0xf61, 43, 72, "longsword")
Scimitar             = CraftableItem(0x13b6, 43, 100, "scimitar")
## ***** Axes *****
Axe                  = CraftableItem(0xf49, 50, 16, "axe")
BattleAxe            = CraftableItem(0xf47, 50, 23, "battle axe")
DoubleAxe            = CraftableItem(0xf4b, 50, 30, "double axe")
ExecutionerAxe       = CraftableItem(0xf45, 50, 37, "executioner"s axe")
LargeBattleAxe       = CraftableItem(0x13fb, 50, 44, "large battle axe")
TwoHandedAxe         = CraftableItem(0x1443, 50, 51, "two handed axe")
WarAxe               = CraftableItem(0x13b0, 50, 58, "war axe")
## ***** Polearms *****
Bardiche             = CraftableItem(0xf4d, 57, 2, "bardiche")
BladedStaff          = CraftableItem(0x26bd, 57, 9, "bladed staff") # TODO: Verify
DoubleBladedStaff    = CraftableItem(0x26bf, 57, 16, "double bladed staff") # TODO: Verify
Halberd              = CraftableItem(0x143e, 57, 23, "halberd")
Lance                = CraftableItem(0x26c0, 57, 37, "lance") # TODO: Verify
Pike                 = CraftableItem(0x26be, 57, 44, "pike") # TODO: Verify ?????
ShortSpear           = CraftableItem(0x1403, 57, 51, "short spear")
Scythe               = CraftableItem(0x26ba, 57, 58, "scythe") # TODO: Verify
Spear                = CraftableItem(0xf62, 57, 65, "spear")
Warfork              = CraftableItem(0x1405, 57, 72, "war fork")
## ***** Bashing *****
HammerPick       = CraftableItem(0x143d, 64, 9, "hammer pick")
Mace             = CraftableItem(0xf5c, 64, 16, "mace")
Maul             = CraftableItem(0x143b, 64, 23, "maul")
Scepter          = CraftableItem(0x26bc, 64, 30, "scepter") # TODO: Verify ???
WarMace          = CraftableItem(0x1407, 64, 37, "war mace")
WarHammer        = CraftableItem(0x1439, 64, 44, "war hammer")


class BOD:
    Gump = 0x5afbd742 # TODO: Verify
    GumpCombineResponse = 2 # TODO: Verify
    Graphic = 0x2258 # TODO: Verify
    SmithHue = 1102
    MetalTypes = ["dull", "shadow", "copper", "bronze", "gold", "agapite", "verite", "valorite"]


    def __init__(self, id):
        self.id = id
        self.item = self.GetItem()
        self.material = self.GetMaterial()
        self.isCompletable = self.CheckIfCompletable()
        self.amount = self.GetAmount()
        self.completed = self.GetCompleted()


    def OpenGump(self):
        if DEBUG: SysMessage("[debug]:In BOD.OpenGump", debugTextColor)
        UseObject(self.id)
        WaitForGump(BOD.Gump, gumpTimeout)
        if not GumpExists(BOD.Gump):
            SysMessage("Looking for BOD Gump and not found", errorTextColor)
            return False
        return True


    def GetItem(self):
        if DEBUG: SysMessage("[debug]:In BOD.GetItem", debugTextColor)

        items = [
            ChainmailCoif, ChainmailLeggings, ChainmailTunic, 
            RingmailGloves, RingmailLeggings, RingmailSleeves, RingmailTunic, 
            PlatemailArms, PlatemailGloves, PlatemailGorget, PlatemailLeggings, PlatemailTunic, PlateHelm, 
            PlatemailTunicFemale, 
            Bascinet, CloseHelmet, Helmet, NorseHelm, 
            Buckler, RoundShield, HeaterShield, MetalKiteShield, TearKiteShield, ChaosShield, OrderShield, MetalShield, 
            BarbarianSword, Broadsword, CrescentBlade, Cutlass, Dagger, Katana, Kryss, Longsword, Scimitar, 
            LargeBattleAxe, BattleAxe, DoubleAxe, ExecutionerAxe, TwoHandedAxe, WarAxe, Axe, 
            Bardiche, BladedStaff, DoubleBladedStaff, Halberd, Lance, Pike, ShortSpear, Scythe, Spear, Warfork, 
            HammerPick, WarMace, Mace, Maul, Scepter, WarHammer, 
        ]
        
        if not self.OpenGump(): return None
        for i in items:
            if InGump(BOD.Gump, i.name):
                return i

        SysMessage("Did not find a supported item in the BOD Gump", errorTextColor)
        self.isCompletable = False
        return None


    def GetMaterial(self):
        if DEBUG: SysMessage("[debug]:In BOD.GetMaterials", debugTextColor)

        if not self.OpenGump(): return None

        materialType = "iron"
        for type in BOD.MetalTypes:
            if InGump(BOD.Gump, type):
                materialType = type

        if DEBUG: SysMessage("[debug]:Material type is: " + materialType, debugTextColor)

        if materialType == "iron": return Iron
        elif materialType == "dull copper": return DullCopper
        elif materialType == "shadow": return ShadowIron
        elif materialType == "copper": return Copper
        elif materialType == "bronze": return Bronze
        elif materialType == "golden": return Golden
        elif materialType == "agapite": return Agapite
        elif materialType == "verite": return Verite
        elif materialType == "valorite": return Valorite

        # default to Iron
        return Iron


    def CheckIfCompletable(self):
        if DEBUG: SysMessage("[debug]:In BOD.CheckIfCompletable", debugTextColor)
        completable = True
        if self.material == Iron: completable = not(Material.outOfIron)
        elif self.material == DullCopper: completable = not(Material.outOfDullCopper)
        elif self.material == ShadowIron: completable = not(Material.outOfShadowIron)
        elif self.material == Copper: completable = not(Material.outOfCopper)
        elif self.material == Bronze: completable = not(Material.outOfBronze)
        elif self.material == Golden: completable = not(Material.outOfGolden)
        elif self.material == Agapite: completable = not(Material.outOfAgapite)
        elif self.material == Verite: completable = not(Material.outOfVerite)
        elif self.material == Valorite: completable = not(Material.outOfValorite)

        if (self.item == PlateHelm or
            self.item == PlatemailGorget or 
            self.item == PlatemailGloves or
            self.item == PlatemailLeggings or
            self.item == PlatemailArms or
            self.item == PlatemailTunic):
            if not craftMalePlatemailArmor:
                SysMessage("Macro set to not make Male Platemail Armor", textColor)
            completable = completable and craftMalePlatemailArmor
            
        if DEBUG: SysMessage("[debug]:In BOD.CheckIfCompletable: " + str(completable), debugTextColor)
        return completable


    def GetAmount(self):
        if DEBUG: SysMessage("[debug]:In BOD.GetAmount", debugTextColor)
        amount = 0
        amount = PropertyValue[int](self.id, "Amount to make:")
        return amount


    def GetCompleted(self):
        if DEBUG: SysMessage("[debug]:In BOD.GetCompleted", debugTextColor)
        completed = -1
        # if we were given an invalid BOD, it would have been set to incompletable
        # in earlier calls, a non-valid BOD would cause this to crash
        if self.isCompletable:
            bod = Engine.Items.GetItem(self.id)
            for property in bod.Properties:
                if DEBUG: SysMessage("[debug]:property: " + property.Text, debugTextColor)
                if self.item.name in property.Text:
                    for arg in property.Arguments:
                        if DEBUG: SysMessage("[debug]:argument: " + arg, debugTextColor)
                    completed = int(property.Arguments[1])

        return completed


    def SetCombineOption(self):
        if not GumpExists(BOD.Gump):
            UseObject(self.id)
            WaitForGump(BODGump, gumpTimeout)

        # Select the "combine" option to target items as they are made
        ReplyGump(BOD.Gump, BOD.GumpCombineResponse)
        WaitForGump(BOD.Gump, gumpTimeout)
        WaitForTarget(targetTimeout)


# *************************
# ******  FUNCTIONS  ******
# *************************

def GetRestockContainer():
    if DEBUG: SysMessage("[debug]:In GetRestockContainer", debugTextColor)
    container = GetAlias("smith restock container")
    if container == 0:
        SysMessage("Looking for "smith restock container" alias and not found", errorTextColor)
        CancelTarget()
        Stop()
    elif not InRange(container, 2):
        SysMessage("Restock container is no longer in range", errorTextColor)
        CancelTarget()
        Stop()
    else: return container


def UnloadMaterials():
    if DEBUG: SysMessage("[debug]:In UnloadMaterials", debugTextColor)
    materials = [Iron, DullCopper, ShadowIron, Copper, Bronze, Golden, Agapite, Verite, Valorite]
    container = GetRestockContainer()
    for x in materials:
        MoveType(x.graphic, "backpack", container, -1, -1, -1)


def RefillMaterial(material):
    if DEBUG: SysMessage("[debug]:In RefillMaterial", debugTextColor)
    if material == 0 or material == None:
        SysMessage("Trying to refill materials and no valid type provided", errorTextColor)
        return

    container = GetRestockContainer()
    if CountType(material.graphic, "backpack", material.hue) < material.minPackAmt:
        if CountType(material.graphic, container, material.hue) == 0:
            msg = "OUT OF " + material.name + "!"
            SysMessage(msg.upper(), errorTextColor)
            if stopOnOutOfResource:
                CancelTarget()
                Stop()
            else:
                if material == Iron: Material.SetMaterialOut("iron")
                elif material == DullCopper: Material.SetMaterialOut("dull copper")
                elif material == ShadowIron: Material.SetMaterialOut("shadow")
                elif material == Copper: Material.SetMaterialOut("copper")
                elif material == Bronze: Material.SetMaterialOut("bronze")
                elif material == Golden: Material.SetMaterialOut("golden")
                elif material == Agapite: Material.SetMaterialOut("agapite")
                elif material == Verite: Material.SetMaterialOut("verite")
                elif material == Valorite: Material.SetMaterialOut("valorite")
        else:
            Pause(shortPause)
            MoveType(material.graphic, container, "backpack", -1, -1, -1, material.hue, material.restockAmt)
            Pause(longPause)


def CheckMaterials(bod):
    if DEBUG: SysMessage("[debug]:In CheckMaterials", debugTextColor)
    
    if bod == 0 or bod == None:
        SysMessage("Looking for required BOD material but no valid bod given", errorTextColor)
        return
    if DEBUG: SysMessage("[debug]:Material type is: " + str(bod.material), debugTextColor)
    
    RefillMaterial(bod.material)


def SetMetalType(bod):
    if DEBUG: SysMessage("[debug]:In SetMetalType", debugTextColor)
    
    if bod == 0 or bod == None:
        SysMessage("Trying to set metal type but no current BOD", errorTextColor)
        return

    tongs = GetTongs()
    UseObject(tongs)
    WaitForGump(smithGump, gumpTimeout)
    ReplyGump(smithGump, smithMaterialResponse)
    WaitForGump(smithGump, gumpTimeout)
    if bod.material == Iron: ReplyGump(smithGump, smithIronResponse)
    elif bod.material == DullCopper: ReplyGump(smithGump, smithDullCopperResponse)
    elif bod.material == ShadowIron: ReplyGump(smithGump, smithShadowIronResponse)
    elif bod.material == Copper: ReplyGump(smithGump, smithCopperResponse)
    elif bod.material == Bronze: ReplyGump(smithGump, smithBronzeResponse)
    elif bod.material == Golden: ReplyGump(smithGump, smithGoldenResponse)
    elif bod.material == Agapite: ReplyGump(smithGump, smithAgapiteResponse)
    elif bod.material == Verite: ReplyGump(smithGump, smithVeriteResponse)
    elif bod.material == Valorite: ReplyGump(smithGump, smithValoriteResponse)


def CraftTinkerItem(item):
    if DEBUG: SysMessage("[debug]:In CraftTinkerItem", debugTextColor)
    # Careful of endless loop if we are crafting a tinker tool
    toolCheck = True
    if item.graphic == TinkerTool.graphic:
        toolCheck = False

    if toolCheck:   
        if CountType(TinkerTool.graphic, "backpack", TinkerTool.defaultHue) < 2:
            CraftTinkerItem(TinkerTool)

    RefillMaterial(Ingots)
    UseType(TinkerTool.graphic)
    WaitForGump(tinkerGump, gumpTimeout)
    ReplyGump(tinkerGump, item.gumpResponse1)
    WaitForGump(tinkerGump, gumpTimeout)
    ReplyGump(tinkerGump, item.gumpResponse2)
    Pause(longPause)


def GetTongs():
    if DEBUG: SysMessage("[debug]:In GetTongs", debugTextColor)
    while not FindType(Tongs.graphic, 1, "backpack", Tongs.defaultHue):
        container = GetRestockContainer()
        if not FindType(Tongs.graphic, 2, container, Tongs.defaultHue):
            CraftTinkerItem(Tongs)
        else:
            MoveType(Tongs.graphic, container, "backpack", -1, -1, -1, Tongs.defaultHue)
            Pause(longPause)
    if FindType(Tongs.graphic, 1, "backpack", Tongs.defaultHue):        
        return GetAlias("found")
    else:
        SysMessage("ERROR GETTING TONGS", errorTextColor)
        Stop()


def CraftSmithItem(item):
    if DEBUG: SysMessage("[debug]:In CraftSmithItem", debugTextColor)
    tongs = GetTongs()
    UseObject(tongs)
    WaitForGump(smithGump, gumpTimeout)
    ReplyGump(smithGump, item.gumpResponse1)
    WaitForGump(smithGump, gumpTimeout)
    ReplyGump(smithGump, item.gumpResponse2)
    WaitForGump(smithGump, gumpTimeout)
    Pause(shortPause)
    while FindType(item.graphic, 1, "backpack"):
        craftedItem = GetAlias("found")
        Target(craftedItem)
        WaitForTarget(2000)
        if not TargetExists() and InJournal("must be exceptional"):
            # Smelt
            if not GumpExists(smithGump):
                tongs = GetTongs()
                UseObject(tongs)
            ReplyGump(smithGump, smithSmeltResponse)
            WaitForTarget(targetTimeout)
            Target(craftedItem)
            Pause(300)
            
            # Bring back the target cursor
            Pause(shortPause)
            ReplyGump(BOD.Gump, BOD.GumpCombineResponse)
            WaitForGump(BOD.Gump, gumpTimeout)
            WaitForTarget(targetTimeout)
            ClearJournal()


def BookDeedsRemaining():
    if DEBUG:SysMessage("[debug]:In BookDeedsRemaining", debugTextColor)
    # Close any existing gump (could be another book)
    ReplyGump(BODBookGump, 0)
    
    bodBook = GetAlias("smith bod source")
    if not bodBook == 0:
        # I want to handle a book with many deeds in it but
        # with the filter have none to pull from book therefore
        # cannot use the book property for "Deeds Remaining:"
        ClearJournal()
        Pause(shortPause)
        UseObject(bodBook)  
        if InJournal("The book is empty"):
            return False
        else:
            WaitForGump(BODBookGump, 2000)
            Pause(mediumPause)
            if GumpExists(BODBookGump) and InGump(BODBookGump, "Small"):
                return True
    else:
        SysMessage("Did not find the "smith bod source" alias", errorTextColor)

    return False


# ******************************
# *****      MAIN          *****
# ******************************
def Main():
    while BookDeedsRemaining() or FindType(BOD.Graphic, 1, "backpack", BOD.SmithHue):
        # Search for BOD to Fill
        if FindType(BOD.Graphic, 1, "backpack", BOD.SmithHue):
            bod = BOD(GetAlias("found"))
            if bod.isCompletable:
                if DEBUG: SysMessage("[debug]:PASSED COMPLETED CHECK: " + str(bod.isCompletable), debugTextColor)
                bod.SetCombineOption()
                SetMetalType(bod)
                Pause(600)

                while (TargetExists() and bod.item != None and bod.isCompletable):
                    CheckMaterials(bod)
                    CraftSmithItem(bod.item)
                    bod.isCompletable = bod.CheckIfCompletable()
                    if DEBUG: 
                        SysMessage("[debug]:BOD completable: " + str(bod.isCompletable), debugTextColor)
                        SysMessage("[debug]:Out of Iron: " + str(Material.outOfIron), debugTextColor)
                        SysMessage("[debug]:Out of Dull Copper: " + str(Material.outOfDullCopper), debugTextColor)
                        SysMessage("[debug]:Out of Shadow Iron: " + str(Material.outOfShadowIron), debugTextColor)
                        SysMessage("[debug]:Out of Copper: " + str(Material.outOfCopper), debugTextColor)
                        SysMessage("[debug]:Out of Bronze: " + str(Material.outOfBronze), debugTextColor)
                        SysMessage("[debug]:Out of Golden: " + str(Material.outOfGolden), debugTextColor)
                        SysMessage("[debug]:Out of Agapite: " + str(Material.outOfAgapite), debugTextColor)
                        SysMessage("[debug]:Out of Verite: " + str(Material.outOfVerite), debugTextColor)
                        SysMessage("[debug]:Out of Valorite: " + str(Material.outOfValorite), debugTextColor)

                if bod.completed == bod.amount or not TargetExists():
                    # BOD is complete, move to destination book
                    SysMessage("BOD is complete", textColor)
                    ReplyGump(BOD.Gump, 0) # Close
                    destination = GetAlias("smith bod destination")
                    Pause(mediumPause)
                    MoveItem(bod.id, destination)
                    bod = None
                    Pause(shortPause)
                    UnloadMaterials()
                    Pause(shortPause)
            else:
                if DEBUG: SysMessage("[debug]:Moving deed to uncompletable book", debugTextColor)
                # Move to incompletable book
                SysMessage("NOT doing this BOD", textColor)
                uncompletableBook = GetAlias("smith uncompletable bod book")
                Pause(mediumPause)
                MoveItem(bod.id, uncompletableBook)
                Pause(shortPause)
                UnloadMaterials()
                Pause(shortPause)

        # Get A BOD out of the book
        else:
            ReplyGump(BODBookGump, 0) 
            SysMessage("Getting a new BOD", textColor)
            bodBook = GetAlias("smith bod source")
            UseObject(bodBook)
            WaitForGump(BODBookGump, gumpTimeout)
            ReplyGump(BODBookGump, 5)
            Pause(longPause)

    UnloadMaterials()
    # Close Gumps
    ReplyGump(BODBookGump, 0)
    ReplyGump(BOD.Gump, 0)
    ReplyGump(smithGump, 0)
    # End Macro
    SysMessage("NO BODS TO FILL", textColor)
    CancelTarget()
    Stop()


# ******************************
# ***** MACRO ENTRY POINT  *****
# ******************************
Main()