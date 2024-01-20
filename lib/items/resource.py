class Resource:
    def __init__(self, name, hue = -1):
        self.name = name
        self.hue = hue


# *************************
# Wood
# *************************
Wood           = Resource("wood", 0)
Ash            = Resource("ash", 1191)
Cherry         = Resource("cherry", 1863)
Ebony          = Resource("ebony", 2412)
GoldenOak      = Resource("golden oak", 2010)
Hickory        = Resource("hickory", 1045)
Mohagony       = Resource("mohagony", 2312)
Driftwood      = Resource("driftwood", 2419)
Oak            = Resource("oak", 1810)
Pine           = Resource("pine", 461)
Ghost          = Resource("ghost", 2498)
Rosewood       = Resource("rosewood", 2115)
Walnut         = Resource("walnut", 1872)
Petrified      = Resource("petrified", 2708) # TODO: Verify
Elven          = Resource("elven", 2618)


# *************************
# Metal
# *************************
Iron           = Resource("iron", 0)
DullCopper     = Resource("dull copper", 2741)
ShadowIron     = Resource("shadow", 2739)
Copper         = Resource("copper", 2840)
Bronze         = Resource("bronze", 2236)
Golden         = Resource("golden", 2458)
Agapite        = Resource("agapite", 2794)
Verite         = Resource("verite", 2141)
Valorite       = Resource("valorite", 2397)
Nepturite      = Resource("nepturite", 2376)
Obsidian       = Resource("obsidian", 1986) # TODO: Verify
Steel          = Resource("steel", 2463) # TODO: Verify
Brass          = Resource("brass", 2451)
Mithril        = Resource("mithril", 2928)
Xormite        = Resource("xormite", 1991) # TODO: Verify
Dwarven        = Resource("dwarven", 1788)


# *************************
# Leather
# *************************
Leather        = Resource("leather", 0)
Lizard         = Resource("lizard", 2736) # Horned
Serpent        = Resource("serpent", 2841) # Barbed
Necrotic       = Resource("necrotic", 1968)
Volcanic       = Resource("volcanic", 2873)
Frozen         = Resource("frozen", 2907)
DeepSea        = Resource("deep sea", 2747) # Spined
Goliath        = Resource("goliath", 2154)
Draconic       = Resource("draconic", 2740)
Hellish        = Resource("hellish", 2810)
Dinosaur       = Resource("dinosaur", 2333)
Alien          = Resource("alien", 2300)