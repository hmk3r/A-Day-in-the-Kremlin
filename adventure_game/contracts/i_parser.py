from abc import ABCMeta, abstractmethod


class IParser(metaclass=ABCMeta):
    @abstractmethod
    def parse_command(self, command_as_text):
        pass
