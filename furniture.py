from item import Item

class Furniture(Item):

    def __init__(self, name):
        super(Furniture, self).__init__(name, "furniture")

    def examine_item(self, game_state, map):
        if self.name in map.object_relations and len(map.object_relations[self.name]) > 0:
            item_found = map.object_relations[self.name].pop()
            return item_found
        else:
            return None
