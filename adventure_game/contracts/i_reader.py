from abc import ABCMeta, abstractmethod


class IReader(metaclass=ABCMeta):
    @abstractmethod
    def read_input(self, prompt):
        pass
