from abc import ABCMeta, abstractmethod


class IPlayer(metaclass=ABCMeta):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def location(self):
        pass

    @location.setter
    @abstractmethod
    def location(self, value):
        pass

    @property
    @abstractmethod
    def inventory(self):
        pass

    @abstractmethod
    def take_item(self, item):
        pass

    @abstractmethod
    def drop_item(self, item):
        pass

    @abstractmethod
    def move_to(self, location):
        pass
