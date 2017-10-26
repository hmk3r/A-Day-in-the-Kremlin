from abc import ABCMeta, abstractmethod


class IRoomFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_room(self, room_id, name, description, exits=None, items=None, puzzles=None):
        pass
