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

class BaseHashManager(object):
    def __init__(self):
        self._current_hash = None

    def reset(self):
        self._current_hash = None

    def __call__(self, hook):
        if self._current_hash is None:
            self._current_hash = self._calculate_directly(hook)
        else:
            self._update_hash(hook)
        return self._current_hash

    def _update_hash(self, hook):
        self._current_hash = self._calculate_directly(hook)

class ExactHashManager(BaseHashManager):
    def _calculate_directly(self, hook):
        return ''.join(t.token_value for t in hook.walk())

class StructuralHashManager(BaseHashManager):
    def _calculate_directly(self, hook):
        return ''.join(t.token_type for t in hook.walk())
