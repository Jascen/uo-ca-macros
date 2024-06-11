from services.filter.implementations import AllFilter, AnyFilter, NameFilter, NotFilter, PropertyFilter, TypeFilter

class FixedLists:
    Instruments = AnyFilter([
        TypeFilter(0xe9d), # Tambourine
        TypeFilter(0xe9e), # Tambourine w/ Tassel                    
        TypeFilter(0xeb3), # Lute
        TypeFilter(0xeb2), # Harp
        TypeFilter(0xe9c), # Drum
        TypeFilter(0x2805), # Flute
    ])
    Slayers = AnyFilter([
        PropertyFilter("Giant Killer"),
        PropertyFilter("Supernatural Vanquishing"),
        PropertyFilter("Weed Ruin"),
        PropertyFilter("Serpentaur Execution"),
        PropertyFilter("Orcish Demise"),
        PropertyFilter("Ogre Extinction"),
        PropertyFilter("Golem Destruction"),
    ])
    Jewelry = AnyFilter([
        NameFilter("earring"),
        NameFilter("beads"),
        NameFilter("amulet"),
        NameFilter("necklace"),
        NameFilter("bracelet"),
        AllFilter([ # Rings - The coloring of names provides False positives because "ring" is a substring of "string"
            AnyFilter([
                NameFilter(" ring"),
                NameFilter("ring "),
            ]),
            NotFilter(PropertyFilter("requirement"))
        ]),
    ])