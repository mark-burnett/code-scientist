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

import pygments
import pygments.lexers
import pygments.token

from code_scientist.instruments.duplication.token import Token

def get_tokens(filename):
    code = open(filename, 'r').read()
    lexer = pygments.lexers.guess_lexer(code, stripall=True)

    raw_tokens = lexer.get_tokens_unprocessed(code)

    return _process_tokens(raw_tokens)

def _process_tokens(raw_tokens):
    result = []
    line_number = 1
    for file_position, token_type, token_value in raw_tokens:
        stripped_value = token_value.strip()
        if stripped_value and token_type not in pygments.token.Comment:
            result.append(Token(line_number, stripped_value))
        line_number += token_value.count('\n')
    return result
