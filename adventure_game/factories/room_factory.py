from adventure_game.models import Room
from adventure_game.models.contracts import IRoom
from adventure_game.factories.contracts import IRoomFactory
import adventure_game.constants as constants


class RoomFactory(IRoomFactory):
    def __init__(self):
        pass

    def create_room_exits(self, east_room_id=None, west_room_id=None, north_room_id=None, south_room_id=None):
        return {
            constants.DIRECTION_EAST: east_room_id,
            constants.DIRECTION_WEST: west_room_id,
            constants.DIRECTION_NORTH: north_room_id,
            constants.DIRECTION_SOUTH: south_room_id
        }

    def create_room(self, room_id, name, description, exits=None, items=[], puzzles=[]) -> IRoom:
        if not exits:
            exits = self.create_room_exits()

        return Room(room_id,
                    name,
                    description,
                    items,
                    exits[constants.DIRECTION_EAST],
                    exits[constants.DIRECTION_WEST],
                    exits[constants.DIRECTION_NORTH],
                    exits[constants.DIRECTION_SOUTH],
                    puzzles)
