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

import base_testcase

from code_scientist.database import FileSetCategory

class FileSetCategoryTest(base_testcase.BaseDatabaseTest):
    def test_construction(self):
        fsc = FileSetCategory(name='fsc_1')

        self.session.add(fsc)
        self.session.commit()
        fsc2 = self.session.query(FileSetCategory).first()
        self.assertIs(fsc, fsc2)
