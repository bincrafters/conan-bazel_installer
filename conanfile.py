from conans import ConanFile, tools, os
from conans.tools import os_info, SystemPackageTool, ChocolateyTool

class BazelConan(ConanFile):
    name = "Bazel"
    version = "0.6.0"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/conan-bazel"
    description = "Abseil Common Libraries (C++) from Google"
    license = "https://github.com/bazelbuild/bazel/blob/master/LICENSE"
    options = {"shared": [True, False], "with_msys2":  [True, False], "with_java": [True, False]}
    default_options = "shared=False", "with_msys2=False", "with_bazel=False", "with_java=False"
 
    def requirements(self):
        if self.options.with_msys2:
            self.requires("msys2_installer/latest@bincrafters/testing")
            
        if self.options.with_java:
            self.requires("java_installer/latest@bincrafters/testing")
       
    def source(self):
        source_url = "https://github.com/bazelbuild/bazel"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        
    def build(self):
        with tools.chdir("bazel-{0}".format(self.version)):
            if os_info.is_windows:
                self.run("./compile.sh")
            else: 
                self.run("bash ./compile.sh")
                    
    def package(self):
        self.copy("bazel.exe", dst="bin", src="output")
        self.copy("bazel", dst="bin", src="output")

    def package_info(self):
        self.env_info.path.append(self.cpp_info.bindirs)

