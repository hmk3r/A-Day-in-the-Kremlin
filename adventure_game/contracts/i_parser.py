from abc import ABCMeta, abstractmethod


class IParser(metaclass=ABCMeta):
    @abstractmethod
    def parse_command(self, command_as_text):
        pass

    @abstractmethod
    def normalise_string(self, input_string):
        pass
