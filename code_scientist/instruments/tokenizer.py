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

import collections
import logging

import pygments
import pygments.lexers
import pygments.token

Token = collections.namedtuple('Token', 'line_number token_value token_type')

def tokenize(file_object):
    lexer = _fetch_lexer(file_object)
    raw_tokens = lexer.get_tokens_unprocessed(file_object.get_contents())

    sloc, tokens = _process_raw_tokens(raw_tokens)
    file_object.properties['tokens'] = tokens
    file_object.properties['SLOC'] = sloc

def _fetch_lexer(file_object):
    if file_object.file_type:
        logging.debug("Fetching lexer for type '%s'.", file_object.file_type)
        return pygments.lexers.get_lexer_by_name(file_object.file_type,
                stripall=True)
    elif file_object.name:
        logging.debug("Fetching lexer by filename '%s'.", file_object.name)
        return pygments.lexers.get_lexer_for_filename(file_object.name,
                stripall=True)
    else:
        logging.debug("Guessing lexer.")
        return pygments.lexers.guess_lexer(file_object.get_contents(),
                stripall=True)

def _process_raw_tokens(raw_tokens):
    processed_tokens = []
    line_number = 1
    sloc = 0
    code_on_last_line = False
    for file_position, token_type, token_value in raw_tokens:
        stripped_value = token_value.strip()

        token_line_count = token_value.count('\n')
        if token_line_count and code_on_last_line:
            sloc += token_line_count
            code_on_last_line = False

        if stripped_value and (token_type not in pygments.token.Comment):
            processed_tokens.append(Token(line_number,
                stripped_value, token_type))
            code_on_last_line = True

        line_number += token_line_count

    return sloc, processed_tokens
