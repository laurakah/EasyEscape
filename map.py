class Map(object):
    """docstring for Map."""

    def __init__(self):
        self.object_relations = {}
        self.start_room = None
        self.end_room = None

    def get_next_room_of_door(self, game_state, door):
        connected_rooms = self.object_relations[door.name]
        for room in connected_rooms:
            if not game_state.current_room == room:
                return room

    def get_item_by_name(self, item_name, room_name):
        item = None
        for item_available in self.object_relations[room_name]:
            if not item_available.name == item_name:
                continue
            item = item_available
            break
        return item

    def add_relation(self, name, item_list):
        self.object_relations.update({name: item_list})

    def set_start_room(self, start_room):
        self.start_room = start_room

    def get_start_room(self):
        return self.start_room

    def set_end_room(self, end_room):
        self.end_room = end_room

    def get_end_room(self):
        return self.end_room
