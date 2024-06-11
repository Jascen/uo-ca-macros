"""
Name: Item Organizer
Description: Used to move items that pass the configured Filter Criteria from a Source container to a Destination container.
Author: Tsai (Ultima Adventures)
Version: v1.5
"""

from Assistant import Engine
from ClassicAssist.UO import UOMath


from services.filter.useroptions import UserOptions

from services.filter.systemcontainers import SystemContainers

class UserContainers:
    """
    User-Defined container serials or aliases. For use when creating Organizers.
    """
    
    ### Destinations - Begin
    Currency = SystemContainers.PlayerBank
    #Currency = None
    Arms_Lore = [0x401662dc, 0x40165b06, 0x401eefda]
    Item_Identification = [0x401662d7, 0x40166304, 0x401eefdc]
    Taste_Identification = [0x401632fe, 0x40163302, 0x40165a9e]
    Sellable_Stacks = [0x40165b00]
    Sellable_Items = [0x40165afd, 0x401632f9, 0x40163310]
    Books = [0x40165b19]
    Scrolls = [0x401eef95]

    Cartography = [0x401eefa4]
    Magery = [0x401eefd8]
    Reagents = [0x401eefcf]
    Potions = [0x401eef9e]
    Resources_Cloth = [0x401eefc8]
    Resources_Metal = [0x401eefd1]
    Resources_Leather = [0x401eefd6]
    Resources_Wood = [0x401eefd3]
    Fun = [0x401eefa8]

    Artifact_Weapon = [0x401ef25f]
    Artifact_Other = [0x401ef25b]
    Magic_Instruments = [0x401ef24f]
    Skill_Bonus = [0x401ef258, 0x40165b1b]
    ### Destinations - End


def GetIgnoredFilters():
    """
    User-Defined list of Filters that should not be organized.
    """

    return [
        0xefa, # Magery spellbook
        0x2253, # Necromancer book
        0x98f, # Waterskin
        "Skull of Baron Almric",
        "Belongs To",
        "Kas' & Knight", # DK book
        "Book of Ninjitsu",
        "Book of Bushido",
        "Book of Chivalry",
    ]


def GetOrganizers():
    """
    User-constructed list of Organizers to execute.

    Organizer(<Source>, <Destination>, <Filters>)
    - Source - Serial or Alias. The container to open and run the provided item Filters against
    - Destination - Serial or Alias. The container that an item is moved to if it passes at least one Filter
    - Filters - Array of Filters. All items found in the Source container are run through each Filter individually

    Warning: The order of your Organizers matters. Organizers are executed from first to last (top-down order).
    An item will be moved to the Destination first Organizer whose Filter passed

    Shorthand notation:
    - You may use number (0xab3) (0x123abc) values to check against an item's Grapich/ID or Serial
    - You may use string ("this is a string") values to check against item's `Name` or `Property values`
    - String notation may also use the `&` operator to require multiple conditions
      - Example: All unidentified wands
        - Filter = "wand & unidentified"
        - Item must contain "wand" in the `Name` or `Property values`
        - Item must contain "unidentified" in the `Name` or `Property values`
    
    Combining filters:
    - As use-cases evolve, you may need to invert filters to exclude items
    - Example: All non-weapon artifacts
        - Filter = All("Artifact", Not("Weapon"))
            - Item must contain "artifact" in the `Name` or `Property values`
            - Item must NOT contain "weapon" in either the `Name` or the `Property values`
    
    Explicit notation:
    - As use-cases evolve, you may need to explicitly create Filters yourself
        - Example: All non-weapon artifacts
          - Filter = AllFilter(["Artifact", NotFilter("Weapon")])
    """

    source = SystemContainers.PromptForSource

    return [
        Organizer(source, UserContainers.Arms_Lore, [
            "Use Arms Lore",
        ]),
        Organizer(source, UserContainers.Item_Identification, [
            "Use Item Identification",
            "wand & unidentified", # Wands
            "Magic Scroll",
        ]),
        Organizer(source, UserContainers.Taste_Identification, [
            "jar of & unidentified",
            "jug of & unidentified",
            "bottle of & unidentified",
            0x23a, # Venom Sack
        ]),
        Organizer(source, UserContainers.Sellable_Stacks, [
            TypeRangeFilter(0x0F0F, 0x0F30), # Individual gems (Diamond, Ruby, Sapphire, etc)
        ]),
        Organizer(source, UserContainers.Sellable_Items, [
            # Any Jewelry/Circlets with NO magical properties
            All(
                Any(
                    "circlet",
                    FixedLists.Jewelry,
                ),
                Any(
                    # Name, Weight, Durability ... nothing else
                    MaxPropertyCountFilter(3),

                    # Name, Weight, Durability, Exceptional ... nothing else
                    All(
                        MaxPropertyCountFilter(4),
                        "exceptional",
                    ),
                ),
            ),
        ]),
        Organizer(source, UserContainers.Books, [
            "Written By",
            All("Scroll of", Not(0x14f0)), # Not powerscrolls
            "World Map",
        ]),
        Organizer(source, UserContainers.Scrolls, [
            TypeRangeFilter(0x1F2D, 0x1F72), # Bard/Magery scrolls
            TypeRangeFilter(0x2260, 0x2279), # Necromancy scrolls
        ]),

        Organizer(source, UserContainers.Currency, [
            0xeed, # Gold Coin
            0xef0, # Copper Coin, Silver Coin
            0x1bc8, # Gold Nuggets
            0xe99, # Gem Pile
        ]),

        Organizer(source, UserContainers.Magery, [
            0xe84, # Rune Bag
            "Skull of",
            "Magic Rune Stone",
        ]),
        Organizer(source, UserContainers.Cartography, [
            0x14ec, # Treasure Map
            0x12ad, # Message in a Bottle
            0x14ed, # A Waterstained SOS
            "Magical Prison",
        ]),
        Organizer(source, UserContainers.Potions, [
            "Empty Bottle", # Empty Bottle
            0x282f, # All Mixtures?
            0x10b4, # Empty Jar
            "Potion",
            "Elixir",
            "Concoction",
            "Draught",
            "Ooze",
            "Mixture",
            "Embalming Fluid",
        ]),
        Organizer(source, UserContainers.Reagents, [
            "Ginseng",
            "Mandrake Root",
            "Sulfurous Ash",
            "Blood Moss",
            "Garlic",
            "Black Pearl",
            "Nightshade",
            "Spiders' Silk",

            "Grave Dust",
            "Nox Crystal",
            "Pig Iron",
            "Batwing",
            "Daemon Blood",
            #TypeFilter(0xf7d, 0), # Daemon Blood

            0xf19, # Mage Eye
            0xf78, # Dragon Tooth
            "Dragon's Blood",
            #TypeFilter(0xf7d, 1194), # Dragon Blood
            "Demon Claw",
            "Silver Widow",
            "Sea Salt",
            "Brimstone",
            "Moon Crystal",
            "Pixie Skull",
            "Vampire Thorn",
            "Fey Seed",
            "Butterfly Wings",
            "Gargoyle Ear",
            "Winter Berry",
            0xa96, # Enchanted Seaweed, Druidic Blade, Deepwater Stem
            0x2fe8, # Lotus Petal, Red Lotus, Flow Petal
            "Forest Hair",
            "Frog Leaf",
            "Mushroom",
            "Beetle Shell",
            "Eye of Toad",
            "Fairy Egg",
            "Cactus Sponge",
            "Desert Root",
            "Swamp Berries",
            "Dark Toadstool",
            "Purple Fungus",
            "Dragon Berry",
            "Life Root",
            "Earth Stem",
            All("jar of", Not("unidentified")),
            All("bottle of", Not("unidentified")),
        ]),

        Organizer(source, UserContainers.Resources_Cloth, [
            0x1767, # Folded Cloth
            0x1766, # Cloth
            0xf95, # Cloth Bolt
            0x1a9c, # Flax
        ]),
        Organizer(source, UserContainers.Resources_Metal, [
            0x1bf2, # Ingots
            0x1bf8, # Custom Ingot ("Block")
            0x19b9, # Large Ore
            0x19b7, # Small Ore
            0x26b4, # Crafting Scales
            0x26b2, # Smeltable Scales
            0x2158, # Granite
        ]),
        Organizer(source, UserContainers.Resources_Leather, [
            0x11f4, # Fur
            0x1081, # Leather or Skin
        ]),
        Organizer(source, UserContainers.Resources_Wood, [
            0x1bd7, # Boards
            0x1be0, # Logs
            0x4ccd, # Feathers
            TypeFilter(0xf7d, 1501), # Tree Sap
            TypeFilter(0xf7d, 2112), # Reaper Oil
        ]),
        Organizer(source, UserContainers.Fun, [
            "Magical Dye",
            "Jar of Dye",
            "Gender Change",
            "Oil of",
        ]),

        Organizer(source, UserContainers.Artifact_Weapon, [
            "artifact & weapon"
        ]),

        Organizer(source, UserContainers.Artifact_Other, [
            All("Artifact", Not("Weapon"))
        ]),
        Organizer(source, UserContainers.Magic_Instruments, [
            All(
                Any(FixedLists.Instruments),
                Any(
                    # Desirable Properties
                    "+", # Skill bonus
                    "Lower Reagent",
                    "Lower Mana",
                    FixedLists.Slayers
                ),
            ),
        ]),
        Organizer(source, UserContainers.Skill_Bonus, [ # Must come after Instruments
            "+" # Skill bonus
        ]),
    ]


#---------------------------------------
# System Configuration
#---------------------------------------
from services.filter.systemconfig import SystemConfig


#---------------------------------------
# Filter Abstractions - Do not touch
#---------------------------------------
from services.filter.core import *

def Not(filter):
    return NotFilter(filter)

def All(*filters):
    filter_list = []
    for filter in filters: filter_list.append(filter)
    return AllFilter(filter_list)

def Any(*filters):
    filter_list = []
    for filter in filters: filter_list.append(filter)
    return AnyFilter(filter_list)


#---------------------------------------
# Filters
#---------------------------------------
from services.filter.implementations import *


#---------------------------------------
# Filter Utilities
#---------------------------------------
from services.filter.utilities import *


#------------------------
# Lists of Items
#------------------------
from services.filter.fixedlists import FixedLists


#------------------------
# Organizer
#------------------------
from services.filter.organizer import Organizer


#------------------------
# Alias Utilities
#------------------------
class AliasUtils:
    @classmethod
    def GetSerial(cls, alias_or_serial):
        if isinstance(alias_or_serial, int): return alias_or_serial
        if not FindAlias(alias_or_serial): return None
        
        return GetAlias(alias_or_serial)

    @classmethod
    def AsString(cls, alias_or_serial):
        if isinstance(alias_or_serial, int): return hex(alias_or_serial)
        return alias_or_serial

    @classmethod
    def GetBackpackSerial(cls, alias_or_serial):
        serial = cls.GetSerial(alias_or_serial)
        if UOMath.IsMobile(serial):
            mobile = Engine.Mobiles.GetMobile(serial)
            if mobile: return mobile.Backpack # Set the backpack if it exists
        
        return alias_or_serial


#------------------------
# Item Utilities
#------------------------
class ItemUtils:
    @classmethod
    def GetItemsRecursive(cls, source_container, items, process_item_predicate, include_children = True):
        for item in source_container.GetItems():
            if not process_item_predicate(item): continue

            if include_children and cls.HasProperty(item.Properties, "contents:"):
                container = cls.OpenContainer(item.Serial)
                if container == None: continue
                
                cls.GetItemsRecursive(container, items, process_item_predicate, include_children)
            else:
                items.append(item)
    
    @classmethod
    def HasProperty(cls, properties, substring): 
        for property in properties:
            if substring in property.Text.ToLower(): return True
        return False


    @classmethod
    def OpenContainer(cls, alias_or_serial):
        alias_or_serial = AliasUtils.GetSerial(alias_or_serial)
        if not isinstance(alias_or_serial, int): alias_or_serial = GetAlias(alias_or_serial)
        
        item = Engine.Items.GetItem(alias_or_serial)
        if item == None:
            SysMessage("Failed to find container ({})".format(AliasUtils.AsString(alias_or_serial)))
            return None
            
        UseObject(item)
        #WaitForContents(item, 5000)
        Pause(1000)

        return item.Container


    @classmethod
    def HasCapacity(cls, alias_or_serial, reserved_space = 5):
        container = Engine.Items.GetItem(alias_or_serial)
        if container == None: return False

        for property in container.Properties:
            if property.Text.startswith("Contents"): # Contents: #min/#max items, #min/max stones
                args = property.Arguments
                return int(args[0]) < int(args[1]) - reserved_space # Current/Max
        return False


from utility.movement import Runner


#------------------------
# Runner
#------------------------
class OrganizerRunner:
    def Validate(self, organizers):
        for organizer in organizers:
            if not self.__getDestination(organizer.destination):
                SysMessage("Failed to open Destination ({}).".format(organizer.destination))

    def Process(self, organizers, ignored_filter):
        # Aggregate by Source and Destination
        organizers_by_source = self.__groupBySource(organizers)
        for source in organizers_by_source:
            source_container = ItemUtils.OpenContainer(source)
            if not source_container:
                SysMessage("Failed to open Source ({}).".format(source))
                return

            # Get all the items
            items = []
            ItemUtils.GetItemsRecursive(source_container, items, lambda item: ignored_filter == None or not ignored_filter.Test(item), UserOptions.Open_Child_Containers)
            total_items = len(items)

            # Process the list of items
            for i, item in enumerate(items):
                SysMessage("Processing item ({} of {}).".format(i + 1, total_items))
                if ignored_filter != None and ignored_filter.Test(item): continue # TODO: Can this be removed?

                for organizer in organizers_by_source[source]:
                    if organizer.Test(item):
                        # Find the first container with capacity
                        destination = self.__getDestination(organizer.destination)
                        if destination == None:
                            # TODO: Verify lists will print correctly
                            SysMessage("Skipping organizer. Failed to Destination with capacity ({}).".format(AliasUtils.AsString(destination)))
                            continue
                        
                        if UserOptions.Move_To_Destination:
                            if not self.__moveToDestination(destination):
                                SysMessage("Failed to move to Destination ({}).".format(AliasUtils.AsString(destination)))

                        if UserOptions.Output_Item_Move_Messages: SysMessage("Moved ({}) to ({})".format(item.Name, AliasUtils.AsString(destination)))

                        MoveItem(item, destination)
                        Pause(1000)
                        break


    def __getDestination(self, destinations):
        if not isinstance(destinations, list): return destinations

        for destination in destinations:
            if ItemUtils.HasCapacity(destination): return destination

        return None


    def __groupBySource(self, organizers):
        organizers_by_source = {}
        for organizer in organizers:
            if organizer.destination == None: continue

            if not organizer.source in organizers_by_source:
                organizers_by_source[organizer.source] = []
            
            organizers_by_source[organizer.source].append(organizer)
        
        return organizers_by_source
    
    
    def __moveToDestination(self, destination_alias):
        if destination_alias == SystemContainers.PlayerBank:
            vault_type_id = 0x436
            if not FindType(vault_type_id, 7):
                SysMessage("Failed to find Vault.")
                return False

            vault_id = GetAlias("found")
            if not Runner.MoveTo(vault_id):
                SysMessage("Failed to move to Vault.")
                return False
            
            UseObject(vault_id)
            Pause(1000)

        elif destination_alias != SystemContainers.PlayerBackpack:
            # Convert destination to Serial if necessary
            destination = AliasUtils.GetSerial(destination_alias)
            if not destination:
                SysMessage("Failed to find Destination ({}).".format(AliasUtils.AsString(destination)))
                return False

            # Move
            if not Runner.MoveTo(destination): return False
        
        return True

#------------------------
# Main
#------------------------
def Main():
    ignored_filter = None
    ignored_filters = GetIgnoredFilters()
    if 0 < len(ignored_filters):
        FilterUtils.ResolveFilters(ignored_filters, SystemConfig.AndOperatorCharacter)
        ignored_filter = AnyFilter(ignored_filters)

    organizers = GetOrganizers()

    # Check if we need to prompt
    UnsetAlias(SystemContainers.PromptForSource)
    if any(organizer.source == SystemContainers.PromptForSource for organizer in organizers):
            container = AliasUtils.GetBackpackSerial(PromptMacroAlias("$SourceContainer"))
            SetAlias(SystemContainers.PromptForSource, container)

    for organizer in organizers:
        # Convert any shorthand
        FilterUtils.ResolveFilters(organizer.filters, SystemConfig.AndOperatorCharacter)
        if SystemConfig.LogFilterSummary: print(map(str, organizer.filters))
    
    runner = OrganizerRunner()
    runner.Process(organizers, ignored_filter)
    
    HeadMsg("Execution Completed")

# Execute Main
Main()