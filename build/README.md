# Installation scripts

build.sh (build.cmd) does a bunch of things in two modes

```MODE 1 - Creating``` 

```$ build.* create```

- Creates build dirs
- Prepares all source files from ./src
- Cleans files and sets up a setup.py module

```MODE 2 - Building```

```$ build.* build```

- Compresses source into a single file
- Convert file to C code with cython
- Copy setup and C files to release folder
- And finishes up

```MODE 3 - Cleaning```

```$ build.* clean```

- Removes compiled files from dist folder
- Removes Release folder

In the dist folder do we have the compiling and compressing 
scripts that does all the heavy lifting.