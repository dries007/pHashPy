# pHashPy

**Python bindings for the [pHash](https://github.com/aetilius/pHash) (perceptual hashing) library.

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
