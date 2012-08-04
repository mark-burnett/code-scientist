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

import functools
import os.path
import re

def regex_filter(regex, iterable):
    compiled_re = re.compile(regex)
    return filter(compiled_re.search, iterable)

def compose(function_sequence, target):
    value = target
    for f in function_sequence:
        value = f(value)
    return value

def walk_files(path):
    if os.path.isfile(path):
        yield path
        return

    for directory, subdirs, files in os.walk(path):
        for f in files:
            yield os.path.join(directory, f)

def slurp_file(filename):
    return open(filename, 'r').read()

def memoize(func):
    cache = {}
    @functools.wraps(func)
    def memoizing_wrapper(*args):
        result = cache.get(args)
        if result is None:
            result = func(*args)
            cache[args] = result
        return result
    return memoizing_wrapper
