# -*- coding: utf-8 -*-

import fs_inode
import fs_superbloc
import fs_bloc_group
from bitarray import *
import struct
from bloc_device import *


# This class implements read only ext2 filesystem

class ext2(object):
    def __init__(self, filename):
        superbloc = fs_superbloc.ext2_superbloc(filename)
        self.blocSize = 1024 << superbloc.s_log_block_size
        self.device = bloc_device(self.blocSize, filename)
        # Contained in bloc 2
        self.bgroup_desc_list = [fs_bloc_group.ext2_bgroup_desc(raw_bgroup_desc=self.device.read_bloc(2))]
        # self.inode_map = bitarray(device.read_bloc(self.bgroup_desc_list[0].bg_inode_bitmap))
        # self.bloc_map = bitarray(device.read_bloc(self.bgroup_desc_list[0].bg_block_bitmap))
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
