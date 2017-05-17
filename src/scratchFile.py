from fs import *
# from tester_answers2 import *
from tester_answers import *

testfile = "../data/smallimg0.ext2.img"
# testfile = "../data/mediumimg0.ext2.img"
ext2fs = ext2(testfile)
# print ext2fs.superbloc
print ext2fs.blocSize
print ext2fs.indirectBlocksCount
print ext2fs.doubleIndirectBlockCount
# print "##############"
# print ext2fs.bgroup_desc_list
# print "##############"
# print "========"
# for i in ext2fs.bgroup_desc_list:
#     print i
#     print "=========="
# print len(ext2fs.bgroup_desc_list)
# print ext2fs.groupCnt
# print ext2fs.inode_map
# print ext2fs.bloc_map
# print ext2fs.superbloc.s_inodes_count
# print ext2fs.groupCnt
# print ext2fs.superbloc.s_inodes_per_group
# print ext2fs.inodes_list[-1]
# print "====="
# print INODELIST[-1]
# print len(ext2fs.inodes_list)
# print len(INODELIST)

dir_bmap_list = []
inode_num = 297
for i in range(0, 12):
    bmap_bloc = ext2fs.bmap(ext2fs.inodes_list[inode_num], i)
    dir_bmap_list.append(bmap_bloc)

print dir_bmap_list

indir_bmap_list = []
for i in range(12, (ext2fs.blocSize / 4) + 12):
    bmap_bloc = ext2fs.bmap(ext2fs.inodes_list[inode_num], i)
    indir_bmap_list.append(bmap_bloc)

print indir_bmap_list

dbl_indir_bmap_list = []
for i in range((ext2fs.blocSize / 4) + 12, 1024):
    bmap_bloc = ext2fs.bmap(ext2fs.inodes_list[inode_num], i)
    dbl_indir_bmap_list.append(bmap_bloc)
print dbl_indir_bmap_list
print DBLINDIRMAP
