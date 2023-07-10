# Recursive File Finder (C)

This repository contains a recursive file finder utility implemented in C. The utility allows you to search for files and folders within a specified directory. It recursively traverses the directory structure, providing the path of the found items and counting the number of directories and files searched.

## Features

- Search for files and folders within a directory
- Recursive directory traversal to find matching items
- Output the path of the found items
- Count the total number of directories and files searched

## Usage

### Prerequisites

- C compiler (GCC or Clang)

### Instructions

1. Clone the repository:

   ```shell
   git clone https://github.com/axjh03/recursive-file-finder-c.git

2. Navigate to the project directory:
    ```shell
    cd recursive-file-finder-c

3. Compile the C file
    ```shell
    gcc finder.c -o finder


## Usage
### Finding a file recursively in the current directory:

```shell
./a.out -file filename.ext

Finding a folder recursively in the current directory:
```shell
./a.out -folder foldername

Finding a file recursively in a custom directory (absolute path):
```shell
./a.out -file filename.ext -dir /path/to/directory


Finding a folder recursively in a custom directory (relative path):
```shell
./a.out -folder foldername -dir ../path/to/directory