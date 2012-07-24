import re

class RemoveMatches(object):
    def __init__(self, regex=None):
        self.regex = regex
        self._compiled_re = re.compile(regex)

    def __call__(self, line):
        if self._compiled_re.match(line):
            return ''
        return line

empty_line = RemoveMatches(regex='^\s*$')
comment_line = RemoveMatches(regex='^\s*\#.*\n$')
