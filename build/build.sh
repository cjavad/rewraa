#!/bin/bash

# building into release

if [ -z ${GPGKEY+x} ]
then 
    GPGKEY="EC3BA849662CD0C6E206E0671D25EEAE9626AF3E"
else
    GPGKEY=$GPGKEY
fi

if [ "$1" == "clean" ];
then
    chmod 777 ./release
    rm -rf ./release
    rm ./rewraa.c
    rm ./rewraa.pyx
    exit
fi 

if [ "$1" == "build" ];
then
    command -v python3  >/dev/null 2>&1 || { echo >&2 "I require python3 but it's not installed.  Aborting."; exit 1; }
    if [ ! -f ./release/setup.py ]; then 
        echo Project has not been created yet
        exit
    fi
    cd ./release/
    # Build
    python3 setup.py build
    python3 setup.py sdist
    python3 setup.py bdist
    python3 setup.py bdist_wheel
    # snapcraft
    exit
fi

if [ "$1" == "create" ];
then
    command -v python3  >/dev/null 2>&1 || { echo >&2 "I require python3 but it's not installed.  Aborting."; exit 1; }
    python3 ./create.py
    python3 ./build.py
    mkdir ./release
    cp ./resources/* ./release
    cp ./rewraa.c ./release/rewraa.c
    cd ./release
    ls
    echo "Use setup.py build to build and setup.py install for installing package"
    exit
fi


echo "Use build, create or clean as the first argument"
cd ..
exit