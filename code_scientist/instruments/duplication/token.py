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

Token = collections.namedtuple('Token', 'line_number token_value')

class TokenIterator(object):
    __slots__ = ['filename', 'tokens', 'index',
            'start_line', 'stop_line', '_done']
    def __init__(self, filename, tokens, index, start_line):
        self.filename = filename
        self.tokens = tokens
        self.index = index # XXX -1?
        self.start_line = start_line
        self.stop_line = self.tokens[self.index].line_number
        self._done = False


    def __iter__(self):
        return self

    def next(self):
        self.index += 1
        if self._done or self.index >= len(self.tokens):
            self._done = True
            raise StopIteration()
        return self.tokens[self.index]

class TokenWindowIterator(object):
    def __init__(self, filename, tokens, window_size=100):
        self.filename = filename
        self.tokens = tokens
        self.window_size = window_size
        self._i = -1
        self._done = False
        self._last_hard_hash = None

    def __iter__(self):
        return self

    def next(self):
        self._i += 1
        if self._done or self._i + self.window_size >= len(self.tokens):
            self._done = True
            raise StopIteration()
        return self.hard_hash, TokenIterator(self.filename, self.tokens,
                self._i + self.window_size, self.tokens[self._i].line_number)

    @property
    def hard_hash(self):
        if not self._last_hard_hash:
            self._last_hard_hash = ''.join(self.tokens[i].token_value
                    for i in xrange(self._i, self._i + self.window_size))
        return self._last_hard_hash
