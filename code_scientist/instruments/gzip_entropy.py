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
import tempfile

from code_scientist.instruments import file_wrappers
from code_scientist import utils

class GzipEntropy(object):
    def __init__(self, file_filters=[]):
        self.file_filters = file_filters

    def make_measurements(self, specimen_group):
        tar_archive = file_wrappers.TarWrapper()
        self._add_group_to_tar_archive(tar_archive, specimen_group)

        compressed_file = self._compress_archive(tar_archive)

        uncompressed_size = tar_archive.size
        compressed_size = compressed_file.size

        result = {
                'information_content': compressed_size,
                'DRYness':
                    float(compressed_size) / uncompressed_size }

        return result

    def make_comparative_measurements(self,
            old_specimen_group, new_specimen_group):
        pass


    def _add_group_to_tar_archive(self, tar_archive, specimen_group):
        for filename in specimen_group:
            filtered_file = self._filter_file(filename)
            tar_archive.add_file(filtered_file)
            filtered_file.close()

    def _filter_file(self, filename):
        result_obj = tempfile.TemporaryFile()
        source_obj = open(filename)

        for line in source_obj:
            filtered_line = utils.compose(self.file_filters, line)
            if filtered_line:
                result_obj.write(filtered_line)

        source_obj.close()
        result_obj.seek(0)
        return result_obj

    def _compress_archive(self, tar_archive):
        compressed_file = file_wrappers.GzipWrapper()
        tar_archive.seek(0)

        for line in tar_archive:
            compressed_file.write(line)

        compressed_file.finish()
        return compressed_file
