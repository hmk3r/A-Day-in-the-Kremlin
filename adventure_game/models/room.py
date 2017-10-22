from adventure_game.models.contracts import IRoom
import adventure_game.constants as constants


class Room(IRoom):
    def __init__(self,
                 room_id,
                 name,
                 description,
                 items=None,
                 east_room_id=None,
                 west_room_id=None,
                 north_room_id=None,
                 south_room_id=None,
                 puzzles=None):

        self._id = room_id
        self._name = name
        self._description = description
        self._items = items if items else []
        self._exits = self._create_exist_scheme(east_room_id, west_room_id, north_room_id, south_room_id)
        self._puzzles = puzzles if puzzles else []

    @property
    def puzzles(self):
        return self._puzzles

    @property
    def exits(self):
        return self._exits

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def name(self):
        return self._name

    @property
    def items(self):
        return self._items

    @property
    def id(self):
        return self._id

    @property
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
