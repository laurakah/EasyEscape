from item import Item

class Door(Item):
    """docstring for Door."""

    def __init__(self, name):
        super(Door, self).__init__(name, "door")
        self.name = name

    def examine_item(self, game_state, map):
        if game_state.check_for_key(self):
            return True
        else:
            return None
