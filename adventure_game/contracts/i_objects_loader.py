from abc import ABCMeta, abstractmethod


class IObjectsLoader(metaclass=ABCMeta):
    @abstractmethod
    def load(self):
        pass
