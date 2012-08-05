#    Copyright (C) 2012 Mark Burnett, David Morton
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

from sqlalchemy import Column, ForeignKey, UniqueConstraint, relation
from sqlalchemy import Integer, String

import base

def _make_class_dict(kind):
    lower_kind = kind.lower()
    kind_metric_value = lower_kind + '_metric_value'
    result = {
        '__tablename__': lower_kind + '_metric_value',

        'id': Column(Integer, primary_key=True),
        'value': Column(String),

        'instrument_id': Column(Integer, ForeignKey('instrument.id')),
        'metric_id': Column(Integer, ForeignKey('metric.id')),
        lower_kind + '_id': Column(Integer, ForeignKey(
                lower_kind + '_id'),

        'instrument' = relation('Instrument', backref=kind_metric_value),
        'metric' = relation('Metric', backref=kind_metric_value),
        lower_kind = relation(kind, backref=kind_metric_value),

        '__table_args__': (UniqueConstraint('instrument_id', 'metric_id',
                        lower_kind + '_id'), {})
    }
    return result


def _make_metric_value_class(kind):
    new_class_name = kind + 'MetricValue'
    new_class = type(new_class_name, base.Base, _make_class_dict(kind))
    return new_class

SnapshotMetricValue = _make_metric_value_class('Snapshot')
FileSetMetricValue = _make_metric_value_class('FileSet')
FileMetricValue = _make_metric_value_class('File')
FunctionMetricValue = _make_metric_value_class('Function')
