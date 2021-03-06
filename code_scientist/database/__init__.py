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

import sqlalchemy as _sa
import sqlalchemy.orm as _orm
import logging as _logging

import base as _base
import tables as _tables

from function import Function
from file import File
from file_set import FileSet
from snapshot import Snapshot
from repository import Repository
from tag import Tag

from metric import Metric

from metric_value import FunctionMetricValue, FileMetricValue
from metric_value import FileSetMetricValue, SnapshotMetricValue

def initialize(engine_string='sqlite://'):
    _logging.debug('Creating SQLAlchemy engine for string: %s', engine_string)
    engine = _sa.create_engine(engine_string)

    _logging.debug('Creating tables.')
    _base.Base.metadata.create_all(engine)
    _base.Base.metadata.bind = engine

    _logging.debug('Creating Session class.')
    global Session
    global UnscopedSession
    UnscopedSession = _orm.sessionmaker(bind=engine)
    Session = _orm.scoped_session(UnscopedSession)
