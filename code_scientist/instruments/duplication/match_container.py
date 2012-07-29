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
import copy

import itertools

class MatchContainer(object):
    def __init__(self):
        self.token_walkers = []
        self.matches = collections.defaultdict(set)

    def __iter__(self):
        return self.matches.itervalues()

    def add(self, new_token_walker):
        skips = [0]
        for tw in self.token_walkers:
            key, a, b, skip = _get_longest_match(copy.copy(tw),
                    copy.copy(new_token_walker))
            self.matches[key].add(a)
            self.matches[key].add(b)
            skips.append(skip)
        self.token_walkers.append(copy.copy(new_token_walker))
        return max(skips)

    @property
    def has_match(self):
        return len(self.matches) > 0

MatchIdentifier = collections.namedtuple('MatchIdentifier',
        'filename start_line stop_line token_count')

def _get_longest_match(left, right):
    skip = -1
    left_stop_line = left.stop_line
    right_stop_line = right.stop_line
    matching_token_values = []

    for left_token, right_token in itertools.izip(left, right):
        if left_token.token_value != right_token.token_value:
            break

        skip += 1
        left_stop_line = left_token.line_number
        right_stop_line = right_token.line_number
        matching_token_values.append(left_token.token_value)

#    count = left.end_position - left.start_position + skip + 1
    count = skip + 1
    return (''.join(matching_token_values),
            MatchIdentifier(left.filename,
                left.start_line, left_stop_line,
                count),
            MatchIdentifier(right.filename,
                right.start_line, right_stop_line,
#                right.tokens[0].line_number,
#                right_stop_line_number,
                count),
            skip)
