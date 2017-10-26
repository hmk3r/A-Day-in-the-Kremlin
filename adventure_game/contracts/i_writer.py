from abc import ABCMeta, abstractmethod


class IWriter(metaclass=ABCMeta):
    @abstractmethod
    def write(self, text):
        pass

    @abstractmethod
    def write_slowly(self, text):
        pass

    @abstractmethod
    def write_separator(self):
        pass

    @abstractmethod
    def write_info(self, text):
        pass

    @abstractmethod
    def write_error(self, error):
        pass

    @abstractmethod
    def write_success(self, message):
        pass

    @abstractmethod
    def clear(self):
        pass
