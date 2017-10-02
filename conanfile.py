from conans import ConanFile, tools, os 
from conans.tools import os_info


class BazelInstallerConan(ConanFile):
    name = "bazel_installer"
    version = "0.6.0"
    url = "https://github.com/bincrafters/conan-bazel_installer"
    description = "Abseil Common Libraries (C++) from Google"
    license = "https://github.com/bazelbuild/bazel/blob/master/LICENSE"
    settings = "os"
    options = {"with_jdk": [True, False]}
    default_options = "with_jdk=False"

    def source(self):
        name_and_version = "bazel-{0}".format(self.version)
        base_url = "https://github.com/bazelbuild/bazel/releases/download/{0}".format(self.version)
        
        bin_filename = name_and_version
           
        if not self.options.with_jdk:
            bin_filename += "-without-jdk-"
        
        arch_segment = "x86_64"
        
        if os_info.is_windows:
            os_segment = "windows"
            ext = "exe"
        else:
            if os_info.is_linux:
                os_segment = "installer-linux"
            if os_info.is_macos:
                os_segment = "installer-darwin"
            ext = "sh"
        
        bin_filename += "{0}-{1}.{2}".format(os_segment, arch_segment, ext)
        sha_filename = bin_filename + ".sha256"
        
        bin_url = "{0}/{1}".format(base_url, bin_filename)
        sha_url = "{0}/{1}".format(base_url, sha_filename)
        
        self.output.info("Downloading : {0}".format(sha_url))
        tools.download(sha_url, sha_filename)
        
        self.output.info("Downloading : {0}".format(bin_url))
        tools.download(bin_url, bin_filename)
        
        sha_checksum = tools.load(sha_filename).split(" ")[0]
        tools.check_sha256(bin_filename, sha_checksum)

        os.rename(bin_filename, "bazel.{0}".format(ext))
    
    def build(self):
        if not os_info.is_windows:
            self.run("chmod +x bazel.sh")
            self.run("./bazel.sh --prefix={0} --bin=%prefix%/bin --base=%prefix%/lib/bazel".format(os.getcwd()))
            
    def package(self):
        bin_dir = "." if os_info.is_windows else "bin"
        self.copy(pattern="bazel*", dst="bin", src=bin_dir, symlinks=True)
        self.copy(pattern="*", dst="lib", src="lib", symlinks=True)
        
    def package_info(self):
        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable with : {0}".format(bin_path))
        self.env_info.path.append(bin_path)
