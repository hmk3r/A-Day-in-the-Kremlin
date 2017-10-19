from abc import ABCMeta


class IItem(metaclass=ABCMeta):
    id = ""
    name = ""
    description = ""
