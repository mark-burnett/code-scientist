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

import hash_manager
import factories
import lexer
import match_container

class Duplication(object):
    def __init__(self, minimum_token_count=100):
        self.minimum_token_count = minimum_token_count

    def make_measurements(self, specimen_group):
        all_tokens = dict((f, lexer.get_tokens(f)) for f in specimen_group)
        hooks = collections.defaultdict(list)
        matches = match_container.MatchContainer()
        hm = hash_manager.HashManager()

        for filename, tokenlist in all_tokens.iteritems():
#            print 'file:', filename, 'num_tokens:', len(tokenlist), 'num_lines:', tokenlist[-1].line_number
            hm.reset()
            for new_hook in factories.create_hooks(filename,
                    tokenlist, self.minimum_token_count):
                hook_key = hm.get_key(new_hook)
                for existing_hook in hooks[hook_key]:
                    matches.add(new_hook, existing_hook)
                hooks[hook_key].append(new_hook)

        return matches
