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

import itertools

import match

def extract_match(left, right):
    backward_extent = _get_backward_extent(left, right)
    forward_extent = _get_forward_extent(left, right)

    l_start_index, l_start_line, r_start_index, r_start_line = backward_extent
    l_stop_index, l_stop_line, r_stop_index, r_stop_line = forward_extent

#    key = left.get_key(l_start_index, l_stop_index)
    key = ''.join(left.tokens[i].token_value
            for i in xrange(l_start_index, l_stop_index + 1))

    return key, [match.Match(left.filename, l_start_index, l_stop_index,
            l_start_line, l_stop_line),
        match.Match(right.filename, r_start_index, r_stop_index,
            r_start_line, r_stop_line)]

def _get_backward_extent(left, right):
    rleft = left.reversed()
    rright = right.reversed()

    left_index = left.start_index
    left_line = left.start.line_number
    right_index = right.start_index
    right_line = right.start.line_number

    for left_token, right_token in itertools.izip(rleft, rright):
        if left_token.token_value != right_token.token_value:
            break
        left_index -= 1
        right_index -= 1
        left_line = rleft.start.line_number
        right_line = rright.start.line_number
    return left_index, left_line, right_index, right_line

def _get_forward_extent(left, right):
    cleft = left.clone()
    cright = right.clone()

    left_index = left.stop_index
    left_line = left.stop.line_number
    right_index = right.stop_index
    right_line = right.stop.line_number

    for left_token, right_token in itertools.izip(cleft, cright):
        if left_token.token_value != right_token.token_value:
            break
        left_index += 1
        right_index += 1
        left_line = cleft.stop.line_number
        right_line = cright.stop.line_number
    return left_index, left_line, right_index, right_line
