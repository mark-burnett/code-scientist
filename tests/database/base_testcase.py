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

import unittest

import sqlalchemy
import sqlalchemy.orm

from code_scientist.database import base


ENGINE = sqlalchemy.create_engine('sqlite://')
base.Base.metadata.create_all(ENGINE)

Session = sqlalchemy.orm.sessionmaker(bind=ENGINE)


class BaseDatabaseTest(unittest.TestCase):
    def setUp(self):
        self.connection = ENGINE.connect()
        self.transaction = self.connection.begin()
        self.session = self.new_session()

    def new_session(self):
        return Session(bind=self.connection)

    def tearDown(self):
        self.transaction.rollback()
        self.session.close()
