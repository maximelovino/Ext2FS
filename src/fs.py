# -*- coding: utf-8 -*-

import fs_inode 
import fs_superbloc
import fs_bloc_group 
import bitarray
import struct
from bloc_device import *

#This class implements read only ext2 filesystem

class ext2(object):
    def __init__(self,filename):
        return
    #find the directory inode number of a path
    #given : ex '/usr/bin/cat' return the inode
    #of '/usr/bin' 
    def dirnamei(self,path):
        return 
    #find an inode number according to its path
    #ex : '/usr/bin/cat'
    #only works with absolute paths
                   
    def namei(self,path):
	return
    
    def bmap(self,inode,blk):
        return 
    
    #lookup for a name in a directory, and return its inode number, 
    #given inode directory dinode
    #ext2 release 0 store directories in a linked list of records
    #pointing to the next by length
    # - records cannot span multiple blocs.
    # - the end of the linked list as an inode num equal to zero.

    def lookup_entry(self,dinode,name):
        return 
