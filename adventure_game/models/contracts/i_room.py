from abc import ABCMeta


class IRoom(metaclass=ABCMeta):
    id = ""
    name = ""
    description = ""
    exits = {}
    items = []
