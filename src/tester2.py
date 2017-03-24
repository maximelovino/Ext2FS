# -*- coding: utf-8 -*-
# filesystem and bloc device unit tests
# part 1: internal filesystem's functions.
# tested with python2 only

from bloc_device import *
from fs import *
from fs_superbloc import *
from fs_api import *
from bitarray import *
from tester_answers2 import *
import unittest
import os
import sys

# Test requirements : 
# - bloc_device class : modeling a disk drive with the following methods
#   -  read_bloc
# - ext2_superbloc class : a structure storing minix superblocs infos.
# - ext2_inode class : a structure modeling a minix inode
# - ext2_filesystem class : modeling ext2 filesystem class with the following methods:
#   - bmap(), lookup_entry(), namei()
# - bitarray class : used to store and manipulated inode and zone bitmaps in memory
#   member ofs minix_filesystem class

#testfile="ext2fs_lab1.img"
workfile="mediumimg0.ext2.img"
BLOCK_SIZE=2048

class Ext2Tester(unittest.TestCase):

    #test if the content returned by read_bloc 
    #is the one we expect.
    def test_1_bloc_device_read_bloc(self):
        self.disk=bloc_device(BLOCK_SIZE,workfile)
	bloc2=self.disk.read_bloc(2)
        bloc5=self.disk.read_bloc(5)
        bloc7=self.disk.read_bloc(7)
        bloc24=self.disk.read_bloc(24)
        self.assertEqual(bloc2,BLOC2)
        self.assertEqual(bloc5,BLOC5)
        self.assertEqual(bloc7,BLOC7)
        self.assertEqual(bloc24,BLOC24)
    
    #superbloc test : read it and check object values
    def test_2_super_bloc_read_super(self):
        sb=ext2_superbloc(workfile)

        self.assertEqual(sb.s_blocks_per_group,16384)
        self.assertEqual(sb.s_inodes_count,38400)
        self.assertEqual(sb.s_blocks_count,76800)
        self.assertEqual(sb.s_r_blocks_count,3840)
        self.assertEqual(sb.s_free_blocks_count,60222)
        self.assertEqual(sb.s_free_inodes_count,37560)
        self.assertEqual(sb.s_first_data_block,0)
        self.assertEqual(sb.s_log_block_size,1)
        self.assertEqual(sb.s_inodes_per_group,7680)
        self.assertEqual(sb.s_magic,0xEF53)
        self.assertEqual(sb.s_state,0)
        self.assertEqual(sb.s_rev_level,1)
        self.assertEqual(sb.s_def_resuid,0)
        self.assertEqual(sb.s_def_resgid,0)
        self.assertEqual(sb.s_first_ino,11)
        self.assertEqual(sb.s_inode_size,256)
    
    #bloc groups test
    def test_3_bloc_groups(self):
        self.ext2fs=ext2(workfile)
        self.assertEqual(self.ext2fs.bgroup_desc_list,BGROUPDESC);

    #inode and zone map tests
    #we only test the bitmap in the first bloc group
    def test_4_fs_inode_and_bloc_bitmaps(self):
        self.ext2fs=ext2(workfile)
        self.assertEqual(self.ext2fs.inode_map,INODEBITMAP1);
        self.assertEqual(self.ext2fs.bloc_map,ZONEBITMAP1);

    #inode list content test
    def test_5_fs_inode_list(self):
        self.ext2fs=ext2(workfile)
        self.assertEqual(self.ext2fs.inodes_list,INODELIST);

    #testing bmap function : just check that some bmaped
    #blocs have the right numbers.
    def test_6_fs_bmap(self):
        ext2fs=ext2(workfile)
        #bmap of inode 297, an inode with double indirects blocs
        #containing linux-0.95.tgz. Get all blocs of the file
        #direct blocs
        dir_bmap_list=[]
	inode_num=23306
        for i in range(0,12):
            bmap_bloc=ext2fs.bmap(ext2fs.inodes_list[inode_num],i)
            dir_bmap_list.append(bmap_bloc)
        self.assertEqual(dir_bmap_list,DIRMAP)
        
        #indirect blocs
        indir_bmap_list=[]
        for i in range(12,(BLOCK_SIZE/4)+12):
            bmap_bloc=ext2fs.bmap(ext2fs.inodes_list[inode_num],i)
            indir_bmap_list.append(bmap_bloc)
        self.assertEqual(indir_bmap_list,INDIRMAP)
        
        #double indirect blocs
        dbl_indir_bmap_list=[]
        for i in range((BLOCK_SIZE/4)+13,1024):
            bmap_bloc=ext2fs.bmap(ext2fs.inodes_list[inode_num],i)
            dbl_indir_bmap_list.append(bmap_bloc)
        self.assertEqual(dbl_indir_bmap_list,DBLINDIRMAP)

    #testing lookup_entry function : give a known inode 
    #number, and name, expect another inode number
    #do a few lookups
    def test_7_fs_lookup_entry(self):
        ext2fs=ext2(workfile)
        #lookup_entry, inode 426 ("/usr/src/ps-0.97"), lookup for ps.c 
        inode=ext2fs.lookup_entry(ext2fs.inodes_list[23435],"ps.c")
        self.assertEqual(inode,LOOKUPINODE1)
        #lookup_entry, inode 113 ("/usr/src/linux/fs/minix"), lookup for namei.c 
        inode=ext2fs.lookup_entry(ext2fs.inodes_list[23122],"namei.c")
        self.assertEqual(inode,LOOKUPINODE2)

    #testing namei function. Test that a few paths return
    #the expected inode number.
    def test_8_fs_namei(self):
        ext2fs=ext2(workfile)
        paths=["/usr/src/linux/fs/open.c","/bin/bash","/","/usr/include/assert.h"]
        namedinodelist=[]
        for p in paths:
            namedinode=ext2fs.namei(p)
            namedinodelist.append(namedinode)
        self.assertEqual(namedinodelist,NAMEDINODES)
    
    #def read(self,fd,offset,count) 
    def test_9_fs_api_read(self):
        ext2fs=ext2(workfile)
    	fsapi=ext2_file_api(ext2fs)
    	fd=fsapi.open("/usr/src/archives/linux-0.95.tgz")
    	b=fsapi.read(fd,0,123456)
        self.assertEqual(b,API_READ1)
    	b=fsapi.read(fd,2000,2345)
        self.assertEqual(b,API_READ2)
    
    def test_a_fs_api_attr(self):
        ext2fs=ext2(workfile)
    	fsapi=ext2_file_api(ext2fs)
    	attr=fsapi.attr("/usr/src/archives/linux-0.95.tgz")
        self.assertEqual(attr,ATTR1)
    
    # implementation of readdir(3) : 
    # open the named file, and read each dir_entry in it
    # note that is not really a syscall.

    def test_b_fs_api_dodir(self):
        ext2fs=ext2(workfile)
    	fsapi=ext2_file_api(ext2fs)
        dirlist=fsapi.dodir("/usr/src/linux/include/linux")
        self.assertEqual(dirlist,DIRLIST1)
    
    # implementation of readlink(2) : 
    
    def test_c_fs_api_readlink(self):
        ext2fs=ext2(workfile)
    	fsapi=ext2_file_api(ext2fs)
    	rlink1=fsapi.readlink("/tcptraceroute")
    	rlink2=fsapi.readlink("/hahaha")
        self.assertEqual(rlink1,READLINK1)
        self.assertEqual(rlink2,READLINK2)


    def test_d_cleanup(self):
        #clean up
        os.system("rm *.pyc")
        return True

if __name__ == '__main__' :
    unittest.main()
