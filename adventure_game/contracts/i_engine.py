from abc import ABCMeta, abstractmethod


class IEngine(metaclass=ABCMeta):
    @abstractmethod
    def run(self):
        pass
