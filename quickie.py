#!/usr/bin/env python
import pprint
#from code_scientist.instruments import entropy, duplication
from code_scientist.instruments import duplication
from code_scientist.specimen_groups import regex

from code_scientist.filters.regex import empty_line, comment_line

def main():
    sg = regex.RegexSpecimenGroup(
#'/home/mark/projects/SQLAlchemy-0.7.4/lib/sqlalchemy',
'/home/mark/research/filament-dynamics/actin_dynamics',
#'/home/mark/cs/',
#            'dup_test_.*\.py$')
            '.*\.py$')
#'/home/mark/research/filament-dynamics/cpp_stochastic',
#            '.*\.cpp$')

#    entropy_instrument = entropy.Entropy(file_filters=[empty_line, comment_line])
#    results = entropy_instrument.make_measurements(sg, sg)

#    filtered_sg = apply_filters(sg, [empty_line, comment_line])

#    duplication_instrument = duplication.Duplication()
    duplication_instrument = duplication.Duplication()
    results = duplication_instrument.make_measurements(sg)
    pprint.pprint(results)

if '__main__' == __name__:
    main()
