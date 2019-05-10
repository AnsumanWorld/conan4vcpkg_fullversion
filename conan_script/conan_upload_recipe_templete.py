from conans import ConanFile,tools
import os

class %s%s(ConanFile):
    name = "%s"
    version = "%s"
    license = "GPL-3.0"
    url = "<https://github.com/apattnaik0721013/vcpkg>"
    description = "conan for vcpkg"
    settings = "vcpkg_triplet","vcpkg_port"
    no_copy_source=True


    def package(self):
        self.copy("%s", dst="pkg", src=r"%s")