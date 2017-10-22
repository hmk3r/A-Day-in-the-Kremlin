from adventure_game.models.contracts import IRoom


class Room(IRoom):
    def __init__(self,
                 room_id,
                 name=None,
                 description=None,
                 items=None,
                 exits=None,
                 puzzles=None):

        self._id = room_id
        self._name = name
        self._description = description
        self._items = items if items else []
        self._exits = exits if exits else {}
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
