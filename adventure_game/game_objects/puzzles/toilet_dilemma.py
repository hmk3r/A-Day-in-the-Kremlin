from adventure_game.models import Puzzle
from adventure_game.exceptions import PlayerDeadException

ANSWER_ROUGH = "2"
ANSWER_SOFT = "1"
ANSWER_ROUGH_ERROR_MESSAGE = """Well you blew it. You scratched the golden bog and you got sent to the Gulag. 
You will spend the rest of your days working generous 14 hour day’s until you freeze to death yay!
"""
ANSWER_SOFT_ERROR_MESSAGE = "You barely clean the toilet, Stalin has your family publicly executed from treason and sends you to GULAG!"


class ToiletDilemma(Puzzle):
    def __init__(self):
        super().__init__("toilet_dilemma")

    def answer_is_correct(self, answer):
        if answer == self.correct_answer:
            self._is_solved = True
            return True

        if answer == ANSWER_ROUGH:
            raise PlayerDeadException(ANSWER_ROUGH_ERROR_MESSAGE)

        if answer == ANSWER_SOFT:
            raise PlayerDeadException(ANSWER_SOFT_ERROR_MESSAGE)

        return False
