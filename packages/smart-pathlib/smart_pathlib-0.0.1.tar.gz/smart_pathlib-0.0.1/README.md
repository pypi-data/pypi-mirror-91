# smart_pathlib - utils for making common path operations interoperable with Cloud object storages

## What ?

`smart_pathlib` is highly inspired by `smart_open` and provide drop-in
replacement for Python part of `os`, `os.path`, `glob` modules functions such as
`exists`, `stat`, `listdir`, `glob`.

## Why ?

The goal is to provide a clean and Pythonic API for common file manipulations.
It simplifies rapid application development, making your code that manipulates
files interoperable with local file system and Cloud blob storage solutions
such as S3, GCS, Azure Blob Storage.

## Example

A drop-in replacement `os.path.exists` that operates on different storage types:

```python
# Test if a local file exists
from smart_pathlib import exists
assert exists('/Users/me/Downloads/test_file.txt')
```

```python
# Test if a file exists on GCS
from smart_pathlib import exists
assert exists('gs://my_bucket/test_file.txt')
```

## Installation

You can select the "flavor" of `smart_pathlib` to install, depending on your
storage provider:

```
pip install smart_pathlib[gcp]    # Install GCP deps
```

Or install all packages using:
```
pip install smart_pathlib[all]
```
