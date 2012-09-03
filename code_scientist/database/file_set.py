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

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

import base

class FileSet(base.Base):
    __tablename__ = 'file_set'

    id = Column(Integer, primary_key=True)
    snapshot_id = Column(Integer, ForeignKey('snapshot.id'))
    name = Column(String, nullable=False, index=True)
    __table_args__ = (UniqueConstraint('snapshot_id', 'name'), {})

    snapshot = relationship('Snapshot', backref='file_sets')
    files = relationship('File', secondary='file_set_files',
            backref='file_sets')

    repository = relationship('Repository', secondary='snapshot', uselist=False)
