from bloc_device import *
from fs import *
from fs_superbloc import *
from fs_api import *
from bitarray import *
from tester_answers import *
import unittest
import os
import sys

testfile = "../data/smallimg0.ext2.img"
ext2fs = ext2(testfile)
