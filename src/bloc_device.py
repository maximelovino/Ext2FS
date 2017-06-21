# -*- coding: utf-8 -*-
# emulate a simple bloc device using a file
# reading it only by bloc units

class bloc_device(object):
    def __init__(self, blksize, pathname):
        self.blksize = blksize
        self.pathname = pathname
        self.file = open(pathname)
        return

    def read_bloc(self, bloc_num, numofblk=1):
        offset = bloc_num * self.blksize
        size = numofblk * self.blksize
        self.file.seek(offset)
        return self.file.read(size)
