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

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer

import base

def make_many_to_many_table(a, b):
    table_name = "%s_%ss" % (a, b)
    result = Table(table_name, base.Base.metadata,
            Column('%s_id' % a, Integer, ForeignKey('%s.id' % a),
                primary_key=True, nullable=False),
            Column('%s_id' % b, Integer, ForeignKey('%s.id' % b),
                primary_key=True, nullable=False))
    return result

file_set_files = make_many_to_many_table('file_set', 'file')

snapshot_tags = make_many_to_many_table('snapshot', 'tag')
file_set_tags = make_many_to_many_table('file_set', 'tag')
file_tags     = make_many_to_many_table('file', 'tag')
function_tags = make_many_to_many_table('function', 'tag')
