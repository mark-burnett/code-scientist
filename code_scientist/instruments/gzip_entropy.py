import gzip
import os
import tarfile
import tempfile

from code_scientist import utils

class GzipEntropy(object):
    def __init__(self, file_filters=[]):
        self.file_filters = file_filters

    def make_measurements(self, specimen_group):
        tar_archive, bare_tar_file = self._create_tar_archive()
        self._add_group_to_tar_archive(tar_archive, specimen_group)
        tar_archive.close()

        compressed_file = self._compress_archive(bare_tar_file)

        bare_tar_file.flush()
        uncompressed_size = os.fstat(bare_tar_file.fileno()).st_size
        bare_tar_file.close()

        compressed_file.flush()
        compressed_size = os.fstat(compressed_file.fileno()).st_size
        compressed_file.close()

        result = {
                'information_content': compressed_size,
                'DRYness':
                    float(compressed_size) / uncompressed_size }

        return result

    def make_comparative_measurements(self,
            old_specimen_group, new_specimen_group):
        pass


    def _create_tar_archive(self):
        bare_file = tempfile.TemporaryFile()
        tar_archive = tarfile.open(fileobj=bare_file, mode='w')

        return tar_archive, bare_file

    def _add_group_to_tar_archive(self, tar_archive, specimen_group):
        for filename in specimen_group:
            filtered_file = self._filter_file(filename)
            tar_archive.addfile(tar_archive.gettarinfo(fileobj=filtered_file),
                    fileobj=filtered_file)
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
        bare_file = tempfile.TemporaryFile()
        compressed_file = gzip.GzipFile('', mode='wb', fileobj=bare_file)

        tar_archive.seek(0)
        for line in tar_archive:
            compressed_file.write(line)

        compressed_file.close()

        return bare_file
