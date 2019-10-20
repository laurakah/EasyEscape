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

    def start_game(self):
        self.clear()
        print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
        room = self.game_state.current_room
        while not room == self.game_state.target_room:
            print("You are now in " + room.get_room_name())
            intended_action = input("What would you like to do? Type 'explore' or 'examine'?").strip()
            if intended_action == "explore":
                room_items = room.get_room_items(self.map)
                item_names = [item.name for item in room_items]
                self.clear()
                print("You explore the room. This is " + room.name + ". You find " + ", ".join(item_names))
                continue
            if intended_action == "examine":
                item_selected = input("What would you like to examine?").strip()
                item = room.get_item(self.map, item_selected)
                if not item:
                    self.clear()
                    print("The item you requested is not found in the current room.")
                    continue
                self.clear()
                print("You examine " + item.name + ". ")
                item_examined = item.examine_item(self.game_state, self.map)
                if item.type == "door" and not item_examined:
                    print("It is locked but you don't have the key.")
                elif item.type == "door" and item_examined:
                    print("You unlock it with a key you have.")
                    next_room = self.map.get_next_room_of_door(self.game_state, item)
                    if (next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes'):
                        room = next_room
                        self.game_state.current_room = next_room
                        continue
                elif item.type == "furniture" and not item_examined:
                    print("There isn't anything interesting about it.")
                elif item.type == "furniture" and item_examined:
                    self.game_state.keys_collected.append(item_examined)
                    print("You find the " + item_examined.name + ".")
            else:
                self.clear()
                print("Not sure what you mean. Type 'explore' or 'examine'.")
        self.clear()
        print("Congrats! You escaped the room!")

if __name__ == "__main__":
    game = Game()
    game.start_game()
