from abc import ABCMeta, abstractmethod


class IRoom(metaclass=ABCMeta):
    @property
    @abstractmethod
    def id(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @description.setter
    @abstractmethod
    def description(self, value):
        pass

    @property
    @abstractmethod
    def exits(self):
        pass

    @property
    @abstractmethod
    def items(self):
        pass

    @property
    @abstractmethod
    def puzzles(self):
        pass

    @property
    @abstractmethod
    def is_completed(self):
        pass
