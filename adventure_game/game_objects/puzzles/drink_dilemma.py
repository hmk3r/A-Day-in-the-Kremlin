from adventure_game.models import Puzzle
from adventure_game.exceptions import PlayerDeadException

ANSWER_SPECIAL_DRINK = "2"
ANSWER_FRUIT_SHOOT = "3"

SPECIAL_DRINK_ERROR_MESSAGE = """YOU HAVE POURED STALIN'S SPECIAL DRINK!!! This is to be only poured after a great victory. 
This crime is so great that you and your entire village are sent to GULAG!"""
FRUIT_SHOOT_ERROR_MESSAGE = "Stalin is offended by your choice and sends you to a labour camp for 5 years..."


class DrinkDilemma(Puzzle):
    def __init__(self):
        super().__init__("drink_dilemma")

    def answer_is_correct(self, answer):
        if answer == self.correct_answer:
            self._is_solved = True
            return True

        if answer == ANSWER_SPECIAL_DRINK:
            raise PlayerDeadException(SPECIAL_DRINK_ERROR_MESSAGE)

        if answer == ANSWER_FRUIT_SHOOT:
            raise PlayerDeadException(FRUIT_SHOOT_ERROR_MESSAGE)

        return False
