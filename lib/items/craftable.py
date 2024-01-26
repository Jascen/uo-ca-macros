from craft.item import CraftableItem


# *************************
# Alchemy
# *************************
## ***** Potions *****
LesserExplosionPotion  = CraftableItem(0x2407, 1, 65, "lesser explosion potion")
ExplosionPotion        = CraftableItem(0xf0d, 1, 72, "explosion potion")
GreaterExplosionPotion = CraftableItem(0x2408, 1, 79, "greater explosion potion")
LesserPoisonPotion     = CraftableItem(0x2600, 1, 128, "lesser poison potion")
PoisonPotion           = CraftableItem(0xf0a, 1, 135, "poison potion")
GreaterPoisonPotion    = CraftableItem(0x2601, 1, 142, "greater poison potion")
DeadlyPoisonPotion     = CraftableItem(0x2669, 1, 149, "deadly poison potion")
LethalPoisonPotion     = CraftableItem(0x266a, 1, 156, "lethal poison potion")
## ***** Transmutations *****
TransmuteDullCopper    = CraftableItem(0x1bd7, 22, 2, "dull copper ingot")
TransmuteShadowIron    = CraftableItem(0x1bd7, 22, 9, "shadow iron ingot")
TransmuteCopper        = CraftableItem(0x1bd7, 22, 16, "copper ingot")
TransmuteBronze        = CraftableItem(0x1bd7, 22, 23, "bronze ingot")
TransmuteMohagony      = CraftableItem(0x1bd7, 22, 107, "mohagony board")
TransmuteDriftwood     = CraftableItem(0x1bd7, 22, 114, "driftwood board")


# *************************
# Blacksmith
# *************************
## ***** Chain/Ring/Banded *****
ChainmailCoif          = CraftableItem(0x13bb, 1, 2, "chainmail coif") # TODO: Verify
ChainmailLeggings      = CraftableItem(0x13be, 1, 9, "chainmail leggings")
ChainmailTunic         = CraftableItem(0x13bf, 1, 16, "chainmail tunic")
RingmailGloves         = CraftableItem(0x13eb, 1, 23, "ringmail gloves")
RingmailLeggings       = CraftableItem(0x13f0, 1, 30, "ringmail leggings")
RingmailSleeves        = CraftableItem(0x13ee, 1, 37, "ringmail sleeves")
RingmailTunic          = CraftableItem(0x13ec, 1, 44, "ringmail tunic")
## ***** Platemail *****
PlatemailArms          = CraftableItem(0x304, 8, 2, "platemail arms") # TODO: Verify
PlatemailGloves        = CraftableItem(0x1414, 8, 9, "platemail gloves") # TODO: Verify
PlatemailGorget        = CraftableItem(0x1413, 8, 16, "platemail gorget") # TODO: Verify
PlatemailLeggings      = CraftableItem(0x1411, 8, 23, "platemail legs") # TODO: Verify
PlatemailTunic         = CraftableItem(0x1415, 8, 37, "platemail tunic") # TODO: Verify
PlatemailTunicFemale   = CraftableItem(0x1c04, 8, 44, "female plate") # TODO: Verify
## ***** Royal Armor *****
RoyalGorget            = CraftableItem(0x2b0e, 15, 16, "royal gorget")
## ***** Scalemail *****
## ***** Helmets *****
Bascinet               = CraftableItem(0x140c, 29, 2, "bascinet")
CloseHelmet            = CraftableItem(0x1408, 29, 9, "close helmet")
Helmet                 = CraftableItem(0x140a, 29, 16, "helmet")
NorseHelm              = CraftableItem(0x140e, 29, 23, "norse helm")
PlateHelm              = CraftableItem(0x1412, 29, 30, "plate helm")
## ***** Shields *****
Buckler                = CraftableItem(0x1b73, 36, 2, "buckler")
RoundShield            = CraftableItem(0x1b72, 36, 9, "bronze shield") # TODO: Verify
HeaterShield           = CraftableItem(0x1b76, 36, 16, "heater shield")
MetalShield            = CraftableItem(0x1b7b, 36, 23, "metal shield")
MetalKiteShield        = CraftableItem(0x1b74, 36, 30, "metal kite shield")
TearKiteShield         = CraftableItem(0x1b79, 36, 37, "tear kite shield")
ChaosShield            = CraftableItem(0x1bc3, 36, 93, "chaos shield") # TODO: Verify
OrderShield            = CraftableItem(0x1bc4, 36, 100, "order shield") # TODO: Verify
## ***** Bladed *****
BarbarianSword         = CraftableItem(0x13b9, 43, 16, "viking sword")
Broadsword             = CraftableItem(0xf5e, 43, 23, "broadsword")
CrescentBlade          = CraftableItem(0x26c1, 43, 30, "crescent blade") # TODO: Verify
Cutlass                = CraftableItem(0x1441, 43, 37, "cutlass")
Dagger                 = CraftableItem(0xf52, 43, 44, "dagger")
Katana                 = CraftableItem(0x13ff, 43, 58, "katana")
Kryss                  = CraftableItem(0x1401, 43, 65, "kryss")
Longsword              = CraftableItem(0xf61, 43, 72, "longsword")
Scimitar               = CraftableItem(0x13b6, 43, 100, "scimitar")
## ***** Axes *****
Axe                    = CraftableItem(0xf49, 50, 16, "axe")
BattleAxe              = CraftableItem(0xf47, 50, 23, "battle axe")
DoubleAxe              = CraftableItem(0xf4b, 50, 30, "double axe")
ExecutionerAxe         = CraftableItem(0xf45, 50, 37, "executioner's axe")
LargeBattleAxe         = CraftableItem(0x13fb, 50, 44, "large battle axe")
TwoHandedAxe           = CraftableItem(0x1443, 50, 51, "two handed axe")
WarAxe                 = CraftableItem(0x13b0, 50, 58, "war axe")
## ***** Polearms *****
Bardiche               = CraftableItem(0xf4d, 57, 2, "bardiche")
BladedStaff            = CraftableItem(0x26bd, 57, 9, "bladed staff") # TODO: Verify
DoubleBladedStaff      = CraftableItem(0x26bf, 57, 16, "double bladed staff") # TODO: Verify
Halberd                = CraftableItem(0x143e, 57, 23, "halberd")
Lance                  = CraftableItem(0x26c0, 57, 37, "lance") # TODO: Verify
Pike                   = CraftableItem(0x26be, 57, 44, "pike") # TODO: Verify ?????
ShortSpear             = CraftableItem(0x1403, 57, 51, "short spear")
Scythe                 = CraftableItem(0x26ba, 57, 58, "scythe") # TODO: Verify
Spear                  = CraftableItem(0xf62, 57, 65, "spear")
Warfork                = CraftableItem(0x1405, 57, 72, "war fork")
## ***** Bashing *****
HammerPick             = CraftableItem(0x143d, 64, 9, "hammer pick")
Mace                   = CraftableItem(0xf5c, 64, 16, "mace")
Maul                   = CraftableItem(0x143b, 64, 23, "maul")
Scepter                = CraftableItem(0x26bc, 64, 30, "scepter") # TODO: Verify ???
WarMace                = CraftableItem(0x1407, 64, 37, "war mace")
WarHammer              = CraftableItem(0x1439, 64, 44, "war hammer")


# *************************
# Carpentry
# *************************
## ***** Other *****
BarkFragment           = CraftableItem(0x318f, 1, 9, "bark fragment")
BarrelStaves           = CraftableItem(0x1eb1, 1, 23, "barrel staves")
BarrelLid              = CraftableItem(0x1db8, 1, 30, "barrel lid")
## ***** Furniture *****
WoodenChair            = CraftableItem(0xb57, 8, 23, "chair")
## ***** Weapons and Armor *****
Fukiya                 = CraftableItem(0x27aa, 29, 44, "fukiya")
Bokuto                 = CraftableItem(0x27a8, 29, 37, "bokuto")
Tetsubo                = CraftableItem(0x27a6, 29, 51, "tetsubo")


# *************************
# Fletching
# *************************
## ***** Materials *****
Shaft                  = CraftableItem(0x1bd4, 1, 9, "shaft")
## ***** Weapons *****
Bow                    = CraftableItem(0x13b2, 15, 2, "bow")
Crossbow               = CraftableItem(0xf50, 15, 9, "crossbow")
HeavyCrossbow          = CraftableItem(0x13fd, 15, 16, "heavy crossbow")
CompositeBow           = CraftableItem(0x26c2, 15, 23, "composite bow")
RepeatingBow           = CraftableItem(0x26c3, 15, 30, "repeating crossbow")
Yumi                   = CraftableItem(0x27a5, 15, 37, "yumi")
WoodlandShortbow       = CraftableItem(0x2d2b, 15, 44, "woodland shortbow")
WoodlandLongbow        = CraftableItem(0x2d1e, 15, 51, "woodland longbow")


# *************************
# Tailoring
# *************************
## ***** Hats *****
Skullcap               = CraftableItem(0x1544, 8, 2, "skullcap")
Bandana                = CraftableItem(0x1540, 8, 9, "bandana")
FloppyHat              = CraftableItem(0x1713, 8, 16, "floppy hat")
Cap                    = CraftableItem(0x1715, 8, 23, "cap")
WideBrimHat            = CraftableItem(0x1714, 8, 30, "wide-brim hat")
StrawHat               = CraftableItem(0x1717, 8, 37, "straw hat")
TallStrawHat           = CraftableItem(0x1716, 8, 44, "tall straw hat")
WizardHat              = CraftableItem(0x1718, 8, 51, "wizard's hat")
Bonnet                 = CraftableItem(0x1719, 8, 65, "bonnet")
FeatheredHat           = CraftableItem(0x171a, 8, 72, "feathered hat")
TricornHat             = CraftableItem(0x171b, 8, 79, "tricorne hat")
JesterHat              = CraftableItem(0x171c, 8, 93, "jester hat")
Kasa                   = CraftableItem(0x2798, 8, 163, "kasa")
## ***** Shirts *****
Doublet                = CraftableItem(0x1f7b, 15, 2, "doublet")
Shirt                  = CraftableItem(0x1517, 15, 9, "shirt")
Tunic                  = CraftableItem(0x1fa1, 15, 37, "tunic")
Surcoat                = CraftableItem(0x1ffd, 15, 44, "surcoat")
PlainDress             = CraftableItem(0x1f01, 15, 51, "plain dress")
FancyDress             = CraftableItem(0x1f00, 15, 58, "fancy dress")
Cloak                  = CraftableItem(0x1515, 15, 72, "cloak")
Robe                   = CraftableItem(0x1f03, 15, 86, "robe")
JesterSuit             = CraftableItem(0x1f9f, 15, 198, "jester suit")
FancyShirt             = CraftableItem(0x1efd, 15, 296, "fancy shirt")
## ***** Pants *****
ShortPants             = CraftableItem(0x152e, 22, 2, "short pants")
LongPants              = CraftableItem(0x1539, 22, 9, "long pants")
Kilt                   = CraftableItem(0x1537, 22, 30, "kilt")
Skirt                  = CraftableItem(0x1516, 22, 37, "skirt")
## ***** Miscellaneous *****
BodySash               = CraftableItem(0x1541, 29, 2, "body sash")
HalfApron              = CraftableItem(0x153b, 29, 16, "half apron")
FullApron              = CraftableItem(0x153d, 29, 23, "full apron")
HarpoonRope            = CraftableItem(0x52b1, 29, 51, "harpoon rope")
OilCloth               = CraftableItem(0x175d, 29, 58, "oil cloth")
## ***** Footwear *****
Sandals                = CraftableItem(0x170d, 36, 30, "sandals")
Shoes                  = CraftableItem(0x170f, 36, 37, "shoes")
Boots                  = CraftableItem(0x170b, 36, 44, "boots")
ThighBoots             = CraftableItem(0x1711, 36, 51, "thigh boots")
## ***** Leather Armor *****
LeatherGorget          = CraftableItem(0x13c7, 43, 2, "leather gorget")
LeatherCap             = CraftableItem(0x1db9, 43, 9, "leather cap")
LeatherGloves          = CraftableItem(0x13c6, 43, 16, "leather gloves")
LeatherSleeves         = CraftableItem(0x13cd, 43, 23, "leather sleeves")
LeatherLeggings        = CraftableItem(0x13cb, 43, 30, "leather leggings")
LeatherTunic           = CraftableItem(0x13cc, 43, 37, "leather tunic")
LeatherShorts          = CraftableItem(0x1c00, 43, 58, "leather shorts")
LeatherSkirt           = CraftableItem(0x1c08, 43, 65, "leather skirt")
LeatherBustier         = CraftableItem(0x1c0a, 43, 72, "leather bustier")
FemaleLeatherArmor     = CraftableItem(0x1c06, 43, 79, "female leather armor")
## ***** Studded Armor *****
StuddedGorget          = CraftableItem(0x13d6, 50, 2, "studded gorget")
StuddedGloves          = CraftableItem(0x13d5, 50, 9, "studded gloves")
StuddedSleeves         = CraftableItem(0x13dc, 50, 16, "studded sleeves")
StuddedLeggings        = CraftableItem(0x13da, 50, 23, "studded leggings")
StuddedTunic           = CraftableItem(0x13db, 50, 37, "studded tunic")
StuddedBustier         = CraftableItem(0x1c0c, 50, 44, "studded bustier")
StuddedArmor           = CraftableItem(0x1c02, 50, 51, "studded armor")
## ***** Bone Armor *****
BoneHelmet             = CraftableItem(0x1451, 57, 2, "bone helmet")
BoneGloves             = CraftableItem(0x1450, 57, 9, "bone gloves")
BoneArms               = CraftableItem(0x144e, 57, 16, "bone arms")
BoneLeggings           = CraftableItem(0x1452, 57, 23, "bone leggings")
BoneArmor              = CraftableItem(0x144f, 57, 37, "bone armor")


# *************************
# Tinker
# *************************
## ***** Tools ******
Scissors               = CraftableItem(0xf9f, 8, 2, "scissors")
MortarAndPestle        = CraftableItem(0x4ce9, 8, 9, "mortar and pestle")
TinkerTool             = CraftableItem(0x1eb8, 8, 23, "tinker tool")
Hatchet                = CraftableItem(0xf43, 8, 30, "hatchet")
SewingKit              = CraftableItem(0x4c81, 8, 44, "sewing kit", -1)
Shovel                 = CraftableItem(0xf39, 8, 86, "shovel")
Hammer                 = CraftableItem(0x102a, 8, 107, "hammer")
Tongs                  = CraftableItem(0xfbb, 8, 114, "tongs")
Lockpick               = CraftableItem(0x14fc, 8, 149, "lockpick")
Skillet                = CraftableItem(0x97f, 8, 156, "skillet")
FletchingTool          = CraftableItem(0x1f2c, 8, 170, "fletching tools")
MapmakersPen           = CraftableItem(0x2052, 8, 177, "mapmaker's pen", -1)
ScribesPen             = CraftableItem(0x2051, 8, 184, "scribe's pen", -1)
## ***** Parts ******
BarrelHoops            = CraftableItem(0x1db7, 15, 37, "barrel hoops")
Gears                  = CraftableItem(0x1053, 15, 2, "gears")
BarrelTap              = CraftableItem(0x1004, 15, 16, "barrel tap")
# ***** Miscellaneous ******
Spyglass               = CraftableItem(0x14f5, 29, 51, "spyglass")