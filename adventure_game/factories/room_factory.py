from adventure_game.models import Room
from adventure_game.models.contracts import IRoom
from adventure_game.factories.contracts import IRoomFactory


class RoomFactory(IRoomFactory):
    def __init__(self, constants):
        self.constants = constants
        pass

    def create_room_exits(self, east_room_id=None, west_room_id=None, north_room_id=None, south_room_id=None):
        return {
            self.constants.DIRECTION_EAST: east_room_id,
            self.constants.DIRECTION_WEST: west_room_id,
            self.constants.DIRECTION_NORTH: north_room_id,
            self.constants.DIRECTION_SOUTH: south_room_id
        }

    def create_room(self, room_id, name, description, exits=None, items=[]) -> IRoom:
        if not exits:
            exits = self.create_room_exits()

        return Room(room_id, name, description, exits, items)
