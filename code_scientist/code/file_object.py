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

from code_scientist import utils

class File(object):
    def __init__(self, name, file_type, stream=None):
        self.name = name
        self.file_type = file_type
        self._stream = stream

        self.properties = {}

    @utils.memoize
    def get_contents(self):
        if self._stream:
            result = self._stream.read()
            self._stream.close()
        else:
            result = open(self.name).read()
        return result
