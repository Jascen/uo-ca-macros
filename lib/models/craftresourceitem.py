class CraftResourceItem:
    """An item that is required for crafting"""
    def __init__(self, graphic, name, hue, min_pack_amount, restock_amount):
        self.graphic = graphic
        self.name = name
        self.hue = hue
        self.min_pack_amount = min_pack_amount
        self.restock_amount = restock_amount


    def clone(self):
        return CraftResourceItem(self.graphic, self.name, self.hue, self.min_pack_amount, self.restock_amount)


    def __str__(self):
        return self.name