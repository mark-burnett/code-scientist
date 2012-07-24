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

import os

from code_scientist import utils

class RegexSpecimenGroup(object):
    def __init__(self, path=None, regex='*', **walk_args):
        if path:
            self.path = path
        else:
            self.path = os.getcwd()

        self.regex = regex

    def __iter__(self):
        return iter(utils.regex_filter(self.regex,
            utils.walk_files(self.path)))
