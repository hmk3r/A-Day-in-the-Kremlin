from adventure_game.models.contracts import IPlayer, IRoom


class Player(IPlayer):

    def __init__(self, name, location: IRoom, inventory=None):
        self._name = name
        self._location = location
        self._inventory = inventory if inventory else []

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def name(self):
        return self._name

    @property
    def inventory(self):
        return self._inventory

    def take_item(self, item):
        self.inventory.append(item)

    def drop_item(self, item):
        self.inventory.remove(item)

    def move_to(self, location):
        self.location = location
