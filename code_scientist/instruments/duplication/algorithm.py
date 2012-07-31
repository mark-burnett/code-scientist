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
import itertools

import factories
import match_container

def find_duplication(all_tokens, hash_manager, minimum_match_length):
    hooks = collections.defaultdict(list)
    matches = match_container.MatchContainer()

    for filename, tokenlist in all_tokens.iteritems():
        hash_manager.reset()
        for new_hook in factories.create_hooks(filename,
                tokenlist, minimum_match_length):
            hook_key = hash_manager(new_hook)
            for existing_hook in hooks[hook_key]:
                matches.add(new_hook, existing_hook)
            hooks[hook_key].append(new_hook)

    return matches.values()
