from conans import ConanFile, CMake, tools
import os


class BoostRegexTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        
    def imports(self):
        self.copy("*", dst="bin", src="lib")
        
    def test(self):
        self.run(os.path.join("bin","test_package"))