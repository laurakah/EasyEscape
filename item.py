class Item():

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def examine_item(self, game_state, map):
        raise Exception("Calling examine_item method on non type item is not possible.")
