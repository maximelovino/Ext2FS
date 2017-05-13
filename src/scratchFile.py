from fs import *
from tester_answers2 import *
# from tester_answers import *

# testfile = "../data/smallimg0.ext2.img"
testfile = "../data/mediumimg0.ext2.img"
ext2fs = ext2(testfile)
# print ext2fs.superbloc
# print ext2fs.blocSize
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
for i in xrange(20):
    print i
    print "#####"
    print ext2fs.inodes_list[i]
    print "-----------"
    print INODELIST[i]
    print "#####"
# print "======"

# for node in ext2fs.inodes_list:
#     print node
#     print "======"
