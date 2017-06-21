# -*- coding: utf-8 -*-
import struct
import hexdump


class ext2_bgroup_desc(object):
    def __init__(self, raw_bgroup_desc=None, bg_block_bitmap=0, bg_inode_bitmap=0, bg_inode_table=0,
                 bg_free_blocks_count=0, bg_free_inodes_count=0, bg_used_dirs_count=0):
        if raw_bgroup_desc == None:
            self.bg_block_bitmap = bg_block_bitmap
            self.bg_inode_bitmap = bg_inode_bitmap
            self.bg_inode_table = bg_inode_table
            self.bg_free_blocks_count = bg_free_blocks_count
            self.bg_free_inodes_count = bg_free_inodes_count
            self.bg_used_dirs_count = bg_used_dirs_count
        else:
            self.bg_block_bitmap = struct.unpack("<I", raw_bgroup_desc[0:4])[0]
            self.bg_inode_bitmap = struct.unpack("<I", raw_bgroup_desc[4:8])[0]
            self.bg_inode_table = struct.unpack("<I", raw_bgroup_desc[8:12])[0]
            self.bg_free_blocks_count = struct.unpack("<H", raw_bgroup_desc[12:14])[0]
            self.bg_free_inodes_count = struct.unpack("<H", raw_bgroup_desc[14:16])[0]
            self.bg_used_dirs_count = struct.unpack("<H", raw_bgroup_desc[16:18])[0]

    def __eq__(self, other):
        if isinstance(other, ext2_bgroup_desc):
            return self.bg_block_bitmap == other.bg_block_bitmap and \
                   self.bg_inode_bitmap == other.bg_inode_bitmap and \
                   self.bg_free_blocks_count == other.bg_free_blocks_count and \
                   self.bg_free_inodes_count == other.bg_free_inodes_count and \
                   self.bg_used_dirs_count == other.bg_used_dirs_count

    def __repr__(self):
        return "ext2_bgroup_desc(" + "bg_block_bitmap=" + str(self.bg_block_bitmap) + \
               ",bg_inode_bitmap=" + str(self.bg_inode_bitmap) + \
               ",bg_inode_table=" + str(self.bg_inode_table) + \
               ",bg_free_blocks_count=" + str(self.bg_free_blocks_count) + \
               ",bg_free_inodes_count=" + str(self.bg_free_inodes_count) + \
               ",bg_used_dirs_count=" + str(self.bg_used_dirs_count) + \
               ")"

    def __str__(self):
        return "bg_desc_bg_block_bitmap:" + str(self.bg_block_bitmap) + "\n" + \
               "bg_desc_bg_inode_bitmap:" + str(self.bg_inode_bitmap) + "\n" + \
               "bg_desc_bg_inode_table:" + str(self.bg_inode_table) + "\n" + \
               "bg_desc_bg_free_blocks_count:" + str(self.bg_free_blocks_count) + "\n" + \
               "bg_desc_bg_free_inodes_count:" + str(self.bg_free_inodes_count) + "\n" + \
               "bg_desc_bg_used_dirs_count:" + str(self.bg_used_dirs_count)
