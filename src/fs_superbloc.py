# -*- coding: utf-8 -*-
import struct
from bloc_device import bloc_device


class ext2_superbloc(object):
    SUPERBLOC_OFFSET = 1024
    SUPERBLOC_SIZE = 1024

    def __init__(self, diskfilename):
        # The superblock is always located at byte offset 1024 from the
        # start of the disk or partition.
        # => 1. Open diskfilename
        # => 2. Read the serialized superbloc content
        # => 3. Unserialized it
        file = open(diskfilename)
        file.seek(self.SUPERBLOC_OFFSET)
        self.read_super(file.read(self.SUPERBLOC_SIZE))
        file.close()
        return

    def read_super(self, raw_sb):
        self.s_inodes_count = struct.unpack("<I", raw_sb[0:4])[0]
        self.s_blocks_count = struct.unpack("<I", raw_sb[4:8])[0]
        self.s_r_blocks_count = struct.unpack("<I", raw_sb[8:12])[0]
        self.s_free_blocks_count = struct.unpack("<I", raw_sb[12:16])[0]
        self.s_free_inodes_count = struct.unpack("<I", raw_sb[16:20])[0]
        self.s_first_data_block = struct.unpack("<I", raw_sb[20:24])[0]
        self.s_log_block_size = struct.unpack("<I", raw_sb[24:28])[0]
        self.s_log_frag_size = struct.unpack("<I", raw_sb[28:32])[0]
        self.s_blocks_per_group = struct.unpack("<I", raw_sb[32:36])[0]
        self.s_frags_per_group = struct.unpack("<I", raw_sb[36:40])[0]
        self.s_inodes_per_group = struct.unpack("<I", raw_sb[40:44])[0]
        self.s_mtime = struct.unpack("<I", raw_sb[44:48])[0]
        self.s_wtime = struct.unpack("<I", raw_sb[48:52])[0]

        self.s_mnt_count = struct.unpack("<H", raw_sb[52:54])[0]
        self.s_max_mnt_count = struct.unpack("<H", raw_sb[54:56])[0]
        self.s_magic = struct.unpack("<H", raw_sb[56:58])[0]
        self.s_state = struct.unpack("<H", raw_sb[58:60])[0]
        self.s_errors = struct.unpack("<H", raw_sb[60:62])[0]
        self.s_minor_rev_level = struct.unpack("<H", raw_sb[62:64])[0]

        self.s_lastcheck = struct.unpack("<I", raw_sb[64:68])[0]
        self.s_checkinterval = struct.unpack("<I", raw_sb[68:72])[0]
        self.s_creator_os = struct.unpack("<I", raw_sb[72:76])[0]
        self.s_rev_level = struct.unpack("<I", raw_sb[76:80])[0]
        self.s_def_resuid = struct.unpack("<H", raw_sb[80:82])[0]
        self.s_def_resgid = struct.unpack("<H", raw_sb[82:84])[0]

        self.s_first_ino = struct.unpack("<I", raw_sb[84:88])[0]
        self.s_inode_size = struct.unpack("<H", raw_sb[88:90])[0]
        self.s_block_group_nr = struct.unpack("<H", raw_sb[90:92])[0]

    # get fs attributes
    # f_bfree is use to compute the "used" field from df command
    # f_bavail is the available number of blocs
    def statfs(self, path):
        # TODO check what to do here
        stat = {
            'f_bsize': 0,
            'f_frsize': 0,
            'f_blocks': 0,
            'f_bfree': 0,
            'f_bavail':0,
            'f_files':0,
            'f_free':0,
            'f_favail':0,
            'f_flag':0,
            'f_namemax':0
        }
        return stat

    def __str__(self):
        return "block_per_group:" + str(self.s_blocks_per_group) + "\n" + \
               "number of inodes:" + str(self.s_inodes_count) + "\n" + \
               "device size in blocs:" + str(self.s_blocks_count) + "\n" + \
               "number of reserved blocs:" + str(self.s_r_blocks_count) + "\n" + \
               "free block counts:" + str(self.s_free_blocks_count) + "\n" + \
               "free inodes counts:" + str(self.s_free_inodes_count) + "\n" + \
               "bloc index of first data block:" + str(self.s_first_data_block) + "\n" + \
               "log_block_size:" + str(self.s_log_block_size) + "\n" + \
               "inodes_per_group:" + str(self.s_inodes_per_group) + "\n" + \
               "magic number:" + str("{:04X}").format(self.s_magic) + "\n" + \
               "state:" + str(self.s_state) + "\n" + \
               "s_rev_level:" + str(self.s_rev_level) + "\n" + \
               "def_resuid:" + str(self.s_def_resuid) + "\n" + \
               "def_resgid:" + str(self.s_def_resgid) + "\n" + \
               "first_ino:" + str(self.s_first_ino) + "\n" + \
               "inode_size:" + str(self.s_inode_size) + "\n" + \
               "s_block_group_nr:" + str(self.s_block_group_nr)
