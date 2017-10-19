from adventure_game.models.contracts import IItem


class Item(IItem):

    def __init__(self, item_id, name, description):
        self.id = item_id
        self.name = name
        self.description = description
