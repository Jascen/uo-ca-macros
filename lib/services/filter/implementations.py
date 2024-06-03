from services.filter.core import MetaFilterBase, MultiFilterBase
class NameFilter:
    """
    - A case-insensitive partial string match against an item's `Name`
        - `name` - The string to search for
        - `hue` - Optional. If provided, the item must have this hue to pass the Filter
        - `partial_match` - Optional. If `False`, the item name must exactly match the provided value
    """
    def __init__(self, name, hue = -1, partial_match = True):
        self.name = name
        self.name_normalized = name.ToLower()
        self.hue = hue
        self.partial_match = partial_match
    
    @classmethod
    def PartialSearch(cls, item, name_normalized):
        return item.Name.ToLower().Contains(name_normalized)
    
    def Test(self, item):
        if self.hue != -1 and self.hue != item.Hue: return False
        if self.partial_match: return self.PartialSearch(item, self.name_normalized)
        return item.Name.ToLower() == self.name_normalized

    def __str__(self):
        name = "Partial Name" if self.partial_match else "Name"
        return "{} ({})".format(name, self.name_normalized)

class MaxPropertyCountFilter:
    """
    - A count of the number of properties
        - `max_count` - The maximum number of properties an item can have
    """
    def __init__(self, max_count):
        self.max_count = max_count
    
    def Test(self, item):
        return len(item.Properties) <= self.max_count

    def __str__(self):
        return "Max Props ({})".format(self.max_count)

class PropertyFilter:
    """
    - A case-insensitive partial string match against an item's `Properties`
        - `property` - The string value to search for
        - `hue` - Optional. If provided, the item must have this hue to pass the Filter
        - `partial_match` - Optional. If `False`, the item property must exactly match the provided value
    """
    def __init__(self, property, hue = -1, partial_match = True):
        self.property = property
        self.property_normalized = property.ToLower()
        self.hue = hue
        self.partial_match = partial_match
    
    def Test(self, item):
        if self.hue != -1 and self.hue != item.Hue: return False

        return self.__hasProperty(item.Properties, self.property_normalized, self.partial_match)

    def __hasProperty(self, properties, value, partial_match):
        if not properties: return False
        
        for property in properties:
            if partial_match:
                if value in property.Text.ToLower(): return True
            else:
                if value == property.Text.ToLower(): return True
        return False

    def __str__(self):
        name = "Partial Prop" if self.partial_match else "Prop"
        return "{} ({})".format(name, self.property_normalized)

class PropertyValueFilter:
    """
    - Exact match against a specific property
        - `property` - The exact name of the property
        - `value` - The numeric or string value to search for
    """
    def __init__(self, property, value):
        self.property = property
        self.value = value
        self.is_numeric = not isinstance(value, str)
    
    def Test(self, item):
        return self.HasValue(item, self.property, self.value, self.is_numeric)

    @classmethod
    def HasValue(self, item, property, value, is_value_numeric):
        property_value = getattr(item, property)
        if is_value_numeric: property_value = int(property_value)

        return property_value == value

    def __str__(self):
        name = "#" if self.is_numeric else "Str"
        return "{} Prop Val ({})".format(name, self.property)
    
class SerialFilter:
    """
    - Exact match against an item's `Serial`
        - `serial` - The ID to search for
    """
    def __init__(self, serial):
        self.serial = serial
    
    def Test(self, item):
        return item.Serial == self.serial

    def __str__(self):
        return "Serial ({})".format(self.serial)

class TypeFilter:
    """
    - Exact match against an item `Graphic` or `ID`
        - `type_id` - The item must have this Graphic or ID
        - `hue` - Optional. If provided, the item must have this hue to pass the Filter
    """
    def __init__(self, type_id, hue = -1):
        self.type_id = type_id
        self.hue = hue
    
    def Test(self, item):
        return (self.hue == -1 or self.hue == item.Hue) and item.ID == self.type_id

    def __str__(self):
        return "Type ({})".format(hex(self.type_id))

class TypeRangeFilter:
    """
    - Requires an item `Graphic` or `ID` to be >= starting ID and <= ending ID
        - `type_start` - The starting graphic ID
        - `type_end` - The ending graphic ID

    """
    def __init__(self, type_start, type_end):
        self.type_start = type_start
        self.type_end = type_end
    
    def Test(self, item):
        return self.type_start <= item.ID and item.ID <= self.type_end

    def __str__(self):
        return "Type Range ({} to {})".format(hex(self.type_start), hex(self.type_end))

class NotFilter(MetaFilterBase):
    """
    - Inverts the response of the provided Filter
        - `filter` - A single Filter to check
    """
    def __init__(self, filter):
        MetaFilterBase.__init__(self, filter)

    def Test(self, item):
        return not self.filter.Test(item)

    def __str__(self):
        return "Not: {}".format(self.filter)

class AllFilter(MultiFilterBase): # AND
    """
    - All provided Filters must pass in order for the item to be moved
        - `filters` - An array of Filters to check
    """
    def __init__(self, filters):
        MultiFilterBase.__init__(self, filters)
    
    def Test(self, item):
        for filter in self.filters:
            if not filter.Test(item): return False
        return True

class AnyFilter(MultiFilterBase): # OR
    """
    - At least one Filter must pass in order for the item to be moved
        - `filters` - A list of Filters to check
    """
    def __init__(self, filters):
        MultiFilterBase.__init__(self, filters)
    
    def Test(self, item):
        for filter in self.filters:
            if filter.Test(item): return True
        return False