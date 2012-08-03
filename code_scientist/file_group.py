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

def FileGroup(object):
    def __init__(self, filenames, file_type, lexer):
        self.filenames = filenames
        self.file_type = file_type
        self._lexer = lexer

    @utils.memoize
    def get_verbatim_content(self):
        return map(utils.slurp_file, self.filenames)


    @utils.memoize
    def get_content_as_tokens(self):
        return map(self._lexer, self.get_verbatim_content())
