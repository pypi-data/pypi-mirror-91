# ZipDir

Zip dir is a small library for zipping directories recursively into zip files.

## Installation

    $ pip install zip-dir

## Usage

Either obtain the binary data

```python
    zipBits = zip_directory('/path/to/directory')
```


or else, specify an output file

```python
    zip_directory('/path/to/directory', outputFile = '/my/file.zip')
```
