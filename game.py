from game_state import GameState
from map import Map
from key import Key
from furniture import Furniture
from door import Door
from room import Room

class Game():
    """docstring for Game."""

    def __init__(self):
        self.map = Map()
        self.populate_map(self.map)
        self.game_state = GameState(self.map.get_start_room(), self.map.get_end_room())

        self.MSG = {
            "start game": "You wake up on a couch and find yourself in a strange house with no windows in which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!",
            "successfully escaped": "Congrats! You escaped the house!",
            "invalid action": "Not sure what you mean. Type 'explore' or 'examine'.",
            "nothing found": "There isn't anything interesting about it.",
            "unlock door": "You unlock it with a key you have.",
            "locked door": "It is locked but you don't have the key.",
            "item not in romm": "The item you requested is not found in the current room.",
            "found in room": "You explore the room. This is %s. You find %s",
            "current room": "You are now in %s",
            "item found": "You find the %s.",
            "examine": "You examine %s.",

            # input strings
            "what to examine": "What would you like to examine? >>> ",
            "go to next room": "Do you want to go to the next room? Enter 'yes' or 'no' >>> ",
            "examine or explore": "What would you like to do? Type 'explore' or 'examine'? >>> "

        }

    def populate_map(self, map):
        # define rooms and items
        # furniture
        couch = Furniture("couch")
        piano = Furniture("piano")
        double_bed = Furniture("double bed")
        queen_bed = Furniture("queen bed")
        dresser = Furniture("dresser")
        dining_table = Furniture("dining table")

        # doors
        door_a = Door("door a")
        door_b = Door("door b")
        door_c = Door("door c")
        door_d = Door("door d")

        # keys
        key_a = Key("key for door a", door_a)
        key_b = Key("key for door b", door_b)
        key_c = Key("key for door c", door_c)
        key_d = Key("key for door d", door_d)

        # rooms
        game_room = Room("game room")
        bedroom_1 = Room("bedroom 1")
        bedroom_2 = Room("bedroom 2")
        living_room = Room("living room")
        outside = Room("outside")

        # setting start and end rooms
        map.set_start_room(game_room)
        map.set_end_room(outside)

        # object relations
        map.add_relation("game room", [couch, piano, door_a])
        map.add_relation("bedroom 1", [queen_bed, door_a, door_b, door_c])
        map.add_relation("bedroom 2", [double_bed, dresser, door_b])
        map.add_relation("living room", [dining_table, door_c, door_d])
        map.add_relation("outside", [door_d])
        map.add_relation("piano", [key_a])
        map.add_relation("double bed", [key_c])
        map.add_relation("dresser", [key_d])
        map.add_relation("queen bed", [key_b])
        map.add_relation("door a", [game_room, bedroom_1])
        map.add_relation("door b", [bedroom_1, bedroom_2])
        map.add_relation("door c", [bedroom_1, living_room])
        map.add_relation("door d", [living_room, outside])


    def clear(self):
        print("\033[2J")

    def print_msg(self, msg, do_clear=False):
        if do_clear:
            self.clear()
        print(msg)

    def _ask_for_item(self):
        item_selected = input(self.MSG["what to examine"]).strip()
        return item_selected

    def _item_not_found(self):
        self.print_msg(self.MSG["item not in room"], do_clear=True)

    def _examine_item_found(self, item):
        self.print_msg(self.MSG["examine"] % item.name)
        item_examined = item.examine_item(self.game_state, self.map)
        return item_examined

    def _get_next_room(self, item):
        next_room = self.map.get_next_room_of_door(self.game_state, item)
        return next_room

    def _do_go_to_next_room(self):
        answer = input(self.MSG["go to next room"]).strip()
        if answer == "yes":
            return True
        return False

    def _update_current_room(self, next_room):
        self.game_state.current_room = next_room
        return next_room

    def _door_have_no_key(self):
        self.print_msg(self.MSG["locked door"])

    def _door_have_key(self):
        self.print_msg(self.MSG["unlock door"])

    def _furniture_key_found(self, item_examined):
        self.game_state.keys_collected.append(item_examined)
        self.print_msg(self.MSG["item found"] % item_examined.name)

    def _furniture_no_key_found(self):
        self.print_msg(self.MSG["nothing found"])

    def _ask_for_action(self):
        intended_action = input(self.MSG["examine or explore"]).strip()
        return intended_action

    def _explore(self, room):
        room_items = room.get_room_items(self.map)
        item_names = [item.name for item in room_items]
        self.clear()
        self.print_msg(self.MSG["found in room"] % (room.name, ", ".join(item_names)))

    def _examine(self, room):
        item_selected = self._ask_for_item()
        item = room.get_item(self.map, item_selected)
        if not item:
            self._item_not_found()
        self.clear()
        item_examined = self._examine_item_found(item)
        if item.type == "door" and not item_examined:
            self._door_without_key()
        elif item.type == "door" and item_examined:
            self._door_have_key()
            next_room = self._get_next_room(item)
            if next_room and self._do_go_to_next_room():
                self._update_current_room(next_room)
        elif item.type == "furniture" and not item_examined:
            self._furniture_no_key_found()
        elif item.type == "furniture" and item_examined:
            self._furniture_key_found(item_examined)

    def start_game(self):
        self.print_msg(self.MSG["start game"], do_clear=True)
        while not self.game_state.current_room == self.game_state.target_room:
            self.print_msg(self.MSG["current room"] % self.game_state.current_room.get_room_name())
            intended_action = self._ask_for_action()
            if intended_action == "explore":
                self._explore(self.game_state.current_room)
                continue
            if intended_action == "examine":
                self._examine(self.game_state.current_room)
            else:
                self.print_msg(self.MSG["invalid action"], do_clear=True)
        self.print_msg(self.MSG["successfully escaped"], do_clear=True)
