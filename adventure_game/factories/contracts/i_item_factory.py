from abc import ABCMeta, abstractmethod
from adventure_game.models.contracts import IItem


class IItemFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_item(self, item_id, name, description) -> IItem:
        pass
