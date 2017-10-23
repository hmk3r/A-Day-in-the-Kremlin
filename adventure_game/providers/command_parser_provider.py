import string

from adventure_game.contracts import IParser


class CommandParserProvider(IParser):
    SKIP_WORDS = ['a', 'about', 'all', 'an', 'another', 'any', 'around', 'at',
                  'bad', 'beautiful', 'been', 'better', 'big', 'can', 'every', 'for',
                  'from', 'good', 'have', 'her', 'here', 'hers', 'his', 'how',
                  'i', 'if', 'in', 'into', 'is', 'it', 'its', 'large', 'later',
                  'like', 'little', 'main', 'me', 'mine', 'more', 'my', 'now',
                  'of', 'off', 'oh', 'on', 'please', 'small', 'some', 'soon',
                  'that', 'the', 'then', 'this', 'those', 'through', 'till', 'to',
                  'towards', 'until', 'us', 'want', 'we', 'what', 'when', 'why',
                  'wish', 'with', 'would']

    def parse_command(self, command_as_text):
        normalised_string = self.normalise_string(command_as_text)
        words = normalised_string.split(" ")
        no_empty_strings = filter(None, words)
        command = self.filter_words(no_empty_strings, self.SKIP_WORDS)

        return command

    def normalise_string(self, input_string):
        no_punctuation = self.remove_punctuation(input_string).lower()
        no_spaces = self.remove_spaces(no_punctuation)

        return no_spaces

    def filter_words(self, words, skip_words):

        filtered_words = []
        for word in words:
            if word not in skip_words:
                filtered_words.append(word)
            else:
                continue

        return filtered_words

    def remove_punctuation(self, text):
        no_punctuation = ""
        for char in text:
            if not (char in string.punctuation):
                no_punctuation = no_punctuation + char
        return no_punctuation

    def remove_spaces(self, text):
        start = 0
        end = -1
        text_length = len(text)
        while (start < text_length - 1) and text[start].isspace():
            start += 1
        while (text_length + end > 0) and text[end].isspace():
            end -= 1
        if end == -1:
            end = None
        else:
            end += 1
        return text[start:end]
