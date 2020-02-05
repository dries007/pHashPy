# pHashPy

**Python bindings for the [pHash](https://github.com/aetilius/pHash) (perceptual hashing) library.**

Copyright (c) Dries007 2020. \
Licensed under [GPLv3](COPYING) (or later), as is pHash itself.

The project uses cppyy to create a small wrapper around pHash functions.

## Features

Working:
 
- Video hashing
- Image hashing (dct & mh)

Missing:

- Audio
- Text

## Usage

### As a Command Line Tool

You can use the tool as a command line utility to generate a list of hashes from a list of files.

Run `python -m pHashPy --help` for more info.

### As a Library

Import functions from the package's `__init__`, this will automatically load the required library files.
If you import the functions from the individual py files, you must call `helper.init` yourself. 

## Background Info

For more info on pHash:
    
- https://github.com/aetilius/pHash
- https://www.phash.org/
- https://www.phash.org/docs/design.html (Theory.)
- https://www.phash.org/docs/howto.html (Help for developers, archived as [DevelopmentGuide.md](./DevelopmentGuide.md).)

## Testing build manually

Using CentOS 7 (with docker container `quay.io/pypa/manylinux2014_x86_64`):

```bash
cd

yum install -y cmake3 libpng-devel libjpeg-turbo-devel libsamplerate-devel libsndfile-devel libtiff-devel libvdpau-devel libvorbis-devel
yum install -y epel-release

rpm -v --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
yum install -y ffmpeg-devel

git clone https://github.com/dries007/pHashPy.git
cd pHashPy
git submodule init
git submodule update

cd pHash

echo "include_directories(/usr/include/ffmpeg)" >> CMakeLists.txt
sed -i s/SHARED/STATIC/g CMakeLists.txt

mkdir build
cd build
cmake3 .. -DCMAKE_BUILD_TYPE=Release -DWITH_VIDEO_HASH=1 -DWITH_AUDIO_HASH=1
make -j
```
