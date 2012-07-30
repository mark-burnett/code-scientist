#    Copyright (C) 2012 Mark Burnett
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import collections

import algorithm
import match

class MatchContainer(object):
    def __init__(self):
        self._file_pair_matches = collections.defaultdict(list)
        self._matches = collections.defaultdict(set)

    def add(self, new_hook, existing_hook):
        if not self._hooks_already_matched(new_hook, existing_hook):
            match_key, matches = algorithm.extract_match(new_hook, existing_hook)
            self._add_file_match_info(new_hook, existing_hook, matches)
            map(self._matches[match_key].add, matches)

    def _hooks_already_matched(self, left, right):
        combined_filename = _combined_filename(left, right)
        for match_info in self._file_pair_matches[combined_filename]:
            if match_info.has(left, right):
                return True
        return False

    def _add_file_match_info(self, left, right, matches):
        combined_filename = _combined_filename(left, right)
        match_info = match.MatchInfo(*matches)
        self._file_pair_matches[combined_filename].append(match_info)

def _combined_filename(left, right):
    return '|'.join(sorted([left.filename, right.filename]))
