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

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

import base

def _make_class_dict(kind):
    lower_kind = kind.lower()
    kind_id = lower_kind + '_id'
    kind_metric_value = lower_kind + '_metric_values'
    result = {
        '__tablename__': kind_metric_value,

        'id': Column('id', Integer, primary_key=True),
        'value': Column(String, nullable=False, index=True),

        'metric_id': Column('metric_id', Integer,
            ForeignKey('metric.id'), nullable=False),
        kind_id: Column(kind_id, Integer, ForeignKey(
                lower_kind + '.id'), nullable=False),

        'metric': relationship('Metric', backref=kind_metric_value),
        lower_kind: relationship(kind, backref=kind_metric_value),

        '__table_args__': (UniqueConstraint('metric_id', kind_id), {})
    }
    return result


def _make_metric_value_class(kind):
    new_class_name = kind + 'MetricValue'
    new_class = type(new_class_name, (base.Base,), _make_class_dict(kind))
    return new_class

SnapshotMetricValue = _make_metric_value_class('Snapshot')
FileSetMetricValue = _make_metric_value_class('FileSet')
FileMetricValue = _make_metric_value_class('File')
FunctionMetricValue = _make_metric_value_class('Function')
