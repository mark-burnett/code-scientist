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
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import relationship, backref

import base

class Snapshot(base.Base):
    __tablename__ = 'snapshot'

    id = Column(Integer, primary_key=True)
    commit_id = Column(String, index=True)
    time = Column(DateTime, index=True)

    repository_id = Column(Integer, ForeignKey('repository.id'))
    repository = relationship('Repository', backref=backref('snapshots',
        order_by=time))
