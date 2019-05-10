@echo off
python -c "import yaml"
if %errorlevel% neq 0 (
	echo installing conan,please wait..
	pip install conan
	if %errorlevel% neq 0 echo fail to install conan An error occured in %~n0, bailing out & exit /b %errorlevel%
	echo conan is installed...
)

set "Path=%Path%;%programfiles%\7-Zip"
set "VCPKG_USERNAME=NOT_SET_YET"
set "VCPKG_API_KEY=NOT_SET_YET"
call python conan_script\vcpkgbin.py %*
