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

import unittest

import StringIO

from code_scientist.code import file_object

FILE_A = '''
test(some_code)
'''

FILE_B = '''
other(test_code)
'''

class FileTest(unittest.TestCase):
    def setUp(self):
        self.file_a = StringIO.StringIO(FILE_A)
        self.file_b = StringIO.StringIO(FILE_B)

    def test_get_contents(self):
        f_a = file_object.File(None, None, stream=self.file_a)

        self.assertMultiLineEqual(FILE_A, f_a.get_contents())

    def test_get_contents_repeats(self):
        f_a = file_object.File(None, None, stream=self.file_a)

        self.assertMultiLineEqual(FILE_A, f_a.get_contents())
        self.assertMultiLineEqual(FILE_A, f_a.get_contents())

    def test_get_contents_distinct(self):
        f_a = file_object.File(None, None, stream=self.file_a)
        f_b = file_object.File(None, None, stream=self.file_b)

        self.assertNotEqual(f_a.get_contents(), f_b.get_contents())
