from adventure_game.factories.contracts import IItemFactory
from adventure_game.models import Item


class ItemFactory(IItemFactory):
    def create_item(self, item_id, name, description):
        return Item(item_id, name, description)
