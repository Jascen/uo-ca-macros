# Name: Tailor Bod Filler
# Description: This will fill all BODs from a Source BOD Book.
# Author: raveX
# Era: Any
# Servers: ServUO and RunUO tested

from craft.items import *
from Assistant import Engine

# ****************************************
# To turn off/on the ingame help prompts *
# ****************************************
UseHelp = False
DEBUG = False
# ****************************************
SetQuietMode(not(DEBUG))
# ****************************************
#                  GLOBALS                
# ****************************************
craftBoneArmor    = False
craftMaleStuddedArmor = False
stopOnOutOfResource = True

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
tailorGump  = 0x38920abd
tinkerGump  = 0x38920abd
BODBookGump = 0x54f555df
tailorMaterialResponse = 7
tailorLeatherResponse = 6
tailorSpinedResposne = 13
tailorHornedResponse = 20
tailorBarbedResponse = 27

# *****BOD*******

# ****************************************

msg = "Welcome to the Tailor BOD Filler macro.  This macro " \
      "will take BODs from a BOD book and fill them.  It " \
      "supports making any Tailor BOD, cloth, leather, bone, and " \
      "of any leather type.  Let's get started!"
if UseHelp: ConfirmPrompt(msg)

msg = "We will want to know what BOD book you want to pull BODs " \
      "out of to fill.\n\nBe sure to set the filter on the book to the " \
      "specific type of BODs you want to fill here. AT A MINIMUM, you will " \
      "want to ensure you have selected Tailoring and Small BODs."
      
# if not FindAlias('tailor bod source'):
    # if UseHelp: ConfirmPrompt(msg)
    # PromptAlias('tailor bod source')
PromptAlias('tailor bod source')

msg = "You will now need to select a different book to hold the completed " \
      "BODs you fill.  Make sure the book has plenty of room to hold all the " \
      "BODs." 
      
if not FindAlias('tailor bod destination'):
    if UseHelp: ConfirmPrompt(msg)
    PromptAlias('tailor bod destination')
    
msg = "This choice is a book for BODs that cannot be filled. " \
      "For instance, you may have run out of leather and " \
      "still have plenty of cloth in your restock chest. " \
      "The Macro could continue to complete the remaining cloth BODs, " \
      "but would stash all the incompletable leather BODs in this book."
      
if not FindAlias('tailor uncompletable bod book'):
    if UseHelp: ConfirmPrompt(msg)
    PromptAlias('tailor uncompletable bod book')
# PromptAlias('tailor uncompletable bod book')

msg = "Next, you need to select a container that will serve as your restock " \
      "target.  In this container, you will want plenty of materials, such as cut cloth, " \
      "leathers, and bone.  This all obviously depends on what BODs you are planning to fill " \
      "Additionally, if you are going to tinker sewing kits, have plenty of ingots in this " \
      "container as well. If you are not going to use tinkering, be sure to have scissors in " \
      "your pack (for non-exceptional items when exceptional is required) and lots of sewing kits in " \
      "there as well.  Material searches are set to a second level search."
      
if not FindAlias('tailor restock container'):
    if UseHelp: ConfirmPrompt(msg)
    PromptAlias('tailor restock container')


msg = "The next prompt is for a Trash container for failed Bone armor or Footwear attempts as they cannot be recycled."

if not FindAlias('tailor bod trash'):
    if UseHelp: ConfirmPrompt(msg)
    PromptAlias('tailor bod trash')
    
msg = "OK, now for a few tips.\n\nThere are some settings at the top of the macro that you can adjust.  These " \
      "include things like text colors for different messaging, length of pauses, whether or not to make Bone armor, etc."
      
if UseHelp: ConfirmPrompt(msg)

msg = "There is a debug mode that you can turn on (another setting at top) to provide verbose messaging.  This would be " \
      "useful to understand the flow of the method calls or help if you are modifying the script and are actually debugging"
      
if UseHelp: ConfirmPrompt(msg)

msg = "The amount of materials to pull into your pack is a setting on the material types found around lines 152-158. " \
      "You can adjust this as desired depending on how heavy your server makes these materials so you don't overfill your pack."

if UseHelp: ConfirmPrompt(msg)

msg = "You are all set! \n\nOne final note, if you prefer to not see these prompts " \
      "anymore, set the 'UseHelp' variable at the top of the macro to 'False'" \

if UseHelp: ConfirmPrompt(msg)

# *************************
# ******  MATERIALS  ******
# *************************     
class Material:
    outOfCloth   = False
    outOfLeather = False
    outOfSpined  = False
    outOfHorned  = False
    outOfBarbed  = False
    outOfBone    = False
    
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
        if material == "cloth": cls.outOfCloth = True
        elif material == "leather": cls.outOfLeather = True
        elif material == "spined": cls.outOfSpined = True
        elif material == "horned": cls.outOfHorned = True
        elif material == "barbed": cls.outOfBarbed = True
        elif material == "bone": cls.outOfBone = True


# *************************
# FYI - Cloth will be Cut Cloth only, but of any color unless you change the hue setting below
# *************************
# FORMAT: Material(graphic, name, hue, minPackAmt, restockAmt)
# *************************
Ingots  = Material(0x1bf2, "ingots", 0, 2, 50)
Cloth   = Material(0x1766, "cloth", -1, 30, 400)
Leather = Material(0x1081, "leather", 0, 30, 200)
Spined  = Material(0x1081, "spined leather", 2220, 30, 200)
Horned  = Material(0x1081, "horned leather", 2117, 30, 200)
Barbed  = Material(0x1081, "barbed leather", 2129, 30, 200)
Bone    = Material(0xf7e,  "bone", 0, 10, 100)


# *************************
# ****** CRAFT ITEMS ******
# *************************
class CraftableItem:
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


class BOD:
    Gump = 0x5afbd742
    GumpCombineResponse = 2
    Graphic = 0x2258
    TailorHue = 1155
    LeatherItems = ["shoes", "sandals", "boots", "leather", "studded", "bone"]
    LeatherTypes = ["spined", "horned", "barbed"]

    def __init__(self, id):
        self.id = id
        self.item = self.GetItem()
        self.material = self.GetMaterial()
        self.isBone = self.CheckIfBone()
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

        items = [Skullcap, Bandana, FloppyHat, WideBrimHat, TallStrawHat, StrawHat, WizardHat, Bonnet, FeatheredHat,
                TricornHat, JesterHat, Doublet, FancyShirt, Shirt, Surcoat, PlainDress, FancyDress, Cloak, Robe,
                JesterSuit, ShortPants, LongPants, Kilt, BodySash, HalfApron, FullApron, ThighBoots, Sandals, Shoes,
                Boots, LeatherGorget, LeatherCap, LeatherGloves, LeatherLeggings, LeatherSleeves, LeatherTunic, 
                StuddedGorget, StuddedGloves, StuddedLeggings, StuddedSleeves, StuddedTunic, LeatherShorts, 
                LeatherSkirt, LeatherBustier, StuddedBustier, FemaleLeatherArmor, StuddedArmor, BoneHelmet, BoneGloves,
                BoneLeggings, BoneArms, BoneArmor, Skirt, Tunic, Cap]
        
        if not self.OpenGump(): return None
        for i in items:
            if InGump(BOD.Gump, i.name):
                return i

        SysMessage("Did not find a supported item in the BOD Gump", errorTextColor)
        self.isCompletable = False
        return None


    def GetMaterial(self):
        if DEBUG: SysMessage("[debug]:In BOD.GetMaterials", debugTextColor)

        materialType = "cloth"
        if not self.OpenGump(): return None
        for text in BOD.LeatherItems:
            if InGump(BOD.Gump, text):
                materialType = "leather"
                for type in BOD.LeatherTypes:
                    if InGump(BOD.Gump, type):
                        materialType = type

        if DEBUG: SysMessage("[debug]:Material type is: " + materialType, debugTextColor)

        if materialType == "leather": return Leather
        elif materialType == "spined": return Spined
        elif materialType == "horned": return Horned
        elif materialType == "barbed": return Barbed

        # default to Cloth
        return Cloth


    def CheckIfBone(self):
        if DEBUG: SysMessage("[debug]:In BOD.CheckIfBone", debugTextColor)

        if not self.OpenGump(): 
            return False        
        return InGump(BOD.Gump, "bone")


    def CheckIfCompletable(self):
        if DEBUG: SysMessage("[debug]:In BOD.CheckIfCompletable", debugTextColor)
        completable = True
        if self.material == Cloth:
            completable = not(Material.outOfCloth)
        elif self.material == Leather:
            completable = not(Material.outOfLeather)
        elif self.material == Spined:
            completable = not(Material.outOfSpined)
        elif self.material == Horned:
            completable = not(Material.outOfHorned)
        elif self.material == Barbed:
            completable = not(Material.outOfBarbed)

        if self.isBone:
            if not craftBoneArmor:
                SysMessage("Macro set to not make Bone Armor", textColor)
            completable = completable and not(Material.outOfBone) and craftBoneArmor
            
        if (self.item == StuddedGorget or 
            self.item == StuddedGloves or
            self.item == StuddedLeggings or
            self.item == StuddedSleeves or
            self.item == StuddedTunic):
            if not craftMaleStuddedArmor:
                SysMessage("Macro set to not make Male Studded Armor", textColor)
            completable = completable and craftMaleStuddedArmor
            
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
    container = GetAlias('tailor restock container')
    if container == 0:
        SysMessage("Looking for 'tailor restock container' alias and not found", errorTextColor)
        CancelTarget()
        Stop()
    elif not InRange(container, 2):
        SysMessage("Restock container is no longer in range", errorTextColor)
        CancelTarget()
        Stop()
    else: return container

def UnloadMaterials(skipIngots):
    if DEBUG: SysMessage("[debug]:In UnloadMaterials", debugTextColor)
    materials = [Ingots, Cloth, Leather, Spined, Horned, Barbed, Bone]
    container = GetRestockContainer()
    for x in materials:
        if not (skipIngots and x == Ingots):
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
                if material == Cloth: Material.SetMaterialOut("cloth")
                elif material == Leather: Material.SetMaterialOut("leather")
                elif material == Spined: Material.SetMaterialOut("spined")
                elif material == Horned: Material.SetMaterialOut("horned")
                elif material == Barbed: Material.SetMaterialOut("barbed")
                elif material == Bone: Material.SetMaterialOut("bone")
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
    if bod.isBone: RefillMaterial(Bone)


def SetLeatherType(bod):
    if DEBUG: SysMessage("[debug]:In SetLeatherType", debugTextColor)
    
    if bod == 0 or bod == None:
        SysMessage("Trying to set leather type but no current BOD", errorTextColor)
        return

    if bod.material == Cloth: return

    kit = GetSewingKit()
    UseObject(kit)
    WaitForGump(tailorGump, gumpTimeout)
    ReplyGump(tailorGump, tailorMaterialResponse)
    WaitForGump(tailorGump, gumpTimeout)
    if bod.material == Leather: ReplyGump(tailorGump, tailorLeatherResponse)
    elif bod.material == Spined: ReplyGump(tailorGump, tailorSpinedResposne)
    elif bod.material == Horned: ReplyGump(tailorGump, tailorHornedResponse)
    elif bod.material == Barbed: ReplyGump(tailorGump, tailorBarbedResponse)


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


def GetScissors():
    if DEBUG: SysMessage("[debug]:In GetScissors", debugTextColor)
    while not FindType(Scissors.graphic, 1, "backpack"):
        CraftTinkerItem(Scissors)
    FindType(Scissors.graphic, 1, "backpack")
    return GetAlias("found")


def GetSewingKit():
    if DEBUG: SysMessage("[debug]:In GetSewingKit", debugTextColor)
    while not FindType(SewingKit.graphic, 1, "backpack", SewingKit.defaultHue):
        container = GetRestockContainer()
        if not FindType(SewingKit.graphic, 2, container, SewingKit.defaultHue):
            CraftTinkerItem(SewingKit)
        else:
            MoveType(SewingKit.graphic, container, "backpack", -1, -1, -1, SewingKit.defaultHue)
            Pause(longPause)
    if FindType(SewingKit.graphic, 1, "backpack", SewingKit.defaultHue):        
        return GetAlias("found")
    else:
        SysMessage("ERROR GETTING SEWING KIT", errorTextColor)
        Stop()


def CraftTailorItem(item):
    if DEBUG: SysMessage("[debug]:In CraftTailorItem", debugTextColor)
    kit = GetSewingKit()
    UseObject(kit)
    if not WaitForGump(tailorGump, gumpTimeout): return
    
    ReplyGump(tailorGump, item.gumpResponse1)
    if not WaitForGump(tailorGump, gumpTimeout): return

    ReplyGump(tailorGump, item.gumpResponse2)
    if not WaitForGump(tailorGump, gumpTimeout): return
    
    Pause(shortPause)
    while FindType(item.graphic, 1, "backpack"):
        craftedItem = GetAlias("found")
        Target(craftedItem)
        WaitForTarget(2000)
        if not TargetExists() and InJournal("must be exceptional"):
            myScissors = GetScissors()
            Pause(shortPause)
            UseObject(myScissors)
            WaitForTarget(targetTimeout)
            Target(craftedItem)
            Pause(300)
            if InJournal("Scissors cannot be used"):
                Pause(shortPause)
                MoveItem(craftedItem, GetAlias("tailor bod trash"))
                ClearJournal()
            # Bring back the target cursor
            Pause(shortPause)
            ReplyGump(BOD.Gump, BOD.GumpCombineResponse)
            WaitForGump(BOD.Gump, gumpTimeout)
            WaitForTarget(targetTimeout)
            ClearJournal()
        elif not TargetExists(): return


def BookDeedsRemaining():
    if DEBUG:SysMessage("[debug]:In BookDeedsRemaining", debugTextColor)
    # Close any existing gump (could be another book)
    ReplyGump(BODBookGump, 0)
    
    bodBook = GetAlias("tailor bod source")
    if not bodBook == 0:
        # I want to handle a book with many deeds in it but
        # with the filter have none to pull from book therefore
        # cannot use the book property for 'Deeds Remaining:'
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
        SysMessage("Did not find the 'smith bod source' alias", errorTextColor)

    return False


# ******************************
# *****      MAIN          *****
# ******************************
def Main():
    while BookDeedsRemaining() or FindType(BOD.Graphic, 1, "backpack", BOD.TailorHue):
        # Search for BOD to Fill
        if FindType(BOD.Graphic, 1, "backpack", BOD.TailorHue):
            bod = BOD(GetAlias("found"))
            if bod.isCompletable:
                if DEBUG: SysMessage("[debug]:PASSED COMPLETED CHECK: " + str(bod.isCompletable), debugTextColor)
                bod.SetCombineOption()
                SetLeatherType(bod)
                Pause(600)

                while (TargetExists() and bod.item != None and bod.isCompletable):
                    CheckMaterials(bod)
                    CraftTailorItem(bod.item)
                    bod.isCompletable = bod.CheckIfCompletable()
                    if DEBUG: 
                        SysMessage("[debug]:BOD completable: " + str(bod.isCompletable), debugTextColor)
                        SysMessage("[debug]:Out of Cloth: " + str(Material.outOfCloth), debugTextColor)
                        SysMessage("[debug]:Out of Leather: " + str(Material.outOfLeather), debugTextColor)
                        SysMessage("[debug]:Out of Spined: " + str(Material.outOfSpined), debugTextColor)
                        SysMessage("[debug]:Out of Horned: " + str(Material.outOfHorned), debugTextColor)
                        SysMessage("[debug]:Out of Barbed: " + str(Material.outOfBarbed), debugTextColor)
                        SysMessage("[debug]:Out of Bone: " + str(Material.outOfBone), debugTextColor)


                if bod.completed == bod.amount or not TargetExists():
                    # BOD is complete, move to destination book
                    SysMessage("BOD is complete", textColor)
                    ReplyGump(BOD.Gump, 0) # Close
                    destination = GetAlias('tailor bod destination')
                    Pause(mediumPause)
                    MoveItem(bod.id, destination)
                    bod = None
                    Pause(shortPause)
                    UnloadMaterials(True)
                    Pause(shortPause)
            else:
                if DEBUG: SysMessage("[debug]:Moving deed to uncompletable book", debugTextColor)
                # Move to incompletable book
                SysMessage("NOT doing this BOD", textColor)
                uncompletableBook = GetAlias('tailor uncompletable bod book')
                Pause(mediumPause)
                MoveItem(bod.id, uncompletableBook)
                Pause(shortPause)
                UnloadMaterials(True)
                Pause(shortPause)

        # Get A BOD out of the book
        else:
            ReplyGump(BODBookGump, 0) 
            SysMessage("Getting a new BOD", textColor)
            bodBook = GetAlias("tailor bod source")
            UseObject(bodBook)
            WaitForGump(BODBookGump, gumpTimeout)
            ReplyGump(BODBookGump, 5)
            Pause(longPause)

    UnloadMaterials(False)
    # Close Gumps
    ReplyGump(BODBookGump, 0)
    ReplyGump(BOD.Gump, 0)
    ReplyGump(tailorGump, 0)
    # End Macro
    SysMessage("NO BODS TO FILL", textColor)
    CancelTarget()
    Stop()


# ******************************
# ***** MACRO ENTRY POINT  *****
# ******************************
Main()