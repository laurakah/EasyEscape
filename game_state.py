class GameState(object):
    """docstring for GameState."""

    def __init__(self, start_room, target_room):
        self.start_room = start_room
        self.target_room = target_room
        self.keys_collected = []
        self.current_room = start_room

    def check_for_key(self, door):
        have_key = False
        for key in self.keys_collected:
            if key.target == door:
                have_key = True
        return have_key
