from abc import ABCMeta, abstractmethod


class IPuzzle(metaclass=ABCMeta):
    id = ""
    name = ""
    description = ""
    possible_answers = []
    correct_answer = None
    is_solved = False
    reward = None

    @abstractmethod
    def answer_is_correct(self, answer):
        pass
