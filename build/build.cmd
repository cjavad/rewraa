@echo off
REM Building to release

IF "%1"=="clean" (
    rd /s /q .\release
    del .\rewraa.pyx
    del .\rewraa.c
    goto END
)

IF "%1"=="build" (
    py --version >nul 2>&1 && ( echo Found Python ) || (
        echo Python was not found
    )
    IF NOT EXIST .\release\setup.py (
        echo Project is not built
        goto END
    )
    cd .\release
    REM Build
    py setup.py build
    py setup.py sdist
    py setup.py bdist
    py setup.py bdist_wheel
    REM Build for windows
    py setup.py bdist_wininst
    goto END

)

IF "%1"=="create" (
    py --version >nul 2>&1 && ( echo Found Python ) || (
        echo Python was not found
    )
    py .\create.py
    py .\build.py build_ext --inplace
    mkdir .\release
    copy .\resources\* .\release
    copy .\rewraa.c .\release\rewraa.c
    cd .\release
    dir
    echo "Use setup.py build to build and setup.py install for installing package"
    goto END
) ELSE (
    echo Use create, build or clean as the first argument
    goto END
)

:END 