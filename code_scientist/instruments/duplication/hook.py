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

class BaseHook(object):
    def __init__(self, filename, tokens, start_index, stop_index):
        self.filename = filename
        self.tokens = tokens
        self.start_index = start_index
        self.stop_index = stop_index
        self._done = False

    def clone(self):
        return type(self)(self.filename, self.tokens,
                self.start_index, self.stop_index)

    def __iter__(self):
        return self

    @property
    def start(self):
        return self.tokens[self.start_index]

    @property
    def stop(self):
        return self.tokens[self.stop_index]

    def walk(self):
        for i in xrange(self.start_index, self.stop_index + 1):
            yield self.tokens[i]

    def __str__(self):
        return "%s('%s', <tokens>, %s, %s)" % (self.__class__.__name__,
                self.filename, self.start_index, self.stop_index)


class Hook(BaseHook):
    def next(self):
        next_index = self.stop_index + 1
        if self._done or next_index >= len(self.tokens):
            self._done = True
            raise StopIteration()
        self.stop_index = next_index
        return self.tokens[self.stop_index]

    def reversed(self):
        return ReversedHook(self.filename, self.tokens,
                self.start_index, self.stop_index)

class ReversedHook(BaseHook):
    def next(self):
        next_index = self.start_index - 1
        if self._done or next_index < 0:
            self._done = True
            raise StopIteration()
        self.start_index = next_index
        return self.tokens[self.start_index]
