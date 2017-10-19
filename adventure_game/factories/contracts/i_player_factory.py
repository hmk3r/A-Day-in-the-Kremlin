from abc import ABCMeta, abstractmethod
from adventure_game.models.contracts import IPlayer, IRoom
from adventure_game.models import Player


class IPlayerFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_player(self, name, location: IRoom, inventory=[]) -> IPlayer:
        return Player(name, location, inventory)
