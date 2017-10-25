from adventure_game.factories.contracts import IPuzzleFactory
from adventure_game.models import Puzzle


class PuzzleFactory(IPuzzleFactory):
    def create_puzzle(self,
                      puzzle_id,
                      name,
                      description,
                      possible_answers,
                      correct_answer,
                      reward=None,
                      required_items=None,
                      takes_items=False):

        return Puzzle(puzzle_id,
                      name,
                      description,
                      possible_answers,
                      correct_answer,
                      reward,
                      required_items,
                      takes_items)

