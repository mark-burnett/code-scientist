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

from code_scientist.database import File

class FileTest(base_testcase.BaseDatabaseTest):
    def test_comparator_equal(self):
        f = File(path='test path 1')
        self.session.add(f)
        self.session.commit()

        session2 = self.new_session()
        f2 = session2.query(File).first()

        self.assertEqual(f.id, f2.id)
        self.assertEqual(f.path, f2.path)
        self.assertEqual(f, f2)

    def test_comparator_not_equal(self):
        f1 = File(path='test path 1')
        f2 = File(path='test path 2')
        self.session.add(f1)
        self.session.add(f2)
        self.session.commit()

        self.assertNotEqual(f1, f2)

        session2 = self.new_session()
        f1_2 = session2.query(File).filter_by(path='test path 1').first()
        f2_2 = session2.query(File).filter_by(path='test path 2').first()

        self.assertEqual(f1, f1_2)
        self.assertEqual(f2, f2_2)

        self.assertNotEqual(f1_2, f2_2)
