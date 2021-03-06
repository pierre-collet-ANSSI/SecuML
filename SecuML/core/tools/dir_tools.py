# SecuML
# Copyright (C) 2016-2018  ANSSI
#
# SecuML is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# SecuML is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with SecuML. If not, see <http://www.gnu.org/licenses/>.

import hashlib
import os
import shutil


# If the directory exists, it is deleted
# A new directory is created
def createDirectory(directory):
    removeDirectory(directory)
    os.makedirs(directory)


# If the directory exists, it is deleted
def removeDirectory(directory):
    if os.path.isdir(directory):
        shutil.rmtree(directory)


def compute_hash(filename, kind='md5'):
    BLOCKSIZE = 65536
    if kind == 'md5':
        hasher = hashlib.md5()
    elif kind == 'sha1':
        hasher = hashlib.sha1()
    else:
        assert(False)
    with open(filename, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return hasher.hexdigest()
