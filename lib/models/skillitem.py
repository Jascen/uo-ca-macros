class SkillItem:
    """An item that can be crafted for skill gains if done within the supplied skill range"""
    def __init__(self, general_or_craft_menu_item, craft_resource_item_or_array, min_level, max_level):
        self.item = general_or_craft_menu_item
        self.min_level = min_level
        self.max_level = max_level

        if not isinstance(craft_resource_item_or_array, list): craft_resource_item_or_array = [craft_resource_item_or_array] # Convert a single entity into an array
        self.resources = craft_resource_item_or_array


    def clone(self):
        return SkillItem(self.item.name, self.craft_resource_item_or_array, self.min_level, self.max_level)


    def __str__(self):
        return "{} ({} to {})".format(self.item.name, self.min_level, self.max_level)