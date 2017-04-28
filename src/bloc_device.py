# -*- coding: utf-8 -*-
# emulate a simple bloc device using a file
# reading it only by bloc units

class bloc_device(object):
    def __init__(self, blksize, pathname):
        self.blksize = blksize
        self.pathname = pathname
        return

    def read_bloc(self, bloc_num, numofblk=1):
        offset = bloc_num * self.blksize
        size = numofblk * self.blksize
        workingFile = open(self.pathname)
        workingFile.seek(offset)
        string = workingFile.read(size)
        workingFile.close()
        return string
