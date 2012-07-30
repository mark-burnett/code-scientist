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

from code_scientist.instruments.duplication import hash_manager

class MockToken(object):
    def __init__(self, value):
        self.token_value = value

class MockHook(object):
    def __init__(self, tokens, start_index, stop_index):
        self.tokens = tokens
        self.start_index = start_index
        self.stop_index = stop_index

    def walk(self):
        for i in xrange(self.start_index, self.stop_index + 1):
            yield self.tokens[i]

class HashManagerTest(unittest.TestCase):
    def setUp(self):
        self.tokens = [MockToken(str(x)) for x in xrange(100)]
        self.hook = MockHook(self.tokens, 42, 77)

    def test_calculate_directly(self):
        expected_hash = ''.join(str(x) for x in xrange(42, 78))
        self.assertEqual(expected_hash,
                hash_manager._calculate_directly(self.hook))
