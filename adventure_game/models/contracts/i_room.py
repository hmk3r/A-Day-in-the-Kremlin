from abc import ABCMeta, abstractmethod


class IRoom(metaclass=ABCMeta):
    id = ""
    name = ""
    description = ""
    exits = {}
    items = []

    @abstractmethod
    def is_completed(self):
        pass
