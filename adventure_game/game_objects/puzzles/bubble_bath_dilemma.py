from adventure_game.models import Puzzle
from adventure_game.exceptions import PlayerDeadException

ANSWER_LEMON_BUBBLE_BATH = "1"
WRONG_BUBBLE_BATH_ERROR_MESSAGE = "STALIN HATES LEMONS. Bad choices lead to GULAG, comrade!"


class BubbleBathDilemma(Puzzle):
    def __init__(self):
        super().__init__("bubble_bath_dilemma")

    def answer_is_correct(self, answer):
        if answer == self.correct_answer:
            self._is_solved = True
            return True
        elif answer == ANSWER_LEMON_BUBBLE_BATH:
            raise PlayerDeadException(WRONG_BUBBLE_BATH_ERROR_MESSAGE)
        else:
            return False
