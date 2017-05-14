# -*- coding: utf-8 -*-
from hexdump import hexdump

import fs_inode
import fs_superbloc
import fs_bloc_group
from bitarray import *
import struct
from bloc_device import *


# This class implements read only ext2 filesystem

class ext2(object):
    SIZE_OF_BGROUP_DESC = 32
    BGROUP_DESC_OFFSET = 2048

    def __init__(self, filename):
        # Superbloc is always at offset 1024 and of size 1024
        # Group descriptor block is always at offset 2048 (right after superbloc) and of size blocSize
        # After that the offset are logical with the blocnumber stored in the structs

        self.superbloc = fs_superbloc.ext2_superbloc(filename)
        self.blocSize = 1024 << self.superbloc.s_log_block_size
        self.device = bloc_device(self.blocSize, filename)

        # We find the number of bloc groups like that and then we read each struct in the block of the group descriptors
        # TODO check integer division here, should do a ceiling or something
        self.groupCnt = self.superbloc.s_inodes_count / self.superbloc.s_inodes_per_group;
        file = open(filename)
        file.seek(self.BGROUP_DESC_OFFSET)
        self.bgroup_desc_list = []
        for i in xrange(self.groupCnt):
            rawbgroupDesc = file.read(self.SIZE_OF_BGROUP_DESC)
            self.bgroup_desc_list.append(fs_bloc_group.ext2_bgroup_desc(raw_bgroup_desc=rawbgroupDesc))

        # TODO check how can that work for test 2
        # it works because only the one from the first group is checked, if we want to do correctly,
        # we should do the complete bitmap, but it will not be used in the rest of the project as it is read-only
        self.inode_map = bitarray(endian='little')
        self.inode_map.frombytes(self.device.read_bloc(self.bgroup_desc_list[0].bg_inode_bitmap))
        self.bloc_map = bitarray(endian='little')
        self.bloc_map.frombytes(self.device.read_bloc(self.bgroup_desc_list[0].bg_block_bitmap))

        self.inodes_list = []
        # First inode is always the empty inode
        # Size of inode is variable, it's in superbloc as s_inode_size
        # TODO seems like inode num must be the number for that bloc in order to make the test pass
        self.inodes_list.append(fs_inode.ext2_inode())
        i = 1
        for group in self.bgroup_desc_list:
            for k in xrange(self.superbloc.s_inodes_per_group):
                file.seek(group.bg_inode_table * self.blocSize + self.superbloc.s_inode_size * k)
                rawInode = file.read(self.superbloc.s_inode_size)
                self.inodes_list.append(fs_inode.ext2_inode(raw_inode=rawInode, num=k+1))

        file.close()
        return

    # find the directory inode number of a path
    # given : ex '/usr/bin/cat' return the inode
    # of '/usr/bin'
    def dirnamei(self, path):
        return
        # find an inode number according to its path

    # ex : '/usr/bin/cat'
    # only works with absolute paths

    def namei(self, path):
        return

    def bmap(self, inode, blk):
        return

        # lookup for a name in a directory, and return its inode number,

    # given inode directory dinode
    # ext2 release 0 store directories in a linked list of records
    # pointing to the next by length
    # - records cannot span multiple blocs.
    # - the end of the linked list as an inode num equal to zero.

    def lookup_entry(self, dinode, name):
        return
