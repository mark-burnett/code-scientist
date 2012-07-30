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

import itertools

from code_scientist.instruments.duplication import hook

class BaseHookTest(unittest.TestCase):
    def setUp(self):
        self.test_filename = 'test/file/name.py'
        self.test_tokens = ['%d' % x for x in xrange(100)]
        self.test_start_index = 42
        self.test_stop_index = 77

        self.base_hook = hook.BaseHook(self.test_filename, self.test_tokens,
                self.test_start_index, self.test_stop_index)

    def test_clone(self):
        clone = self.base_hook.clone()

        self.assertIsNot(self.base_hook, clone)
        self.assertIs(self.base_hook.filename, clone.filename)
        self.assertIs(self.base_hook.tokens, clone.tokens)
        self.assertIs(self.base_hook.start_index, clone.start_index)
        self.assertIs(self.base_hook.stop_index, clone.stop_index)

    def test_start(self):
        self.assertEqual('42', self.base_hook.start)

    def test_stop(self):
        self.assertEqual('77', self.base_hook.stop)

#    def test_key(self):
#        self.assertEqual(''.join(map(str, range(42, 78))),
#                self.base_hook.get_key())

class HookTest(unittest.TestCase):
    def setUp(self):
        self.test_filename = 'test/file/name.py'
        self.test_tokens = ['%d' % x for x in xrange(100)]
        self.test_start_index = 42
        self.test_stop_index = 77

        self.hook = hook.Hook(self.test_filename, self.test_tokens,
                self.test_start_index, self.test_stop_index)

    def test_next(self):
        expected_values = ['78', '79', '80', '81']
        for value, expected_value in itertools.izip(self.hook,
                expected_values):
            self.assertEqual(value, expected_value)

    def test_stop_iteration(self):
        # Iterate to the end
        for value in self.hook:
            pass
        self.assertEqual(self.hook.stop, '99')
        self.assertRaises(StopIteration, self.hook.next)

class ReversedHookTest(unittest.TestCase):
    def setUp(self):
        self.test_filename = 'test/file/name.py'
        self.test_tokens = ['%d' % x for x in xrange(100)]
        self.test_start_index = 42
        self.test_stop_index = 77

        self.hook = hook.Hook(self.test_filename, self.test_tokens,
                self.test_start_index, self.test_stop_index)

        self.reversed_hook = self.hook.reversed()

    def test_next(self):
        expected_values = ['41', '40', '39', '38', '37']

        for value, expected_value in itertools.izip(self.reversed_hook,
                expected_values):
            self.assertEqual(value, expected_value)

    def test_stop_iteration(self):
        # Iterate to the end
        for value in self.reversed_hook:
            pass
        self.assertEqual(self.reversed_hook.start, '0')
        self.assertRaises(StopIteration, self.reversed_hook.next)
