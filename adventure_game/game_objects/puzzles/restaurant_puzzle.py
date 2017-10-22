from adventure_game.models import Puzzle


class RestaurantPuzzle(Puzzle):
    def __init__(self):
        super().__init__("bubbles", "", "", [], "")

    def answer_is_correct(self, answer):
        print("Here you can define custom logic for the puzzle")
        return super().answer_is_correct(answer)
