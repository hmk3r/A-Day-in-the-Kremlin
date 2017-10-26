from adventure_game.models import Puzzle
from adventure_game.exceptions import PlayerDeadException

ANSWER_CALM_WALK = "2"
ANSWER_CHARGE_AT_BEAR = "3"
BEAR_NOT_TAMED_ERROR_MESSAGE = """Kirillina runs over to you at full speed and jumps onto you as you try to run away.
With a single slash of her paw she separates your head from the rest of your body. Your spirit goes to GULAG.
Blood oozes out onto the ground from where your neck and head once joined.
Kirillina seems to be pleased by the chaos she has caused and she happily strolls to the fountain to drink from vodka.
"""


class BearProblem(Puzzle):
    def __init__(self):
        super().__init__("bear_problem")

    def answer_is_correct(self, answer):
        if answer == self.correct_answer:
            self._is_solved = True
            return True
        elif answer == ANSWER_CALM_WALK or answer == ANSWER_CHARGE_AT_BEAR:
            raise PlayerDeadException(BEAR_NOT_TAMED_ERROR_MESSAGE)
        else:
            return False
