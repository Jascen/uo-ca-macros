from services.scavenger import Scavenger
from utility.item import ItemUtils


def Main():
    item_type_id = ItemUtils.PromptForType()

    scavenger = Scavenger("backpack")
    scavenger.Loot(item_type_id, 15)


# Execute Main()
Main()