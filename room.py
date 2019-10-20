class Room():

    def __init__(self, name):
        self.name = name

    def get_room_items(self, map):
        room_items =  map.object_relations[self.name]
        return room_items

    def get_room_name(self):
        return self.name

    def get_item(self, map, item_name):
        return map.get_item_by_name(item_name, self.name)
