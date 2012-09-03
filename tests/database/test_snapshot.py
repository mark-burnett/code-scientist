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

import datetime

from code_scientist.database import Repository, Snapshot

class SnapshotTest(base_testcase.BaseDatabaseTest):
    def test_construction(self):
        snapshot = Snapshot(time=datetime.datetime.now(), commit_id='some hash')

        self.session.add(snapshot)
        self.session.commit()
        snapshot2 = self.session.query(Snapshot).first()
        self.assertIs(snapshot, snapshot2)

    def test_repository_relationship(self):
        repo = Repository(name='foo')
        snapshot = Snapshot(repository=repo,
                time=datetime.datetime(year=1981, month=10, day=26, hour=10))
        self.session.add(repo)
        self.session.commit()

        ss2 = self.session.query(Snapshot).first()

        self.assertEqual(repo, ss2.repository)

    def test_repository_backref(self):
        repo = Repository(name='foo')
        snapshot = Snapshot(repository=repo,
                time=datetime.datetime(year=1981, month=10, day=26, hour=10))
        self.session.add(repo)
        self.session.commit()

        repo2 = self.session.query(Repository).first()

        self.assertEqual(repo, repo2)
        self.assertEqual(1, len(repo2.snapshots))
        self.assertEqual(snapshot, repo2.snapshots[0])

    def test_repository_backref_ordering(self):
        repo = Repository(name='foo')
        ss_a = Snapshot(repository=repo,
                time=datetime.datetime(year=1981, month=10, day=26, hour=10))
        self.session.add(repo)
        self.session.commit()

        ss_b = Snapshot(repository=repo,
                time=datetime.datetime(year=1980, month=4, day=25, hour=6))
        self.session.commit()

        self.assertEqual(ss_b, repo.snapshots[0])
        self.assertEqual(ss_a, repo.snapshots[1])
