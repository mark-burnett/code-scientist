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

Match = collections.namedtuple('Match',
        'filename start_index stop_index start_line stop_line')

class MatchInfo(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def has(self, left, right):
        if _contains(self.left, left) and _contains(self.right, right):
            return True
        if _contains(self.left, right) and _contains(self.right, left):
            return True
        return False

    def append(self, element):
        print 'adding element:', element
        self._matches.append(element)

    def __str__(self):
        return "MatchInfo(%s, %s)" % (self.left, self.right)

    def __repr__(self):
        return str(self)

def _contains(container, element):
    if container.filename == element.filename:
        if container.start_index <= element.start_index:
            if container.stop_index >= element.stop_index:
                return True
    return False
