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

import hook

def create_hooks(filename, tokens, minimum_token_count):
    num_tokens = len(tokens)
    for start_token_index, t in enumerate(tokens):
        if start_token_index + minimum_token_count <= num_tokens:
            stop_token_index = start_token_index + minimum_token_count - 1
#            hook_key = _make_key(tokens, start_token_index, stop_token_index)
            yield hook.Hook(filename, tokens,
                    start_token_index, stop_token_index)

#def _make_key(tokens, start, stop):
#    return ''.join(tokens[i].token_value for i in xrange(start, stop))