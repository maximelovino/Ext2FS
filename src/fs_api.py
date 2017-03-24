# -*- coding: utf-8 -*-
import hexdump
import stat
import struct

class ext2_file_api(object):
    def __init__(self,filesystem):
        return

    # For all symlink shorter than 60 bytes long, the data is stored within the inode itself; 
    # it uses the fields which would normally be used to store the pointers to data blocks. 
    # This is a worthwhile optimisation as it we avoid allocating a full block for the symlink, 
    # and most symlinks are less than 60 characters long. 
    def readlink(self,path):
        return

    #open a file, i.e reserve a file descriptor
    #in the open file table, pointing to the corresponding 
    #inode. file descriptor is just an handle used to find the
    #corresponding inode. This handle is allocated by the filesystem.
    def open(self,path):
        return

    #release file descriptor entry, should we flush buffers : no, this is separate ?
    # openfiles[fd] = None 
    def close(self,fd):
        return

    #read nbytes from the file descriptor previously opened, starting at the given offset
    def read(self,fd,offset,count):
        return res
    
    #get the attributes of a node in a stat dictionnary : 
    # keys st_ctime, st_mtime, st_nlink, st_mode, st_size, st_gid, st_uid, st_atime
    #{'st_ctime': 1419027551.4907832, 'st_mtime': 1419027551.4907832, \
    # 'st_nlink': 36, 'st_mode': 16877, 'st_size': 4096, 'st_gid': 0, \
    #  'st_uid': 0, 'st_atime': 1423220038.6543322}
    def attr(self,path):
        return res 

    # implementation of readdir(3) : 
    # open the named file, and read each dir_entry in it
    # note that is not a syscall but a function from the libc§

    def dodir(self,path):
        return dirlist
