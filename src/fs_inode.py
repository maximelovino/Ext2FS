# -*- coding: utf-8 -*-
import struct
import stat


# http://www.nongnu.org/ext2-doc/ext2.html#INODE-TABLE

class ext2_inode(object):
    # inodes can be initialized from given values or from raw bytes contents coming from the device
    def __init__(self, raw_inode=None, num=0, mode=0, uid=0, size=0, atime=0, ctime=0, mtime=0, dtime=0, gid=0,
                 nlinks=0, blocks=[]):
        if raw_inode is None:
            self.i_ino = num
            self.i_mode = mode
            self.i_uid = uid
            self.i_size = size
            self.i_atime = atime
            self.i_ctime = ctime
            self.i_mtime = mtime
            self.i_dtime = dtime
            self.i_gid = gid
            self.i_links_count = nlinks
            self.i_blocks = blocks
        else:
            self.i_ino = num
            self.i_mode = struct.unpack("<H", raw_inode[0:2])[0]
            self.i_uid = struct.unpack("<H", raw_inode[2:4])[0]
            self.i_size = struct.unpack("<I", raw_inode[4:8])[0]
            self.i_atime = struct.unpack("<I", raw_inode[8:12])[0]
            self.i_ctime = struct.unpack("<I", raw_inode[12:16])[0]
            self.i_mtime = struct.unpack("<I", raw_inode[16:20])[0]
            self.i_dtime = struct.unpack("<I", raw_inode[20:24])[0]
            self.i_gid = struct.unpack("<H", raw_inode[24:26])[0]
            self.i_links_count = struct.unpack("<H", raw_inode[26:28])[0]
            # TODO here there is an error with blocks being rewritten
            self.i_blocks = struct.unpack("<I", raw_inode[28:32])[0]
            self.i_flags = struct.unpack("<I", raw_inode[32:36])[0]
            self.i_osd1 = struct.unpack("<I", raw_inode[36:40])[0]
            self.i_blocks = [
                # 12 direct blocks = 12*1024 bytes = 0-12288 bytes max
                # 12 direct blocks = 12*4096 bytes = 49152 bytes max
                struct.unpack("<I", raw_inode[40:44])[0],
                struct.unpack("<I", raw_inode[44:48])[0],
                struct.unpack("<I", raw_inode[48:52])[0],
                struct.unpack("<I", raw_inode[52:56])[0],
                struct.unpack("<I", raw_inode[56:60])[0],
                struct.unpack("<I", raw_inode[60:64])[0],
                struct.unpack("<I", raw_inode[64:68])[0],
                struct.unpack("<I", raw_inode[68:72])[0],
                struct.unpack("<I", raw_inode[72:76])[0],
                struct.unpack("<I", raw_inode[76:80])[0],
                struct.unpack("<I", raw_inode[80:84])[0],
                struct.unpack("<I", raw_inode[84:88])[0],
                # 1 indirect block of 1024/4 block = 256*1024 = 12288-256k more bytes
                # 1 indirect block of 4096/4 block = 1024*4096 = 4M more bytes
                struct.unpack("<I", raw_inode[88:92])[0],
                # 1 double indirect block of 1024/4*1024/4 = 64k*1024 = 256k-64M more bytes
                # 1 double indirect block of 4096/4*4096/4 = 1M*4096 = 4G more bytes
                struct.unpack("<I", raw_inode[92:96])[0],
                # 1 triple indirect block of 1024/4*1024/4*1024/4 = 16M*1024 = 64M-16G more bytes
                # 1 triple indirect block of 4096/4*4096/4*4096/4 = 1G*4096 = 4T more bytes
                struct.unpack("<I", raw_inode[96:100])[0],
            ]
            self.i_generation = struct.unpack("<I", raw_inode[100:104])[0]
            self.i_file_acl = struct.unpack("<I", raw_inode[104:108])[0]
            self.i_dir_acl = struct.unpack("<I", raw_inode[108:112])[0]
            self.i_faddr = struct.unpack("<I", raw_inode[112:116])[0]

    def __eq__(self, other):
        if isinstance(other, ext2_inode):
            return self.i_ino == other.i_ino and \
                   self.i_mode == other.i_mode and \
                   self.i_uid == other.i_uid and \
                   self.i_size == other.i_size and \
                   self.i_atime == other.i_atime and \
                   self.i_ctime == other.i_ctime and \
                   self.i_mtime == other.i_mtime and \
                   self.i_dtime == other.i_dtime and \
                   self.i_gid == other.i_gid and \
                   self.i_links_count == other.i_links_count and \
                   self.i_blocks == other.i_blocks

    def __repr__(self):
        return "ext2_inode(" + "num=" + str(self.i_ino) + \
               ",mode=" + str(self.i_mode) + \
               ",uid=" + str(self.i_uid) + \
               ",size=" + str(self.i_size) + \
               ",atime=" + str(self.i_atime) + \
               ",ctime=" + str(self.i_ctime) + \
               ",mtime=" + str(self.i_ctime) + \
               ",dtime=" + str(self.i_dtime) + \
               ",gid=" + str(self.i_gid) + \
               ",nlinks=" + str(self.i_links_count) + \
               ",blocks=" + str(eval(repr(self.i_blocks))) + \
               ")"

    def __str__(self):
        return "i_ino:" + str(self.i_ino) + "\n" + \
               "mode:" + str("{:0x}").format(self.i_mode) + "\n" + \
               "uid:" + str(self.i_uid) + "\n" + \
               "i_size:" + str(self.i_size) + "\n" + \
               "i_atime:" + str(self.i_atime) + "\n" + \
               "i_gid:" + str(self.i_gid) + "\n" + \
               "i_links_count:" + str(self.i_links_count) + "\n" + \
               "i_blocks:" + str(self.i_blocks) + "\n" + \
               "IS_DIR : " + str(stat.S_ISDIR(self.i_mode)) + "\n" + \
               "IS_REG : " + str(stat.S_ISREG(self.i_mode)) + "\n"
