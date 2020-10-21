@setlocal enabledelayedexpansion

set script_dir=%~dp0
pushd %script_dir%..\

set profile=-pr=default
set build_dir=default

if NOT "%1"=="" (
    set profile=-pr=../conan/%1.txt
    set build_dir=%1
)

rmdir /s/q %build_dir%
mkdir %build_dir%
pushd %build_dir%

conan install -o cppserver:tests=True ../conan/conanfilelocal.py cppserver/1.0.0.0@ %profile% -g=virtualenv
conan source ../conan/conanfilelocal.py
conan build ../conan/conanfilelocal.py
