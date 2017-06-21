# Ext2 FileSystem project
A project by [Maxime Lovino](https://github.com/maximelovino) and [Thomas Ibanez](https://github.com/ProtectedVariable)
## Introduction
The idea of this System Programming project is to learn how the Ext2 filesystem works by programming an API to mount Ext2 images using [FUSE](https://github.com/libfuse/libfuse).

You can find some sample Ext2 images in the [data folder](https://github.com/maximelovino/Ext2FS/tree/master/data) of this project

## System requirements

This project works with Python 2, it has been tested running version 2.7.10

The following Python modules are required:
- `bitarray`
- `hexdump`
- `fusepy`
- `struct`

You can install them if they're not already present on your system by using [pip](https://pip.pypa.io/en/stable/)

## Usage

### Unit tests

You can run `tester1` and `tester2` by unzipping the archive containing the images in the [data folder](https://github.com/maximelovino/Ext2FS/tree/master/data) and replacing the path of the `smallimg0.ext2.img` and `mediumimg0.ext2.img` in each file respectively.

Then you can launch both tests with Python like this:
```
python testerX.py
```

### Mounting images with FUSE

You can also mount an image on your system by using our API. Note that for this you need to have the [FUSE](https://github.com/libfuse/libfuse) library installed on your computer.

To mount an image, first create a folder where you want to mount the image, then:

```
python ext2fuse.py <PathToImage> <MountPointPath>
```

To unmount the image, just press `CTRL+C` after closing all Finder/File Explorer/Terminal sessions windows accessing the mounted image.

