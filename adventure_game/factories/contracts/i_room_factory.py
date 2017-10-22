from abc import ABCMeta, abstractmethod

from adventure_game.models.contracts import IRoom


class IRoomFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_room_exits(self, east_room_id=None, west_room_id=None, north_room_id=None, south_room_id=None):
        pass

    @abstractmethod
    def create_room(self, room_id, name, description, exits=None, items=None, puzzles=None) -> IRoom:
        pass
