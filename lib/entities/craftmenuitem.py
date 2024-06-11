from models.craftmenuitem import CraftMenuItem


# *************************
# Alchemy
# *************************
## ***** Potions *****
LesserExplosionPotion  = CraftMenuItem(0x2407, 1, 65, "lesser explosion potion")
ExplosionPotion        = CraftMenuItem(0xf0d,  1, 72, "explosion potion")
GreaterExplosionPotion = CraftMenuItem(0x2408, 1, 79, "greater explosion potion")
LesserPoisonPotion     = CraftMenuItem(0x2600, 1, 128, "lesser poison potion")
PoisonPotion           = CraftMenuItem(0xf0a,  1, 135, "poison potion")
GreaterPoisonPotion    = CraftMenuItem(0x2601, 1, 142, "greater poison potion")
DeadlyPoisonPotion     = CraftMenuItem(0x2669, 1, 149, "deadly poison potion")
LethalPoisonPotion     = CraftMenuItem(0x266a, 1, 156, "lethal poison potion")
GreaterStrengthPotion  = CraftMenuItem(0x25f7, 1, 191, "greater strength potion")
## ***** Transmutations *****
TransmuteDullCopper    = CraftMenuItem(0x1bd7, 22, 2, "dull copper ingot")
TransmuteShadowIron    = CraftMenuItem(0x1bd7, 22, 9, "shadow iron ingot")
TransmuteCopper        = CraftMenuItem(0x1bd7, 22, 16, "copper ingot")
TransmuteBronze        = CraftMenuItem(0x1bd7, 22, 23, "bronze ingot")
TransmuteMohagony      = CraftMenuItem(0x1bd7, 22, 107, "mohagony board")
TransmuteDriftwood     = CraftMenuItem(0x1bd7, 22, 114, "driftwood board")


# *************************
# Blacksmith
# *************************
## ***** Chain/Ring/Banded *****
ChainmailCoif          = CraftMenuItem(0x13bb, 1, 2, "chainmail coif") # TODO: Verify
ChainmailLeggings      = CraftMenuItem(0x13be, 1, 9, "chainmail leggings")
ChainmailTunic         = CraftMenuItem(0x13bf, 1, 16, "chainmail tunic")
RingmailGloves         = CraftMenuItem(0x13eb, 1, 23, "ringmail gloves")
RingmailLeggings       = CraftMenuItem(0x13f0, 1, 30, "ringmail leggings")
RingmailSleeves        = CraftMenuItem(0x13ee, 1, 37, "ringmail sleeves")
RingmailTunic          = CraftMenuItem(0x13ec, 1, 44, "ringmail tunic")
## ***** Platemail *****
PlatemailArms          = CraftMenuItem(0x304,  8, 2, "platemail arms") # TODO: Verify
PlatemailGloves        = CraftMenuItem(0x1414, 8, 9, "platemail gloves") # TODO: Verify
PlatemailGorget        = CraftMenuItem(0x1413, 8, 16, "platemail gorget") # TODO: Verify
PlatemailLeggings      = CraftMenuItem(0x1411, 8, 23, "platemail legs") # TODO: Verify
PlatemailTunic         = CraftMenuItem(0x1415, 8, 37, "platemail tunic") # TODO: Verify
PlatemailTunicFemale   = CraftMenuItem(0x1c04, 8, 44, "female plate") # TODO: Verify
## ***** Royal Armor *****
RoyalGorget            = CraftMenuItem(0x2b0e, 15, 16, "royal gorget")
## ***** Scalemail *****
## ***** Helmets *****
Bascinet               = CraftMenuItem(0x140c, 29, 2, "bascinet")
CloseHelmet            = CraftMenuItem(0x1408, 29, 9, "close helmet")
Helmet                 = CraftMenuItem(0x140a, 29, 16, "helmet")
NorseHelm              = CraftMenuItem(0x140e, 29, 23, "norse helm")
PlateHelm              = CraftMenuItem(0x1412, 29, 30, "plate helm")
## ***** Shields *****
Buckler                = CraftMenuItem(0x1b73, 36, 2, "buckler")
RoundShield            = CraftMenuItem(0x1b72, 36, 9, "bronze shield") # TODO: Verify
HeaterShield           = CraftMenuItem(0x1b76, 36, 16, "heater shield")
MetalShield            = CraftMenuItem(0x1b7b, 36, 23, "metal shield")
MetalKiteShield        = CraftMenuItem(0x1b74, 36, 30, "metal kite shield")
TearKiteShield         = CraftMenuItem(0x1b79, 36, 37, "tear kite shield")
ChaosShield            = CraftMenuItem(0x1bc3, 36, 93, "chaos shield") # TODO: Verify
OrderShield            = CraftMenuItem(0x1bc4, 36, 100, "order shield") # TODO: Verify
## ***** Bladed *****
BarbarianSword         = CraftMenuItem(0x13b9, 43, 16, "viking sword")
Broadsword             = CraftMenuItem(0xf5e,  43, 23, "broadsword")
CrescentBlade          = CraftMenuItem(0x26c1, 43, 30, "crescent blade") # TODO: Verify
Cutlass                = CraftMenuItem(0x1441, 43, 37, "cutlass")
Dagger                 = CraftMenuItem(0xf52,  43, 44, "dagger")
Katana                 = CraftMenuItem(0x13ff, 43, 58, "katana")
Kryss                  = CraftMenuItem(0x1401, 43, 65, "kryss")
Longsword              = CraftMenuItem(0xf61,  43, 72, "longsword")
Scimitar               = CraftMenuItem(0x13b6, 43, 100, "scimitar")
## ***** Axes *****
Axe                    = CraftMenuItem(0xf49,  50, 16, "axe")
BattleAxe              = CraftMenuItem(0xf47,  50, 23, "battle axe")
DoubleAxe              = CraftMenuItem(0xf4b,  50, 30, "double axe")
ExecutionerAxe         = CraftMenuItem(0xf45,  50, 37, "executioner's axe")
LargeBattleAxe         = CraftMenuItem(0x13fb, 50, 44, "large battle axe")
TwoHandedAxe           = CraftMenuItem(0x1443, 50, 51, "two handed axe")
WarAxe                 = CraftMenuItem(0x13b0, 50, 58, "war axe")
## ***** Polearms *****
Bardiche               = CraftMenuItem(0xf4d,  57, 2, "bardiche")
BladedStaff            = CraftMenuItem(0x26bd, 57, 9, "bladed staff") # TODO: Verify
DoubleBladedStaff      = CraftMenuItem(0x26bf, 57, 16, "double bladed staff") # TODO: Verify
Halberd                = CraftMenuItem(0x143e, 57, 23, "halberd")
Lance                  = CraftMenuItem(0x26c0, 57, 37, "lance") # TODO: Verify
Pike                   = CraftMenuItem(0x26be, 57, 44, "pike") # TODO: Verify ?????
ShortSpear             = CraftMenuItem(0x1403, 57, 51, "short spear")
Scythe                 = CraftMenuItem(0x26ba, 57, 58, "scythe") # TODO: Verify
Spear                  = CraftMenuItem(0xf62, 57, 65, "spear")
Warfork                = CraftMenuItem(0x1405, 57, 72, "war fork")
## ***** Bashing *****
HammerPick             = CraftMenuItem(0x143d, 64, 9, "hammer pick")
Mace                   = CraftMenuItem(0xf5c,  64, 16, "mace")
Maul                   = CraftMenuItem(0x143b, 64, 23, "maul")
Scepter                = CraftMenuItem(0x26bc, 64, 30, "scepter") # TODO: Verify ???
WarMace                = CraftMenuItem(0x1407, 64, 37, "war mace")
WarHammer              = CraftMenuItem(0x1439, 64, 44, "war hammer")


# *************************
# Carpentry
# *************************
## ***** Other *****
BarkFragment           = CraftMenuItem(0x318f, 1, 9, "bark fragment")
BarrelStaves           = CraftMenuItem(0x1eb1, 1, 23, "barrel staves")
BarrelLid              = CraftMenuItem(0x1db8, 1, 30, "barrel lid")
## ***** Furniture *****
WoodenChair            = CraftMenuItem(0xb57,  8, 23, "chair")
## ***** Weapons and Armor *****
Fukiya                 = CraftMenuItem(0x27aa, 29, 44, "fukiya")
Bokuto                 = CraftMenuItem(0x27a8, 29, 37, "bokuto")
Tetsubo                = CraftMenuItem(0x27a6, 29, 51, "tetsubo")


# *************************
# Fletching
# *************************
## ***** Materials *****
Shaft                  = CraftMenuItem(0x1bd4, 1, 9, "shaft")
## ***** Weapons *****
Bow                    = CraftMenuItem(0x13b2, 15, 2, "bow")
Crossbow               = CraftMenuItem(0xf50,  15, 9, "crossbow")
HeavyCrossbow          = CraftMenuItem(0x13fd, 15, 16, "heavy crossbow")
CompositeBow           = CraftMenuItem(0x26c2, 15, 23, "composite bow")
RepeatingBow           = CraftMenuItem(0x26c3, 15, 30, "repeating crossbow")
Yumi                   = CraftMenuItem(0x27a5, 15, 37, "yumi")
WoodlandShortbow       = CraftMenuItem(0x2d2b, 15, 44, "woodland shortbow")
WoodlandLongbow        = CraftMenuItem(0x2d1e, 15, 51, "woodland longbow")


# *************************
# Inscription
# *************************
## ***** First Circle *****
ReactiveArmor          = CraftMenuItem(0x00, 1, 2, "reactive armor")
Clumsy                 = CraftMenuItem(0x00, 1, 9, "clumsy")
CreateFood             = CraftMenuItem(0x00, 1, 16, "create food")
Feeblemind             = CraftMenuItem(0x00, 1, 23, "feeblemind")
Heal                   = CraftMenuItem(0x00, 1, 30, "heal")
MagicArrow             = CraftMenuItem(0x00, 1, 37, "magic arrow")
NightSight             = CraftMenuItem(0x00, 1, 44, "night sight")
weaken                 = CraftMenuItem(0x00, 1, 51, "weaken")
## ***** Second Circle *****
Agility                = CraftMenuItem(0x00, 8, 2, "agility")
Cunning                = CraftMenuItem(0x00, 8, 9, "cunning")
Cure                   = CraftMenuItem(0x00, 8, 16, "cure")
Harm                   = CraftMenuItem(0x00, 8, 23, "harm")
MagicTrap              = CraftMenuItem(0x00, 8, 30, "magic trap")
MagicUntrap            = CraftMenuItem(0x00, 8, 37, "magic untrap")
Protection             = CraftMenuItem(0x00, 8, 44, "protection")
Strength               = CraftMenuItem(0x00, 8, 51, "strength")
## ***** Third Circle *****
Bless                  = CraftMenuItem(0x00, 15, 2, "bless")
Fireball               = CraftMenuItem(0x00, 15, 9, "fireball")
MagicLock              = CraftMenuItem(0x00, 15, 16, "magic lock")
Poison                 = CraftMenuItem(0x00, 15, 23, "poison")
Telekinesis            = CraftMenuItem(0x00, 15, 30, "telekinesis")
Teleport               = CraftMenuItem(0x00, 15, 37, "teleport")
Unlock                 = CraftMenuItem(0x00, 15, 44, "unlock")
WallOfStone            = CraftMenuItem(0x00, 15, 51, "wall of stone")
## ***** Fourth Circle *****
ArchCure               = CraftMenuItem(0x00, 22, 2, "arch cure")
ArchProtection         = CraftMenuItem(0x00, 22, 9, "arch protection")
Curse                  = CraftMenuItem(0x00, 22, 16, "curse")
FireField              = CraftMenuItem(0x00, 22, 23, "fire field")
GreaterHeal            = CraftMenuItem(0x00, 22, 30, "greater heal")
Lightning              = CraftMenuItem(0x00, 22, 37, "lightning")
ManaDrain              = CraftMenuItem(0x00, 22, 44, "mana drain")
Recall                 = CraftMenuItem(0x00, 22, 51, "recall")
## ***** Fifth Circle *****
BladeSpirits           = CraftMenuItem(0x00, 29, 2, "blade spirits")
DispelField            = CraftMenuItem(0x00, 29, 9, "dispel field")
Incognito              = CraftMenuItem(0x00, 29, 16, "incognito")
MagicReflection        = CraftMenuItem(0x00, 29, 23, "magic reflection")
MindBlast              = CraftMenuItem(0x00, 29, 30, "mind blast")
Paralyze               = CraftMenuItem(0x00, 29, 37, "paralyze")
PoisonField            = CraftMenuItem(0x00, 29, 44, "poison field")
SummonCreature         = CraftMenuItem(0x00, 29, 51, "summon creature")
## ***** Sixth Circle *****
Dispel                 = CraftMenuItem(0x00, 36, 2, "dispel")
EnergyBolt             = CraftMenuItem(0x00, 36, 9, "energy bolt")
Explosion              = CraftMenuItem(0x00, 36, 16, "explosion")
Invisibility           = CraftMenuItem(0x00, 36, 23, "invisibility")
Mark                   = CraftMenuItem(0x00, 36, 30, "mark")
MassCurse              = CraftMenuItem(0x00, 36, 37, "mass curse")
ParalyzeField          = CraftMenuItem(0x00, 36, 44, "paralyze field")
Reveal                 = CraftMenuItem(0x00, 36, 51, "reveal")
## ***** Seventh Circle *****
ChainLightning         = CraftMenuItem(0x00, 43, 2, "chain lightning")
EnergyField            = CraftMenuItem(0x00, 43, 9, "energy field")
Flamestrike            = CraftMenuItem(0x00, 43, 16, "flamestrike")
GateTravel             = CraftMenuItem(0x00, 43, 23, "gate travel")
ManaVampire            = CraftMenuItem(0x00, 43, 30, "mana vampire")
MassDispel             = CraftMenuItem(0x00, 43, 37, "mass dispel")
MeteorSwarm            = CraftMenuItem(0x00, 43, 44, "meteor swarm")
Polymorph              = CraftMenuItem(0x00, 43, 51, "polymorph")
## ***** Eigth Circle *****
Earthquake             = CraftMenuItem(0x00, 50, 2, "earthquake")
EnergyVortex           = CraftMenuItem(0x00, 50, 9, "energy vortex")
Resurrection           = CraftMenuItem(0x00, 50, 16, "resurrection")
SummonAirElemental     = CraftMenuItem(0x00, 50, 23, "summon air elemental")
SummonDaemon           = CraftMenuItem(0x00, 50, 30, "summon daemon")
SummonEarthElemental   = CraftMenuItem(0x00, 50, 37, "summon earth elemental")
SummonFireElemental    = CraftMenuItem(0x00, 50, 44, "summon fire elemental")
SummonWaterElemental   = CraftMenuItem(0x00, 50, 51, "summon water elemental")


# *************************
# Tailoring
# *************************
## ***** Hats *****
Skullcap               = CraftMenuItem(0x1544, 8, 2, "skullcap")
Bandana                = CraftMenuItem(0x1540, 8, 9, "bandana")
FloppyHat              = CraftMenuItem(0x1713, 8, 16, "floppy hat")
Cap                    = CraftMenuItem(0x1715, 8, 23, "cap")
WideBrimHat            = CraftMenuItem(0x1714, 8, 30, "wide-brim hat")
StrawHat               = CraftMenuItem(0x1717, 8, 37, "straw hat")
TallStrawHat           = CraftMenuItem(0x1716, 8, 44, "tall straw hat")
WizardHat              = CraftMenuItem(0x1718, 8, 51, "wizard's hat")
Bonnet                 = CraftMenuItem(0x1719, 8, 65, "bonnet")
FeatheredHat           = CraftMenuItem(0x171a, 8, 72, "feathered hat")
TricornHat             = CraftMenuItem(0x171b, 8, 79, "tricorne hat")
JesterHat              = CraftMenuItem(0x171c, 8, 93, "jester hat")
Kasa                   = CraftMenuItem(0x2798, 8, 163, "kasa")
## ***** Shirts *****
Doublet                = CraftMenuItem(0x1f7b, 15, 2, "doublet")
Shirt                  = CraftMenuItem(0x1517, 15, 9, "shirt")
Tunic                  = CraftMenuItem(0x1fa1, 15, 37, "tunic")
Surcoat                = CraftMenuItem(0x1ffd, 15, 44, "surcoat")
PlainDress             = CraftMenuItem(0x1f01, 15, 51, "plain dress")
FancyDress             = CraftMenuItem(0x1f00, 15, 58, "fancy dress")
Cloak                  = CraftMenuItem(0x1515, 15, 72, "cloak")
Robe                   = CraftMenuItem(0x1f03, 15, 86, "robe")
JesterSuit             = CraftMenuItem(0x1f9f, 15, 198, "jester suit")
FancyShirt             = CraftMenuItem(0x1efd, 15, 296, "fancy shirt")
## ***** Pants *****
ShortPants             = CraftMenuItem(0x152e, 22, 2, "short pants")
LongPants              = CraftMenuItem(0x1539, 22, 9, "long pants")
Kilt                   = CraftMenuItem(0x1537, 22, 30, "kilt")
Skirt                  = CraftMenuItem(0x1516, 22, 37, "skirt")
## ***** Miscellaneous *****
BodySash               = CraftMenuItem(0x1541, 29, 2, "body sash")
HalfApron              = CraftMenuItem(0x153b, 29, 16, "half apron")
FullApron              = CraftMenuItem(0x153d, 29, 23, "full apron")
HarpoonRope            = CraftMenuItem(0x52b1, 29, 51, "harpoon rope")
OilCloth               = CraftMenuItem(0x175d, 29, 58, "oil cloth")
## ***** Footwear *****
Sandals                = CraftMenuItem(0x170d, 36, 30, "sandals")
Shoes                  = CraftMenuItem(0x170f, 36, 37, "shoes")
Boots                  = CraftMenuItem(0x170b, 36, 44, "boots")
ThighBoots             = CraftMenuItem(0x1711, 36, 51, "thigh boots")
## ***** Leather Armor *****
LeatherGorget          = CraftMenuItem(0x13c7, 43, 2, "leather gorget")
LeatherCap             = CraftMenuItem(0x1db9, 43, 9, "leather cap")
LeatherGloves          = CraftMenuItem(0x13c6, 43, 16, "leather gloves")
LeatherSleeves         = CraftMenuItem(0x13cd, 43, 23, "leather sleeves")
LeatherLeggings        = CraftMenuItem(0x13cb, 43, 30, "leather leggings")
LeatherTunic           = CraftMenuItem(0x13cc, 43, 37, "leather tunic")
LeatherShorts          = CraftMenuItem(0x1c00, 43, 58, "leather shorts")
LeatherSkirt           = CraftMenuItem(0x1c08, 43, 65, "leather skirt")
LeatherBustier         = CraftMenuItem(0x1c0a, 43, 72, "leather bustier")
FemaleLeatherArmor     = CraftMenuItem(0x1c06, 43, 79, "female leather armor")
## ***** Studded Armor *****
StuddedGorget          = CraftMenuItem(0x13d6, 50, 2, "studded gorget")
StuddedGloves          = CraftMenuItem(0x13d5, 50, 9, "studded gloves")
StuddedSleeves         = CraftMenuItem(0x13dc, 50, 16, "studded sleeves")
StuddedLeggings        = CraftMenuItem(0x13da, 50, 23, "studded leggings")
StuddedTunic           = CraftMenuItem(0x13db, 50, 37, "studded tunic")
StuddedBustier         = CraftMenuItem(0x1c0c, 50, 44, "studded bustier")
StuddedArmor           = CraftMenuItem(0x1c02, 50, 51, "studded armor")
## ***** Bone Armor *****
BoneHelmet             = CraftMenuItem(0x1451, 57, 2, "bone helmet")
BoneGloves             = CraftMenuItem(0x1450, 57, 9, "bone gloves")
BoneArms               = CraftMenuItem(0x144e, 57, 16, "bone arms")
BoneLeggings           = CraftMenuItem(0x1452, 57, 23, "bone leggings")
BoneArmor              = CraftMenuItem(0x144f, 57, 37, "bone armor")


# *************************
# Tinker
# *************************
## ***** Tools ******
Scissors               = CraftMenuItem(0xf9f,  8, 2, "scissors")
MortarAndPestle        = CraftMenuItem(0x4ce9, 8, 9, "mortar and pestle")
TinkerTool             = CraftMenuItem(0x1eb8, 8, 23, "tinker tool")
Hatchet                = CraftMenuItem(0xf43,  8, 30, "hatchet")
SewingKit              = CraftMenuItem(0x4c81, 8, 44, "sewing kit", -1)
Shovel                 = CraftMenuItem(0xf39,  8, 86, "shovel")
Hammer                 = CraftMenuItem(0x102a, 8, 107, "hammer")
Tongs                  = CraftMenuItem(0xfbb,  8, 114, "tongs")
Lockpick               = CraftMenuItem(0x14fc, 8, 149, "lockpick")
Skillet                = CraftMenuItem(0x97f,  8, 156, "skillet")
FletchingTool          = CraftMenuItem(0x1f2c, 8, 170, "fletching tools")
MapmakersPen           = CraftMenuItem(0x2052, 8, 177, "mapmaker's pen", -1)
ScribesPen             = CraftMenuItem(0x2051, 8, 184, "scribe's pen", -1)
## ***** Parts ******
BarrelHoops            = CraftMenuItem(0x1db7, 15, 37, "barrel hoops")
Gears                  = CraftMenuItem(0x1053, 15, 2, "gears")
BarrelTap              = CraftMenuItem(0x1004, 15, 16, "barrel tap")
# ***** Miscellaneous ******
Spyglass               = CraftMenuItem(0x14f5, 29, 51, "spyglass")