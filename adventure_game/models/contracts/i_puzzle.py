from abc import ABCMeta, abstractmethod


class IPuzzle(metaclass=ABCMeta):
    @property
    @abstractmethod
    def id(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def possible_answers(self):
        pass

    @property
    @abstractmethod
    def correct_answer(self):
        pass

    @property
    @abstractmethod
    def is_solved(self):
        pass

    @property
    @abstractmethod
    def reward(self):
        pass

    @reward.setter
    @abstractmethod
    def reward(self, value):
        pass

    @abstractmethod
    def answer_is_correct(self, answer):
        pass
