from adventure_game.models.contracts import IPlayer, IRoom


class Player(IPlayer):
    def __init__(self, name, location: IRoom, inventory=[]):
        self.name = name
        self.location = location
        self.inventory = inventory

    def take_item(self, item):
        self.inventory.append(item)

    def drop_item(self, item):
        self.inventory.remove(item)

    def move_to(self, location):
        self.location = location
