from fs import ext2
from tester_answers2 import *
from fs_api import ext2_file_api
# from tester_answers import *

from hexdump import hexdump

# testfile = "../data/smallimg0.ext2.img"
testfile = "../data/mediumimg0.ext2.img"
ext2fs = ext2(testfile)

# print ext2fs.inodes_list[2]
#
# data = ext2fs.device.read_bloc(1038)
# data += ext2fs.device.read_bloc(1112)
# data += ext2fs.device.read_bloc(1113)
# data += ext2fs.device.read_bloc(1402)
# data += ext2fs.device.read_bloc(1404)
#
# start = 0
# inodeNum = 1
# while inodeNum != 0:
#     tempStart = start
#     inodeNum = struct.unpack("<I", data[tempStart:tempStart+4])[0]
#     tempStart += 4
#     recLength = struct.unpack("<H", data[tempStart:tempStart +2])[0]
#     tempStart += 2
#     nameLength = struct.unpack("<B", data[tempStart:tempStart +1])[0]
#     tempStart += 1
#     fileType = struct.unpack("<B", data[tempStart:tempStart + 1])[0]
#     tempStart += 1
#     name = data[tempStart:tempStart + nameLength]
#     start += recLength
#     print inodeNum
#     print recLength
#     print nameLength
#     print fileType
#     print name
#     print "========"

fsapi = ext2_file_api(ext2fs)
rlink1 = fsapi.readlink("/tcptraceroute")
rlink2 = fsapi.readlink("/hahaha")
