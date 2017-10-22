from adventure_game.models import Puzzle


class RestaurantPuzzle(Puzzle):
    def __init__(self):
        super().__init__("puzzle", "a mystery", "You're 3yo. How old are you?", ["0", "10", "15"], "3", reward="quid")
