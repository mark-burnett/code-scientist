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

from code_scientist.database import File, Function

class FunctionTest(base_testcase.BaseDatabaseTest):
    def test_file_relationship(self):
        functions = [Function(name='_call_%s_' % x) for x in xrange(5)]
        file_ = File(path='test/path/1.test', functions=functions)

        self.session.add(file_)
        self.session.commit()

        file_2 = self.session.query(File).first()

        for func in functions:
            self.assertIs(func.file, file_2)

    def test_file_backref(self):
        functions = [Function(name='_call_%s_' % x) for x in xrange(5)]
        file_ = File(path='test/path/1.test', functions=functions)

        self.session.add(file_)
        self.session.commit()

        file_2 = self.session.query(File).first()

        self.assertEqual(len(functions), len(file_2.functions))
        for func in file_2.functions:
            self.assertIn(func, functions)
