from abc import ABCMeta, abstractmethod


class IPlayer(metaclass=ABCMeta):
    name = ""
    location = None
    inventory = []

    @abstractmethod
    def take_item(self, item):
        pass

    @abstractmethod
    def drop_item(self, item):
        pass

    @abstractmethod
    def move_to(self, location):
        pass
