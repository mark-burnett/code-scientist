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
import itertools

import match

class MatchContainer(object):
    def __init__(self):
        self._file_pair_matches = collections.defaultdict(list)
        self._matches = collections.defaultdict(set)

    def add(self, new_hook, existing_hook):
        if not self._hooks_already_matched(new_hook, existing_hook):
            match_key, matches = _extract_match(new_hook, existing_hook)
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

    def values(self):
        return self._matches.values()

def _combined_filename(left, right):
    return '|'.join(sorted([left.filename, right.filename]))

def _extract_match(left, right):
    forward_extent = _get_forward_extent(left, right)

    l_start_index = left.start_index
    l_start_line = left.start.line_number
    r_start_index = right.start_index
    r_start_line = right.start.line_number
    l_stop_index, l_stop_line, r_stop_index, r_stop_line = forward_extent

#    key = left.get_key(l_start_index, l_stop_index)
    key = ''.join(left.tokens[i].token_value
            for i in xrange(l_start_index, l_stop_index + 1))

    return key, [match.Match(left.filename, l_start_index, l_stop_index,
            l_start_line, l_stop_line),
        match.Match(right.filename, r_start_index, r_stop_index,
            r_start_line, r_stop_line)]

def _get_forward_extent(left, right):
    cleft = left.clone()
    cright = right.clone()

    left_index = left.stop_index
    left_line = left.stop.line_number
    right_index = right.stop_index
    right_line = right.stop.line_number

    for left_token, right_token in itertools.izip(cleft, cright):
        if left_token.token_value != right_token.token_value:
            break
        left_index += 1
        right_index += 1
        left_line = cleft.stop.line_number
        right_line = cright.stop.line_number
    return left_index, left_line, right_index, right_line
