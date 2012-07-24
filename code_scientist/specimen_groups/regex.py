import os

from code_scientist import utils

class RegexSpecimenGroup(object):
    def __init__(self, path=None, regex=None, **walk_args):
        if path:
            self.path = path
        else:
            self.path = os.getcwd()

        self.regex = regex
        self.walk_args = walk_args

    def __iter__(self):
        walk_results = iter(os.walk(self.path), **self.walk_args)
        full_file_list = self._parse_walk_results(walk_results)
        return iter(utils.regex_filter(self.regex, full_file_list))

    def _parse_walk_results(self, walk_results):
        result = []
        for directory, subdirs, files in walk_results:
            for f in files:
                result.append(os.path.join(directory, f))
        return result
