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

from sqlalchemy import Column, UniqueConstraint
from sqlalchemy import Integer, String

import base

class Instrument(base.Base):
    __tablename__ = 'instrument'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    revision = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('name', 'revision'), {})
    __mapper_args__ = {'polymorphic_on': name}
#            'polymorphic_identity': 'Instrument'}

    @classmethod
    def get_database_entry(cls):
        s = database.Session()
        i = s.query(database.Instrument).filter_by(name=cls.__name__).first()
        if i:
            logging.debug('Found existing instrument for %s.', cls.__name__)
            return i
        logging.debug('No existing instrument found for %s.  Creating one.',
                cls.__name__)
        i = database.Instrument(name=cls.__name__)
        s.add(i)
        s.commit()
        return i

    def measure_repository(self, repository):
        for snapshot in repository.snapshots:
            self.measure_snapshot(snapshot)

    def measure_snapshot(self, snapshot):
        for file_set in snapshot.file_sets:
            self.measure_file_set(file_set)

    def measure_file_set(self, file_set):
        for file in file_set.files:
            self.measure_file(file)

    def measure_file(self, file):
        for function in file.functions:
            self.measure_function(function)

    def measure_function(self, function):
        logging.error("'measure_function' not implemented for %s.",
                self.__class__.__name__)

        raise RuntimeError('measure_function not implemented for %s',
                self.__class__.__name__)
