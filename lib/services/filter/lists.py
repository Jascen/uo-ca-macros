from services.filter.implementations import NameFilter, PropertyFilter, TypeFilter
class List:
    Instruments = [
        TypeFilter(0xe9d), # Tambourine
        TypeFilter(0xe9e), # Tambourine w/ Tassel                    
        TypeFilter(0xeb3), # Lute
        TypeFilter(0xeb2), # Harp
        TypeFilter(0xe9c), # Drum
        TypeFilter(0x2805), # Flute
    ]
    Slayers = [
        PropertyFilter("Giant Killer"),
        PropertyFilter("Supernatural Vanquishing"),
        PropertyFilter("Weed Ruin"),
        PropertyFilter("Serpentaur Execution"),
        PropertyFilter("Orcish Demise"),
        PropertyFilter("Ogre Extinction"),
        PropertyFilter("Golem Destruction"),
    ]
    Jewelry = [
        NameFilter("ring"), # Ring, Earrings
        NameFilter("beads"),
        NameFilter("amulet"),
        NameFilter("necklace"),
        NameFilter("bracelet"),
    ]

    @classmethod
    def Merge(cls, *lists):
        value = []
        for list in lists:
            value += list

        return value