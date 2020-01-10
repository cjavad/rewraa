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

# File structure in build/

## Blank/After clean
```py
├── README.md # This file
├── SETUPTOOLS_HELP.md # Setuptools help output, useful when trying to install
├── build.cmd # Windows build script
├── build.sh # POSIX build script
└── dist # Dist files, includes base files such as main.py and resource files such as snapcraft config
    ├── build.py # Cython build
    ├── create.py # Creates rewraa.pyx the file cython compiles into c
    ├── main.py # Arg parsing and most user interface for Rewraaa
    └── res # Resources dir
        ├── LICENSE # License file
        ├── MANIFEST.in # Include files manifest for setuptools
        ├── icon.png # Rewraa icon
        ├── rewraa # __main__ command that uses main.py
        ├── setup.py # Setuptools setup.py
        └── snapcraft.yaml # Snapcraft config
```

## After create

```py
├── README.md # This file
├── SETUPTOOLS_HELP.md # Setuptools help output, useful when trying to install
├── build.cmd # Windows build script
├── build.sh # POSIX build script
├── dist # Dist files, includes base files such as main.py and resource files such as snapcraft config
    ├── build.py # Cython build
    ├── create.py # Creates rewraa.pyx the file cython compiles into c
    ├── main.py # Arg parsing and most user interface for Rewraaa
    └── res # Resources dir
        ├── LICENSE # License file
        ├── MANIFEST.in # Include files manifest for setuptools
        ├── icon.png # Rewraa icon
        ├── rewraa # __main__ command that uses main.py
        ├── setup.py # Setuptools setup.py
        └── snapcraft.yaml # Snapcraft config
│   ├── rewraa.c # Cythonized output of rewraa.pyx
│   └── rewraa.pyx # Entire rewraa program compiled into one python file
└── release # Setuptools module folder
    ├── LICENSE # License file (from dist/)
    ├── MANIFEST.in # Include files manifest for setuptools (from dist/)
    ├── icon.png # Rewraa icon (from dist/)
    ├── rewraa # __main__ command that uses main.py (from dist/)
    ├── rewraa.c # Cythonized output of rewraa.pyx (from dist/ after create)
    ├── setup.py # Setuptools setup.py (from dist/)
    └── snapcraft.yaml # Snapcraft config (from dist/)
```

## After build

```py
├── README.md # This file
├── SETUPTOOLS_HELP.md # Setuptools help output, useful when trying to install
├── build.cmd # Windows build script
├── build.sh # POSIX build script
├── dist # Unchanged
└── release # Changes documented
    ├── LICENSE
    ├── MANIFEST.in
    ├── build # build files are system dependant this is how it'll look on macosx
    │   ├── bdist.macosx-10.9-x86_64
    │   ├── lib.macosx-10.9-x86_64-3.7
    │   │   └── rewraa.cpython-37m-darwin.so
    │   └── temp.macosx-10.9-x86_64-3.7
    │       └── rewraa.o
    ├── dist # release/dist files are packaged setuptools modules
    │   ├── rewraa-1.6.1-cp37-cp37m-macosx_10_9_x86_64.whl
    │   ├── rewraa-1.6.1.macosx-10.9-x86_64.tar.gz
    │   └── rewraa-1.6.1.tar.gz
    ├── icon.png
    ├── rewraa
    ├── rewraa.c
    ├── rewraa.egg-info # pypi egg-info folder
    │   ├── PKG-INFO
    │   ├── SOURCES.txt
    │   ├── dependency_links.txt
    │   ├── entry_points.txt
    │   ├── requires.txt
    │   └── top_level.txt
    ├── setup.py
    └── snapcraft.yaml
```

From here on
