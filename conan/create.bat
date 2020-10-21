@setlocal enabledelayedexpansion

set script_dir=%~dp0
pushd %script_dir%

set profile=-pr=default

if NOT "%1"=="" (
    set profile=-pr=%1.txt
)

conan create -o cppserver:tests=True . cppserver/1.0.0.0@ --build=missing --build=cppserver %profile%
