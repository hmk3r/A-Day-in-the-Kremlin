from abc import ABCMeta, abstractmethod


class IItemFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_item(self, item_id, name, description):
        pass
