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
import re

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

import base

def _make_class_dict(target_class_name):
    _name = convert_from_camel(target_class_name)

    table_name = "%s_metric_value" % _name
    backref_name = "%s_metric_values" % _name

    target_id = "%s_id" % _name
    target_id_field =  "%s.id" % _name
    target_name = _name

    result = {
        '__tablename__': table_name,

        'id': Column('id', Integer, primary_key=True),
        'value': Column(String, nullable=False, index=True),

        'metric_id': Column('metric_id', Integer,
                ForeignKey('metric.id'), nullable=False),
        target_id: Column(target_id, Integer,
                ForeignKey(target_id_field), nullable=False),

        'metric': relationship('Metric', backref=backref_name),
        target_name: relationship(target_class_name, backref=backref_name),

        '__table_args__': (UniqueConstraint('metric_id', target_id), {})
    }
    return result

def convert_from_camel(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def _make_metric_value_class(kind):
    new_class_name = kind + 'MetricValue'
    new_class = type(new_class_name, (base.Base,), _make_class_dict(kind))
    return new_class

SnapshotMetricValue = _make_metric_value_class('Snapshot')
FileSetMetricValue  = _make_metric_value_class('FileSet')
FileMetricValue     = _make_metric_value_class('File')
FunctionMetricValue = _make_metric_value_class('Function')
