from item import Item

class Key(Item):

    def __init__(self, name, target):
        super(Key, self).__init__(name, "key")
        self.target = target
