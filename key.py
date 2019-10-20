from item import Item

class Key(Item):
    """docstring for Key."""

    def __init__(self, name, target):
        super(Key, self).__init__(name, "key")
        self.target = target
