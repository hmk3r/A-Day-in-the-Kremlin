from abc import ABCMeta, abstractmethod

from adventure_game.models.contracts import IRoom


class IRoomFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_room(self, room_id, name, description, exits=None, items=None, puzzles=None) -> IRoom:
        pass
