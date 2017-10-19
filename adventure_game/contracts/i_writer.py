from abc import ABCMeta, abstractmethod


class IWriter(metaclass=ABCMeta):
    @abstractmethod
    def write(self, text):
        pass

    @abstractmethod
    def write_separator(self):
        pass
