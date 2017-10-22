from adventure_game.factories.contracts import IPlayerFactory
from adventure_game.models.contracts import IPlayer, IRoom
from adventure_game.models import Player


class PlayerFactory(IPlayerFactory):
    def create_player(self, name, location: IRoom, inventory=None) -> IPlayer:
        return Player(name, location, inventory)
