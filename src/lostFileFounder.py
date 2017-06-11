from fs import ext2
import sys
from fs_api import ext2_file_api
import os
import struct


def main(imageFilePath):
    print "You want to search in " + imageFilePath
    fs = ext2(imageFilePath)

    list = getAllDeletedPaths(fs, "/")

    print list


def getAllDeletedPaths(fs, startpath):
    api = ext2_file_api(fs)

    fd = api.open(startpath)
    data = api.read(fd, 0, fs.inodes_list[api.openFDs[fd]].i_size)

    dirList = []
    start = 0
    inodeNum = 1

    while inodeNum != 0 or start == len(data):
        tempStart = start

        if tempStart + 4 >= len(data):
            break
        inodeNum = struct.unpack_from("<I", data, tempStart)[0]
        tempStart += 4

        if tempStart + 2 >= len(data):
            break
        recLength = struct.unpack_from("<H", data, tempStart)[0]
        tempStart += 2

        if tempStart + 1 >= len(data):
            break
        nameLength = struct.unpack_from("<B", data, tempStart)[0]
        tempStart += 1

        if tempStart + 1 >= len(data):
            break
        fileType = struct.unpack_from("<B", data, tempStart)[0]
        tempStart += 1

        if tempStart + nameLength >= len(data):
            break
        filename = data[tempStart:tempStart + nameLength]
        start += recLength
        if filename == "." or filename == "..":
            continue
        if (fs.inodes_list[inodeNum].i_mode >> (4 * 3)) == 4:
            dirList.extend(getAllDeletedPaths(fs, startpath + (os.sep if startpath != "/" else "") + filename))
        elif fs.inode_map[inodeNum] == 0:
            dirList.append(startpath + (os.sep if startpath != "/" else "") + filename)
    api.close(fd)
    return dirList


if __name__ == '__main__':
    main(sys.argv[1])
