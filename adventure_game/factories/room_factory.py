from adventure_game.models import Room


class RoomFactory:
    def __init__(self, constants):
        self.constants = constants
        pass

    def get_room_exits(self, east_room_id=None, west_room_id=None, north_room_id=None, south_room_id=None):
        return {
            self.constants.DIRECTION_EAST: east_room_id,
            self.constants.DIRECTION_WEST: west_room_id,
            self.constants.DIRECTION_NORTH: north_room_id,
            self.constants.DIRECTION_SOUTH: south_room_id
        }

    def get_room(self, room_id, name, description, exits=None, items=[]):
        if not exits:
            exits = self.get_room_exits()

        return Room(room_id, name, description, exits, items)
