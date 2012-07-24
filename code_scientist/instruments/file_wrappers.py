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

import gzip
import os
import tarfile
import tempfile

class TarWrapper(object):
    def __init__(self, file_object=None, mode='w'):
        if file_object:
            self._bare_file = file_object
        else:
            self._bare_file = tempfile.TemporaryFile()

        self._tar_handle = tarfile.open(fileobj=self._bare_file, mode=mode)

        self.seek = self._bare_file.seek

    def __iter__(self):
        return iter(self._bare_file)

    @property
    def size(self):
        self._bare_file.flush()
        return os.fstat(self._bare_file.fileno()).st_size

    def close(self):
        self._tar_handle.close()
        self._bare_file.close()

    def add_file(self, file_object):
        self._tar_handle.addfile(self._tar_handle.gettarinfo(
            fileobj=file_object), fileobj=file_object)


class GzipWrapper(object):
    def __init__(self, file_object=None, name='', mode='wb'):
        if file_object:
            self._bare_file = file_object
        else:
            self._bare_file = tempfile.TemporaryFile()

        self._gzip_handle = gzip.GzipFile(name, mode=mode,
                fileobj=self._bare_file)

#        self.seek = self._bare_file.seek
        self.write = self._gzip_handle.write

    @property
    def size(self):
        self._bare_file.flush()
        return os.fstat(self._bare_file.fileno()).st_size

    def finish(self):
        self._gzip_handle.close()

    def close(self):
        self._bare_file.close()
