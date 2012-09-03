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

from code_scientist.database import File, FileSet, Snapshot

class FileSetTest(base_testcase.BaseDatabaseTest):
    def test_file_relationship(self):
        files = [File(path='test/path/%s.test' % i) for i in xrange(5)]

        file_set = FileSet(files=files)
        self.session.add(file_set)
        self.session.commit()

        fs2 = self.session.query(FileSet).first()

        self.assertEqual(file_set, fs2)
        # Note the files are not sorted when they come back from the database
        self.assertEqual(len(files), len(fs2.files))
        for f in fs2.files:
            self.assertIn(f, files)

    def test_file_backref(self):
        files = [File(path='test/path/%s.test' % i) for i in xrange(5)]
        file_set = FileSet(files=files)

        for f in files:
            self.assertEqual(1, len(f.file_sets))
            self.assertIs(file_set, f.file_sets[0])

    def test_snapshot_relationship(self):
        snapshot = Snapshot()

        file_set = FileSet(snapshot=snapshot)
        self.session.add(file_set)
        self.session.commit()

        fs2 = self.session.query(FileSet).first()

        self.assertEqual(file_set, fs2)
        self.assertEqual(snapshot, fs2.snapshot)

    def test_snapshot_backref(self):
        snapshot = Snapshot()
        file_set = FileSet(snapshot=snapshot)

        self.assertEqual(1, len(snapshot.file_sets))
        self.assertIs(file_set, snapshot.file_sets[0])
