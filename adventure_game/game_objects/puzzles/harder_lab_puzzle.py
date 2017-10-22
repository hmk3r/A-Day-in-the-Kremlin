from adventure_game.models import Puzzle


class HarderLabPuzzle(Puzzle):
    def __init__(self):
        super().__init__("harderquest", "the harder quest", "13", ["You have to guess"], "37", reward="phone")
