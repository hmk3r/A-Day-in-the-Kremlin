from adventure_game.models.contracts import IPuzzle


class Puzzle(IPuzzle):
    def __init__(self,
                 puzzle_id,
                 name=None,
                 description=None,
                 possible_answers=None,
                 correct_answer=None,
                 win_message=None,
                 reward=None,
                 required_items=None,
                 takes_items=False):
        self._id = puzzle_id
        self._name = name
        self._description = description
        self._possible_answers = possible_answers if possible_answers else []
        self._correct_answer = correct_answer
        self._win_message = win_message
        self._reward = reward
        self._required_items = required_items
        self._takes_items = takes_items
        self._is_solved = False

    @property
    def is_solved(self):
        return self._is_solved

    @property
    def possible_answers(self):
        return self._possible_answers

    @property
    def description(self):
        return self._description

    @property
    def required_items(self):
        return self._required_items

    @property
    def takes_items(self):
        return self._takes_items

    @property
    def reward(self):
        return self._reward

    @property
    def correct_answer(self):
        return self._correct_answer

    @property
    def win_message(self):
        return self._win_message

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    def answer_is_correct(self, answer):
        self._is_solved = answer == self.correct_answer
        return self.is_solved
