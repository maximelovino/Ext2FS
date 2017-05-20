# -*- coding: utf-8 -*-
from hexdump import *
import stat
import struct
import math


class ext2_file_api(object):
    def __init__(self, filesystem):
        self.fs = filesystem
        return

    # For all symlink shorter than 60 bytes long, the data is stored within the inode itself; 
    # it uses the fields which would normally be used to store the pointers to data blocks. 
    # This is a worthwhile optimisation as it we avoid allocating a full block for the symlink, 
    # and most symlinks are less than 60 characters long. 
    def readlink(self, path):
        return

    # open a file, i.e reserve a file descriptor
    # in the open file table, pointing to the corresponding
    # inode. file descriptor is just an handle used to find the
    # corresponding inode. This handle is allocated by the filesystem.
    def open(self, path):
        return self.fs.inodes_list[self.fs.namei(path)]

    # release file descriptor entry, should we flush buffers : no, this is separate ?
    # openfiles[fd] = None 
    def close(self, fd):
        return

    # read nbytes from the file descriptor previously opened, starting at the given offset
    def read(self, fd, offset, count):
        startingBlock = int(math.floor((offset * 1.0) / self.fs.blocSize))
        dataStart = offset % self.fs.blocSize
        data = ""
        i = startingBlock
        while (len(data) - dataStart) < count:
            toRead = self.fs.bmap(fd, i)
            i += 1
            if toRead == 0:
                break
            data += self.fs.device.read_bloc(toRead)
        return data[dataStart: dataStart + count]

    # get the attributes of a node in a stat dictionnary :
    # keys st_ctime, st_mtime, st_nlink, st_mode, st_size, st_gid, st_uid, st_atime
    # {'st_ctime': 1419027551.4907832, 'st_mtime': 1419027551.4907832, \
    # 'st_nlink': 36, 'st_mode': 16877, 'st_size': 4096, 'st_gid': 0, \
    #  'st_uid': 0, 'st_atime': 1423220038.6543322}
    def attr(self, path):
        inode = self.open(path)
        stat = {
            'st_ctime': inode.i_ctime,
            'st_mtime': inode.i_mtime,
            'st_atime': inode.i_atime,
            'st_nlink': inode.i_links_count,
            'st_mode': inode.i_mode,
            'st_size': inode.i_size,
            'st_gid': inode.i_gid,
            'st_uid': inode.i_uid,
        }
        return stat

        # implementation of readdir(3) :

    # open the named file, and read each dir_entry in it
    # note that is not a syscall but a function from the libc§

    def dodir(self, path):
        return dirlist
