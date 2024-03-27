from diagnostic.logger import Logger


class BODContext:
    def __init__(self):
        self.is_large = None
        self.require_exceptional = None
        self.require_amount = None
        self.require_resource = None # Optional
        self.items_counts_by_name = {}


    def __str__(self):
        values = [
            "Large BOD" if self.is_large else "Small BOD",
            "Requires exceptional" if self.require_exceptional else "Optional exceptional",
            "{}".format(self.require_resource) if self.require_resource else "unknown resource",
        ]

        require_amount = self.require_amount if self.require_amount else "unknown amount"
        for item_name, count in self.items_counts_by_name.items():
            values.append("{} ({} / {})".format(item_name, count, require_amount))

        return "\n".join(values)

    
    def GetRemainingAmount(self, item_name):
        current = self.items_counts_by_name[item_name]
        return self.require_amount - current if current != None else 0


    def GetIncompleteItem(self):
        for item_name in self.items_counts_by_name.keys():
            if 0 < self.GetRemainingAmount(item_name): return item_name

        return None


    def IsComplete(self):
        return True if self.require_amount and not self.GetIncompleteItem() else False


class BODFactory:
    @classmethod
    def Create(cls, item):
        context = BODContext()
        for property in item.Properties:
            if not cls.__is_type_set(context): # Find BOD Size
                Logger.Debug("Looking for Type: " + property.Text)
                if "large bulk order" in property.Text:
                    context.is_large = True
                elif "small bulk order" in property.Text:
                    context.is_large = False
                continue

            if not cls.__is_exceptional_set(context): # Try to set Exceptional
                Logger.Debug("Looking for Exceptional: " + property.Text)
                exceptional_line = "All items must be exceptional."
                if exceptional_line == property.Text: context.require_exceptional = True
                if cls.__is_exceptional_set(context): continue # If it's set, nothing else can be on this line

            if not cls.__is_resource_set(context): # Try to set Resource
                Logger.Debug("Looking for Resource: " + property.Text)
                resource_line = "crafted with "
                resource_index = property.Text.IndexOf(resource_line)
                if 0 <= resource_index:
                    context.require_resource = property.Text[resource_index + len(resource_line):]
                    if not cls.__is_exceptional_set(context): context.require_exceptional = False # If not set by now, Exceptional is not required
                    continue # If it's set, nothing else can be on this line

            # Discard properties until we know the amount crafted
            if not cls.__is_amount_set(context):
                Logger.Debug("Looking for Amount: " + property.Text)
                if not property.Text.startswith("amount"): continue
                amount_line = "amount to make: "
                context.require_amount = int(property.Text[len(amount_line):])
                continue


            # Items
            Logger.Debug("Looking for Item and Count: " + property.Text)
            item_name, count = property.Text.Split(":")
            context.items_counts_by_name[item_name] = int(count)
        
        return context if cls.__is_type_set(context) else None


    @staticmethod
    def __is_amount_set(context):
        return context.require_amount != None


    @staticmethod
    def __is_exceptional_set(context):
        return context.require_exceptional != None


    @staticmethod
    def __is_resource_set(context):
        return context.require_resource != None


    @staticmethod
    def __is_type_set(context):
        return context.is_large != None