# `vcpkgbintray`
- generate library from vcpkg and then upload or download to or from bintray through conan
- so here conan is used as transport medium to upload and download vcpkg artifact to or from bintary.

## requirement
- 7zip
- python and pip should be set as environment variable

## Build
1. clone vcpkg folder
2. clone this repository and place it into vcpkg <root> path.

## Run
```bat
    vcpkgbin.bat <operation> <conanPackageName> <vcpkg portname> <vcpkg triplet>
```
### Operation
1. `install package`
    - example 1: [for installing and uploading bzip2:x64-windows-v141 package to server]
    ```bat
        vcpkgbin.bat install vcpkg/0.0.81-6@had/vcpkg bzip2 x64-windows-v141
    ```
    - example 2: [for installing and uploading bzip2:x64-windows-v141 and zlib:x64-windows-v141 package to server]
    ```bat
        vcpkgbin.bat install vcpkg/0.0.81-6@had/vcpkg "bzip2 zlib" x64-windows-v141
    ```
2. `upload package`
    - example 3: [for uploading all package installed in current vcpkg to server]
    ```bat
        vcpkgbin.bat upload vcpkg/0.0.81-6@had/vcpkg
    ```
3. `download package`
    - example 4: [for download bzip2:x64-windows-v141 package]
    ```bat
        vcpkgbin.bat download vcpkg/0.0.81-6@had/vcpkg bzip2 x64-windows-v141
    ```
4. `listing package present in remote`
    - example 5: [for listing list of triplet installed in remote vcpkg/0.0.81-6@had/vcpkg]
    ```bat
        vcpkgbin.bat list remote vcpkg/0.0.81-6@had/vcpkg
    ```
    - example 6: [for listing list of ports of x64-windows-v141 installed in remote vcpkg/0.0.81-6@had/vcpkg]
    ```bat
        vcpkgbin.bat list remote vcpkg/0.0.81-6@had/vcpkg x64-windows-v141
    ```
    - example 7: [for listing information of bzip2 of x64-windows-v141 installed in remote vcpkg/0.0.81-6@had/vcpkg]
    ```bat
        vcpkgbin.bat list remote vcpkg/0.0.81-6@had/vcpkg x64-windows-v141 bzip2
    ```
5. `listing package present in local`
    - example 8: [for listing list of triplet installed in current directory]
    ```bat
        vcpkgbin.bat list local
    ```
    - example 9: [for listing list of ports of x64-windows-v141 installed in current directory]
    ```bat
        vcpkgbin.bat list local x64-windows-v141
    ```
    - example 10: (for listing information of bzip2 of x64-windows-v141 installed in current directory)
    ```bat
        vcpkgbin.bat list local x64-windows-v141 bzip2
    ```
6. `remove package present in remote`
    - example 11: [for removing repository  vcpkg/0.0.81-6@had/vcpkg from remote]
    ```bat
        vcpkgbin.bat remove remote vcpkg/0.0.81-6@had/vcpkg
    ```
    - example 12: [for removing zlib:x64-windows-v141 from the remote repository vcpkg/0.0.81-6@had/vcpkg]
    ```bat
        vcpkgbin.bat remove remote vcpkg/0.0.81-6@had/vcpkg zlib x64-windows-v141
    ```
7. `remove package present in local`
    - example 13: [call vcpkg to remove all the package installed in its local vcpkg directory]
    ```bat
        vcpkgbin.bat remove local
    ```
    - example 14: [call vcpkg to remove zlib:x64-windows-v141 from its local vcpkg directory]
    ```bat
        vcpkgbin.bat remove local zlib x64-windows-v141
    ```
