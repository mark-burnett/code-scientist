from code_scientist.instruments import gzip_entropy, entropy
from code_scientist.specimen_groups import regex

from code_scientist.filters.regex import empty_line, comment_line

def main():
    sg = regex.RegexSpecimenGroup(
'/home/mark/research/filament-dynamics/actin_dynamics',
            '.*\.py$')
    m = entropy.Entropy(file_filters=[empty_line, comment_line])

    results = m.make_measurements(sg, sg)
    print results

if '__main__' == __name__:
    main()
