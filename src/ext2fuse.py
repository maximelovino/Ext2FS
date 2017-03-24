#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import errno
import fs
import fs_api

from fuse import FUSE, FuseOSError, Operations

class Ext2UserFS(Operations):
   
    def __init__(self,fileimage):
        self.api=fs_api.ext2_file_api(fs.ext2(fileimage))

    # Filesystem methods
    # ==================

    def getattr(self, path, fh=None):
        return self.api.attr(path)

    def readdir(self, path, fh):
        return iter(self.api.dodir(path))

    def readlink(self, path):
        return self.api.readlink(path)

    def statfs(self, path):
        return self.api.fs.superbloc.statfs(path)

    # File methods
    # ============

    def open(self, path, flags):
        return self.api.open(path)

    def read(self, path, length, offset, fh):
        return self.api.read(fh,offset,length)

    def release(self, path, fh):
        return self.api.close(fh)

def main(mountpoint, fileimage):
    FUSE(Ext2UserFS(fileimage), mountpoint, foreground=True, nothreads=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])
