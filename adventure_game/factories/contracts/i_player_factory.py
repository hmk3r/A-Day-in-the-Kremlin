from abc import ABCMeta, abstractmethod


class IPlayerFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_player(self, name, location, inventory=None):
        pass
