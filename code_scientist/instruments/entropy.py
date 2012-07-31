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

import os
import subprocess
import tempfile

from code_scientist import utils

class Entropy(object):
    def __init__(self, file_filters=[]):
        self.file_filters = file_filters

    def make_measurements(self, filenames, reference_filenames=None):
        if reference_filenames:
            return self._comparative_measurements(filenames,
                    reference_filenames)
        return self._singular_measurements(filenames)


    def _singular_measurements(self, filenames):
        aggregate_file = self._concatenate(filenames)

        uncompressed_size = _file_size(aggregate_file)
        compressed_size = _compress(aggregate_file)

        return {'information_content': compressed_size,
                'DRYness': float(compressed_size) / uncompressed_size }

    def _comparative_measurements(self,
            filenames, reference_filenames):
        aggregate_file = self._concatenate(filenames)

        uncompressed_size = _file_size(aggregate_file)
        compressed_size = _compress(aggregate_file)

        reference_aggregate_file = self._concatenate(reference_filenames)
        compressed_reference_size = _compress(reference_aggregate_file)

        combined_compressed_size = _combine_compress(aggregate_file,
                reference_aggregate_file)

        return {'information_content': compressed_size,
                'DRYness':
                    float(compressed_size) / uncompressed_size,
                'information_distance': combined_compressed_size
                    - compressed_reference_size }

    def _concatenate(self, filenames, output=None):
        if output is None:
            output = tempfile.NamedTemporaryFile(delete=False)
        for specimen in filenames:
            source = open(specimen)
            for line in source:
                filtered_line = utils.compose(self.file_filters, line)
                if filtered_line:
                    output.write(filtered_line)
        return output

def _file_size(f):
    f.flush()
    return os.fstat(f.fileno()).st_size

def _compress(source):
    name = source.name
    source.flush()
    subprocess.check_call("bzip2 -f -k %s" % name, shell=True)
    size = os.stat("%s.bz2" % name).st_size
    subprocess.check_call("rm %s.bz2" % name, shell=True)
    return size

def _combine_compress(a, b):
    a.flush()
    b.flush()
    subprocess.check_call("cat %s >> %s" % (a.name, b.name), shell=True)
    subprocess.check_call("bzip2 -f -k %s" % b.name, shell=True)

    size = os.stat("%s.bz2" % b.name).st_size
    subprocess.check_call("rm %s.bz2" % b.name, shell=True)
    return size
