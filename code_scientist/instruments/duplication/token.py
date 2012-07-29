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

from code_scientist.instruments.duplication import match_container

Token = collections.namedtuple('Token', 'line_number token_type token_value')

class TokenWalker(object):
    def __init__(self, filename, tokens, start_position=0, end_position=99):
        self.filename = filename
        self.tokens = tokens
        self.start_position = start_position
        self.end_position = end_position
        self._last_hard_hash = None

    def __iter__(self):
        return self

    def next(self):
        self.start_position += 1
        self.end_position += 1
        self._last_hard_hash = None
        if self.end_position >= len(self.tokens):
            raise StopIteration()
        return self

    def get_followup_iterator(self):
        for i in xrange(self.end_position, len(self.tokens)):
            yield self.tokens[i]

    @property
    def hard_hash(self):
        if not self._last_hard_hash:
            self._last_hard_hash = ''.join(self.tokens[i].token_value
                    for i in xrange(self.start_position, self.end_position))
        return self._last_hard_hash

    def get_longest_match(self, sister):
        assert(sister.hard_hash == self.hard_hash)

        skip = -1
        my_stop_line_number = self.tokens[self.end_position]
        sister_stop_line_number = sister.tokens[sister.end_position]
        matching_token_values = []

        for my_token, sister_token in itertools.izip(
                self.get_followup_iterator(), sister.get_followup_iterator()):
            if my_token.token_value != sister_token.token_value:
                break

            skip += 1
            my_stop_line_number = my_token.line_number
            sister_stop_line_number = sister_token.line_number
            matching_token_values.append(my_token.token_value)

        count = self.end_position - self.start_position + skip + 1
        return (''.join(matching_token_values),
                match_container.MatchIdentifier(self.filename,
                    self.tokens[0].line_number, my_stop_line_number, count),
                match_container.MatchIdentifier(sister.filename,
                    sister.tokens[0].line_number, sister_stop_line_number, count),
                skip)

    def skip(self, amount):
        for i in xrange(amount):
            next(self)
