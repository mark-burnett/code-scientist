from code_scientist.instruments import gzip_entropy
from code_scientist.specimen_groups import regex

from code_scientist.filters.regex import empty_line, comment_line

def main():
    sg = regex.RegexSpecimenGroup(
'/home/mark/research/filament-dynamics/actin_dynamics',
            '.*\.py$')
    m = gzip_entropy.GzipEntropy(file_filters=[empty_line, comment_line])

    results = m.make_measurements(sg)
    print results

if '__main__' == __name__:
    main()
