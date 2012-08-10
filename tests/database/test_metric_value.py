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

from code_scientist.database import FunctionMetricValue, FileMetricValue
from code_scientist.database import FileSetMetricValue, SnapshotMetricValue

from code_scientist.database import Function, File, FileSet, Snapshot
from code_scientist.database import Metric, Instrument

class BaseMetricValueTest(object):
    def make_metric_value_object(self):
        instrument = Instrument(name='instrument_1', revision='rev_1')
        metric = Metric(name='metric_1')
        obj = self.cls()
        mv_obj = self.mv_cls(metric=metric, instrument=instrument,
                **{self.forward_name: obj})

        self.session.add(mv_obj)
        self.session.commit()

        return mv_obj, metric, instrument, obj

    def test_metric_relationship(self):
        mv_obj, metric, instrument, obj = self.make_metric_value_object()
        mv_obj2 = self.session.query(self.mv_cls).first()

        self.assertEqual(mv_obj, mv_obj2)
        self.assertEqual(metric, mv_obj2.metric)

    def test_metric_backref(self):
        mv_obj, metric, instrument, obj = self.make_metric_value_object()
        mv_obj2 = self.session.query(self.mv_cls).first()

        self.assertIn(mv_obj2, getattr(metric, self.backref_name))

    def test_instrument_relationship(self):
        mv_obj, metric, instrument, obj = self.make_metric_value_object()
        mv_obj2 = self.session.query(self.mv_cls).first()

        self.assertEqual(mv_obj, mv_obj2)
        self.assertEqual(instrument, mv_obj2.instrument)

    def test_instrument_backref(self):
        mv_obj, metric, instrument, obj = self.make_metric_value_object()
        mv_obj2 = self.session.query(self.mv_cls).first()

        self.assertIn(mv_obj2, getattr(instrument, self.backref_name))

    def test_object_relationship(self):
        mv_obj, metric, instrument, obj = self.make_metric_value_object()
        mv_obj2 = self.session.query(self.mv_cls).first()

        self.assertEqual(mv_obj, mv_obj2)
        self.assertEqual(obj, getattr(mv_obj2, self.forward_name))

    def test_object_backref(self):
        mv_obj, metric, instrument, obj = self.make_metric_value_object()
        mv_obj2 = self.session.query(self.mv_cls).first()

        self.assertIn(mv_obj2, getattr(obj, self.backref_name))

class FunctionMetricValueTest(base_testcase.BaseDatabaseTest,
        BaseMetricValueTest):
    def setUp(self):
        self.mv_cls = FunctionMetricValue
        self.cls = Function
        self.backref_name = 'function_metric_values'
        self.forward_name = 'function'
        base_testcase.BaseDatabaseTest.setUp(self)

class FileMetricValueTest(base_testcase.BaseDatabaseTest,
        BaseMetricValueTest):
    def setUp(self):
        self.mv_cls = FileMetricValue
        self.cls = File
        self.backref_name = 'file_metric_values'
        self.forward_name = 'file'
        base_testcase.BaseDatabaseTest.setUp(self)

class FileSetMetricValueTest(base_testcase.BaseDatabaseTest,
        BaseMetricValueTest):
    def setUp(self):
        self.mv_cls = FileSetMetricValue
        self.cls = FileSet
        self.backref_name = 'fileset_metric_values'
        self.forward_name = 'fileset'
        base_testcase.BaseDatabaseTest.setUp(self)

class SnapshotMetricValueTest(base_testcase.BaseDatabaseTest,
        BaseMetricValueTest):
    def setUp(self):
        self.mv_cls = SnapshotMetricValue
        self.cls = Snapshot
        self.backref_name = 'snapshot_metric_values'
        self.forward_name = 'snapshot'
        base_testcase.BaseDatabaseTest.setUp(self)
