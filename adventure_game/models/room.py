from adventure_game.models.contracts import IRoom
import adventure_game.constants as constants


class Room(IRoom):
    def __init__(self,
                 room_id,
                 name,
                 description,
                 items=[],
                 east_room_id=None,
                 west_room_id=None,
                 north_room_id=None,
                 south_room_id=None,
                 puzzles=[]):

        self.id = room_id
        self.name = name
        self.description = description
        self.items = items
        self.exits = self._create_exist_scheme(east_room_id, west_room_id, north_room_id, south_room_id)
        self.puzzles = puzzles

    def is_completed(self):
        return True

    @staticmethod
    def _create_exist_scheme(east_room_id=None, west_room_id=None, north_room_id=None, south_room_id=None):
        return {
            constants.DIRECTION_EAST: east_room_id,
            constants.DIRECTION_WEST: west_room_id,
            constants.DIRECTION_NORTH: north_room_id,
            constants.DIRECTION_SOUTH: south_room_id
        }
