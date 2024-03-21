from models.resourcetype import ResourceType


class MetalResourceType:
    Iron           = ResourceType("iron",        0)
    DullCopper     = ResourceType("dull copper", 2741)
    ShadowIron     = ResourceType("shadow",      2739)
    Copper         = ResourceType("copper",      2840)
    Bronze         = ResourceType("bronze",      2236)
    Golden         = ResourceType("golden",      2458)
    Agapite        = ResourceType("agapite",     2794)
    Verite         = ResourceType("verite",      2141)
    Valorite       = ResourceType("valorite",    2397)
    Nepturite      = ResourceType("nepturite",   2376)
    Obsidian       = ResourceType("obsidian",    1986) # TODO: Verify
    Steel          = ResourceType("steel",       2463) # TODO: Verify
    Brass          = ResourceType("brass",       2451)
    Mithril        = ResourceType("mithril",     2928)
    Xormite        = ResourceType("xormite",     1991)
    Dwarven        = ResourceType("dwarven",     1788)


class LeatherResourceType:
    Leather        = ResourceType("leather",  0)
    Lizard         = ResourceType("lizard",   2736) # Horned
    Serpent        = ResourceType("serpent",  2841) # Barbed
    Necrotic       = ResourceType("necrotic", 1968)
    Volcanic       = ResourceType("volcanic", 2873)
    Frozen         = ResourceType("frozen",   2907)
    DeepSea        = ResourceType("deep sea", 2747) # Spined
    Goliath        = ResourceType("goliath",  2154)
    Draconic       = ResourceType("draconic", 2740)
    Hellish        = ResourceType("hellish",  2810)
    Dinosaur       = ResourceType("dinosaur", 2333)
    Alien          = ResourceType("alien",    2300)


class WoodResourceType:
    Wood           = ResourceType("wood",       0)
    Ash            = ResourceType("ash",        1191)
    Cherry         = ResourceType("cherry",     1863)
    Ebony          = ResourceType("ebony",      2412)
    GoldenOak      = ResourceType("golden oak", 2010)
    Hickory        = ResourceType("hickory",    1045)
    Mohagony       = ResourceType("mohagony",   2312)
    Driftwood      = ResourceType("driftwood",  2419)
    Oak            = ResourceType("oak",        1810)
    Pine           = ResourceType("pine",       461)
    Ghost          = ResourceType("ghost",      2498)
    Rosewood       = ResourceType("rosewood",   2115)
    Walnut         = ResourceType("walnut",     1872)
    Petrified      = ResourceType("petrified",  2708) # TODO: Verify
    Elven          = ResourceType("elven",      2618)