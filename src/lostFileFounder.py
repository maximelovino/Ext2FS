from fs import ext2
import sys


def main(imageFilePath):
    print "You want to search in " + imageFilePath
    fs = ext2(imageFilePath)
    for i in xrange(len(fs.inode_map)):
        if fs.inode_map[i] == 0:
            print "======="
            print fs.inodes_list[i]
            print "======="


if __name__ == '__main__':
    main(sys.argv[1])
