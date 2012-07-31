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

import algorithm

class Duplication(object):
    def __init__(self, exact_hash_manager=None,
            structural_hash_manager=None,
            exact_minimum_count=100,
            structural_minimum_count=200,
            lexer=None):
        self._exact_hash_manager = exact_hash_manager
        self._structural_hash_manager = structural_hash_manager

        self._exact_minimum_count = exact_minimum_count
        self._structural_minimum_count = structural_minimum_count

        self._lexer = lexer

    def make_measurements(self, filenames):
        all_tokens = dict((f, self._lexer.get_tokens(f)) for f in filenames)

        exact_matches = algorithm.find_duplication(all_tokens,
                self._exact_hash_manager, self._exact_minimum_count)

        structural_matches = algorithm.find_duplication(all_tokens,
                self._structural_hash_manager, self._structural_minimum_count)

        total_tokens = sum(len(tokens) for tokens in all_tokens.itervalues())
        return _create_report(exact_matches, structural_matches,
                total_tokens)


def _create_report(exact_matches, structural_matches, total_tokens):
    exact_duplicated_token_count = _count_duplicate_tokens(exact_matches)
    structural_duplicated_token_count = _count_duplicate_tokens(
            structural_matches)

    return { 'total_tokens': total_tokens,
             'exact_duplication_fraction':
                 float(exact_duplicated_token_count) / total_tokens,
             'structural_duplication_fraction':
                 float(structural_duplicated_token_count) / total_tokens,
             'exact_matches': len(exact_matches),
             'structural_matches': len(structural_matches) }

def _count_duplicate_tokens(matches):
    total = 0
    for match_set in matches:
        token_counts = [m.stop_index - m.start_index for m in match_set]
        total += sum(token_counts) - max(token_counts)
    return total
