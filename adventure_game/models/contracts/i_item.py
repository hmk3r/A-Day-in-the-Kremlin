from abc import ABCMeta, abstractmethod


class IItem(metaclass=ABCMeta):
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
