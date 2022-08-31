# Checksum-Calculator

## Description

A simple checksum calculator for files. supports all algorithms available to
the hashlib module in python.

## Usage

Run the main.py file in the src dir. The program requires a `filepath` argument
to be provided. If the `filepath` argument is a directory the checksum of each
file in that folder will be calculated. To get a list of all available hashing
algorithms use the `-l` argument. To get modify the buffer size for when reading
files use the -b `argument`, default is set to 4096. The default algorithm used
is sha1, this can be changed with the `-a` argument.

```
$ python src/main.py -h
```

```
usage: checksum calculator [-h] [-a ALGORITHM] [-b BUFFERSIZE] [-l] filepath

positional arguments:
  filepath       paths to files or folders to checksum

options:
  -h, --help     show this help message and exit
  -a ALGORITHM   hash algorithm, default: sha1
  -b BUFFERSIZE  buffer size, default: 4096
  -l             list all available algorithms
```

How to calculate a file's checksum:

```
$ py src/main.py test.txt

Algorithm: sha1

b6589fc6ab0dc82cf12099d1c2d40ab994e8410c : test.txt
```

How to calculate multiple files checksums:

```
$ py src/main.py multiple_files/

Algorithm: sha1

356a192b7913b04c54574d18c28d46e6395428ab : multiple_files/test1.txt
da4b9237bacccdf19c0760cab7aec4a8359010b0 : multiple_files/test2.txt
77de68daecd823babbb58edb1c8e14d7106e83bb : multiple_files/test3.txt
```