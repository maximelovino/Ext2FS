from fs import *

# testfile = "../data/smallimg0.ext2.img"
testfile = "../data/mediumimg0.ext2.img"
ext2fs = ext2(testfile)
print ext2fs.superbloc
print ext2fs.blocSize
print "##############"
print ext2fs.bgroup_desc_list
print "##############"
print "========"
for i in ext2fs.bgroup_desc_list:
    print i
    print "=========="
print len(ext2fs.bgroup_desc_list)
print ext2fs.groupCnt

print ext2fs.inode_map
print ext2fs.bloc_map
