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

from code_scientist.database import Function, File, FileSet, Snapshot
from code_scientist.database import Tag

class BaseMetricValueTest(object):
    def make_tag_object(self):
        tag = Tag(name='bar')
        self.obj.tags.append(tag)
        self.session.add(tag)
        self.session.commit()

        return tag

    def test_forward_relationship(self):
        tag = self.make_tag_object()
        objs = getattr(tag, self.ref_name)
        self.assertIn(self.obj, objs)

    def test_reverse_relationship(self):
        tag = self.make_tag_object()
        tags = self.obj.tags
        self.assertIn(tag, tags)


class FunctionMetricValueTest(base_testcase.BaseDatabaseTest,
        BaseMetricValueTest):
    def setUp(self):
        file = File(path='bar')
        self.obj = Function(name='foo', file=file)
        self.ref_name = 'functions'
        base_testcase.BaseDatabaseTest.setUp(self)

class FileMetricValueTest(base_testcase.BaseDatabaseTest,
        BaseMetricValueTest):
    def setUp(self):
        self.obj = File(path='bar')
        self.ref_name = 'files'
        base_testcase.BaseDatabaseTest.setUp(self)

class FileSetMetricValueTest(base_testcase.BaseDatabaseTest,
        BaseMetricValueTest):
    def setUp(self):
        self.obj = FileSet(name='foo')
        self.ref_name = 'file_sets'
        base_testcase.BaseDatabaseTest.setUp(self)

class SnapshotMetricValueTest(base_testcase.BaseDatabaseTest,
        BaseMetricValueTest):
    def setUp(self):
        self.obj = Snapshot()
        self.ref_name = 'snapshots'
        base_testcase.BaseDatabaseTest.setUp(self)

