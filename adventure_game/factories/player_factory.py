from adventure_game.factories.contracts import IPlayerFactory
from adventure_game.models import Player


class PlayerFactory(IPlayerFactory):
    def create_player(self, name, location, inventory=None):
        return Player(name, location, inventory)
