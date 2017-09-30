from conans import ConanFile, tools, os
from conans.tools import os_info, SystemPackageTool, ChocolateyTool

class AbseilConan(ConanFile):
    name = "Abseil"
    version = "09302017"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/conan-abseil"
    description = "Abseil Common Libraries (C++) from Google"
    license = "https://github.com/abseil/abseil-cpp/blob/master/LICENSE"
    default_options = "shared=False"
    options = {"shared": [True, False]}
 
    def system_requirements(self):
        package_name = "bazel"
        if os_info.is_windows:
            installer = SystemPackageTool(tool=ChocolateyTool())
            installer.install(" ".join(["msys2", package_name]))
        elif os_info.linux_distro == "ubuntu":
            tools.save("/etc/apt/sources.list.d/bazel.list", "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8")
            keyfile = "bazel-release.pub.gpg"
            if os.path.isfile(keyfile): 
                os.remove(keyfile)
            tools.download("https://bazel.build/bazel-release.pub.gpg", keyfile)
            self.run("apt-key add " + keyfile)
            installer = SystemPackageTool()
            installer.install(" ".join(["openjdk-8-jdk", package_name]))
        elif os_info.is_macos:
            installer = SystemPackageTool()
            installer.install(" ".join(["java8", package_name]))            
        
    def source(self):
        source_url = "https://github.com/abseil/abseil-cpp"
        self.run("git clone --depth=1 {0}.git".format(source_url))
        
    def build(self):
        with tools.chdir("./abseil-cpp"):
            if os_info.is_windows:
                if str(self.settings.arch) == "x86":
                    self.output.info("using 32bit for bazel")
                    self.run("bazel build --cpu=x86_windows_msvc absl/...:all")
                else:
                    self.output.info("using 64bit for bazel")
                    self.run("bazel build --cpu=x64_windows_msvc absl/...:all")
            else: 
                self.run("bazel build absl/...:all")
                    
    def package(self):
        self.copy("*.h", dst="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False, symlinks=True)

    def package_info(self):
        tools.collect_libs(self)

