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

from code_scientist.instruments.duplication import factory, match_container, token

class Duplication(object):
    def __init__(self, minimum_token_count=100):
        self.minimum_token_count = minimum_token_count

    def make_measurements(self, specimen_group):
        all_tokens = dict((f, factory.get_tokens(f)) for f in specimen_group)
        matches = collections.defaultdict(match_container.MatchContainer)

        for filename, tokenlist in all_tokens.iteritems():
            skip = 0
            for chain_hash, token_iter in token.TokenWindowIterator(filename,
                    tokenlist, self.minimum_token_count):
                if skip > 0:
                    skip -= 1
                    continue
                skip = matches[chain_hash].add(token_iter)

        filtered_matches = _filter_matches(matches)

        token_count = sum(len(v) for v in all_tokens.itervalues())
        return _create_report(filtered_matches, token_count)

def _filter_matches(matches):
    actual_matches = []
    for key, mc in matches.iteritems():
        if mc.has_match:
            actual_matches.append(mc)
    return actual_matches

def _create_report(all_matches, token_count):
    if token_count:
        copied_token_count = 0
        matches = []
        for match_collection in all_matches:
            for match_identifiers in match_collection:
                matched_token_counts = [mi.token_count for mi in match_identifiers]
                copied_token_count += sum(matched_token_counts)
                copied_token_count -= max(matched_token_counts)
                these_matches = [(mi.filename, mi.start_line, mi.stop_line)
                        for mi in match_identifiers]
                matches.append(these_matches)
        return { 'duplication_fraction':
                    float(copied_token_count) / token_count,
                 'matches': matches }
    else:
        return { 'duplication_fraction': 0,
                 'matches': [] }
