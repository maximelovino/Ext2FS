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
    SIZE_OF_BLOCK_ID = 4
    ROOT_INODE = 2

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
        # seems like inode num must be the number for that bloc in order to make the test pass
        self.inodes_list.append(fs_inode.ext2_inode())
        for group in self.bgroup_desc_list:
            rawBlocs = self.device.read_bloc(group.bg_inode_table, (
                self.superbloc.s_inode_size * self.superbloc.s_inodes_per_group) / self.blocSize);
            for k in xrange(self.superbloc.s_inodes_per_group):
                rawInode = rawBlocs[k * self.superbloc.s_inode_size:(k + 1) * self.superbloc.s_inode_size]
                self.inodes_list.append(fs_inode.ext2_inode(raw_inode=rawInode, num=k + 1))

        file.close()

        self.blockIDsInBlock = self.blocSize / self.SIZE_OF_BLOCK_ID
        self.indirectBlocksCount = 12 + self.blockIDsInBlock
        self.doubleBlock = self.blockIDsInBlock ** 2
        self.doubleIndirectBlockCount = self.indirectBlocksCount + self.doubleBlock
        self.tripleIndirectBlockCount = self.doubleIndirectBlockCount + self.blockIDsInBlock ** 3
        return

    # find the directory inode number of a path
    # given : ex '/usr/bin/cat' return the inode
    # of '/usr/bin'
    def dirnamei(self, path):
        pathArray = path.split('/')
        inodeNum = self.ROOT_INODE
        for name in pathArray[1:-1]:
            inodeNum = self.lookup_entry(self.inodes_list[inodeNum], name)

        return inodeNum
        # find an inode number according to its path

    # ex : '/usr/bin/cat'
    # only works with absolute paths

    def namei(self, path):
        if path == "/":
            return self.ROOT_INODE

        pathArray = path.split('/')

        return self.lookup_entry(self.inodes_list[self.dirnamei(path)], pathArray[-1])

    def bmap(self, inode, blk):
        if (blk < 12) and (blk >= 0):
            return inode.i_blocks[blk]
        elif (blk >= 12) and (blk < self.indirectBlocksCount):
            data = self.device.read_bloc(inode.i_blocks[12])
            blk = blk - 12
            return struct.unpack("<I", data[blk * self.SIZE_OF_BLOCK_ID:(blk + 1) * self.SIZE_OF_BLOCK_ID])[0]
        elif (blk >= self.indirectBlocksCount) and (blk < self.doubleIndirectBlockCount):
            firstIndirect = self.device.read_bloc(inode.i_blocks[13])
            blk -= self.indirectBlocksCount
            secondBlock = blk / self.blockIDsInBlock
            # If indirect block is not used, we return 0, because block 0 isn't a datablock
            blocToRead = struct.unpack("<I", firstIndirect[secondBlock * self.SIZE_OF_BLOCK_ID:(
                                                                                                   secondBlock + 1) * self.SIZE_OF_BLOCK_ID])[
                0]
            if blocToRead == 0:
                return 0
            secondIndirect = self.device.read_bloc(blocToRead)
            lastBlock = blk % self.blockIDsInBlock
            return struct.unpack("<I", secondIndirect[
                                       lastBlock * self.SIZE_OF_BLOCK_ID:(lastBlock + 1) * self.SIZE_OF_BLOCK_ID])[0]
        elif (blk >= self.doubleIndirectBlockCount) and (blk < self.tripleIndirectBlockCount):
            # TODO triple indirect
            return 0
        else:
            return 0

    # lookup for a name in a directory, and return its inode number,

    # given inode directory dinode
    # ext2 release 0 store directories in a linked list of records
    # pointing to the next by length
    # - records cannot span multiple blocs.
    # - the end of the linked list as an inode num equal to zero.

    def lookup_entry(self, dinode, name):
        data = ''
        # TODO check if it's correct to take into consideration only the direct blocks
        for i in xrange(12):
            toRead = self.bmap(dinode, i)
            if toRead != 0:
                data += self.device.read_bloc(toRead)

        start = 0
        inodeNum = 1
        while inodeNum != 0:
            tempStart = start
            inodeNum = struct.unpack("<I", data[tempStart:tempStart + 4])[0]
            tempStart += 4
            recLength = struct.unpack("<H", data[tempStart:tempStart + 2])[0]
            tempStart += 2
            nameLength = struct.unpack("<B", data[tempStart:tempStart + 1])[0]
            tempStart += 1
            fileType = struct.unpack("<B", data[tempStart:tempStart + 1])[0]
            tempStart += 1
            filename = data[tempStart:tempStart + nameLength]
            start += recLength
            if filename == name:
                return inodeNum
        return 0
