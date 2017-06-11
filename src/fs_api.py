# -*- coding: utf-8 -*-
from hexdump import *
import stat
import struct
import math


class ext2_file_api(object):
    openFDs = []
    toFreeFDs = []

    def __init__(self, filesystem):
        self.fs = filesystem
        return

    # For all symlink shorter than 60 bytes long, the data is stored within the inode itself; 
    # it uses the fields which would normally be used to store the pointers to data blocks. 
    # This is a worthwhile optimisation as it we avoid allocating a full block for the symlink, 
    # and most symlinks are less than 60 characters long. 
    def readlink(self, path):
        fd = self.open(path)
        inodeNum = ext2_file_api.openFDs[fd]
        inode = self.fs.inodes_list[inodeNum]
        data = ''
        if inode.i_size <= 60:
            # read from bloc indexes direct
            data = struct.pack("<15I", *inode.i_blocks)
        else:
            # read classic way from blocks
            i = 0
            tempBlock = self.fs.bmap(inode, i)
            while tempBlock != 0:
                data += self.fs.device.read_bloc(tempBlock)
                i += 1
                tempBlock = self.fs.bmap(inode,i)

        return data.rstrip('\0')


    # open a file, i.e reserve a file descriptor
    # in the open file table, pointing to the corresponding
    # inode. file descriptor is just an handle used to find the
    # corresponding inode. This handle is allocated by the filesystem.
    def open(self, path):
        inodeNum = self.fs.namei(path)

        if len(ext2_file_api.toFreeFDs) == 0:
            ext2_file_api.openFDs.append(inodeNum)
            return len(ext2_file_api.openFDs) - 1
        else:
            idxToStore = ext2_file_api.toFreeFDs.pop()
            ext2_file_api.openFDs[idxToStore] = inodeNum
            return idxToStore

    # release file descriptor entry, should we flush buffers : no, this is separate ?
    # openfiles[fd] = None 
    def close(self, fd):
        ext2_file_api.toFreeFDs.append(fd)

    # read nbytes from the file descriptor previously opened, starting at the given offset
    def read(self, fd, offset, count):
        inodeNum = ext2_file_api.openFDs[fd]
        inode = self.fs.inodes_list[inodeNum]
        startingBlock = int(math.floor((offset * 1.0) / self.fs.blocSize))
        dataStart = offset % self.fs.blocSize
        data = ""
        i = startingBlock
        while (len(data) - dataStart) < count:
            toRead = self.fs.bmap(inode, i)
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
        fd = self.open(path)
        inodeNum = ext2_file_api.openFDs[fd]
        inode = self.fs.inodes_list[inodeNum]
        stat = {
            'st_ctime': int(inode.i_ctime),
            'st_mtime': int(inode.i_mtime),
            'st_atime': int(inode.i_atime),
            'st_nlink': int(inode.i_links_count),
            'st_mode': int(inode.i_mode),
            'st_size': int(inode.i_size),
            'st_gid': int(inode.i_gid),
            'st_uid': int(inode.i_uid),
            'st_blocks': int(math.ceil(inode.i_size / 512.0)),
            'st_blksize': int(self.fs.blocSize)
        }
        self.close(fd)
        return stat

        # implementation of readdir(3) :

    # open the named file, and read each dir_entry in it
    # note that is not a syscall but a function from the libc§

    def dodir(self, path):
        fd = self.open(path)
        inodeNum = ext2_file_api.openFDs[fd]
        inode = self.fs.inodes_list[inodeNum]
        data = ''
        for i in xrange(12):
            toRead = self.fs.bmap(inode, i)
            if toRead != 0:
                data += self.fs.device.read_bloc(toRead)

        dirList = []
        start = 0
        inodeNum = 1
        
        while inodeNum != 0 or start == len(data):
            tempStart = start
            if tempStart + 4 >= len(data):
                break
            inodeNum = struct.unpack("<I", data[tempStart:tempStart + 4])[0]
            tempStart += 4
            if tempStart + 2 >= len(data):
                break
            recLength = struct.unpack("<H", data[tempStart:tempStart + 2])[0]
            tempStart += 2
            if tempStart + 1 >= len(data):
                break
            nameLength = struct.unpack("<B", data[tempStart:tempStart + 1])[0]
            tempStart += 1
            if tempStart + 1 >= len(data):
                break
            fileType = struct.unpack("<B", data[tempStart:tempStart + 1])[0]
            tempStart += 1
            if tempStart + nameLength >= len(data):
                break
            filename = data[tempStart:tempStart + nameLength]
            start += recLength
            if inodeNum != 0:
                dirList.append(filename)
        self.close(fd)
        return dirList
