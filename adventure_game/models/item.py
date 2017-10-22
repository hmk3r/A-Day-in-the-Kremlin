from adventure_game.models.contracts import IItem


class Item(IItem):
    def __init__(self, item_id, name, description):
        self._id = item_id
        self._name = name
        self._description = description

    @property
    def description(self):
        return self._description

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
