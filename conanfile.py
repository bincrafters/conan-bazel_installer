from conans import ConanFile, tools, os
from conans.tools import os_info

class BazelConan(ConanFile):
    name = "Bazel"
    version = "0.6.0"
    url = "https://github.com/bincrafters/conan-bazel"
    description = "Abseil Common Libraries (C++) from Google"
    license = "https://github.com/bazelbuild/bazel/blob/master/LICENSE"
    no_copy_source = True
    settings = "os"
    options = {"without_jdk": [True, False]}
    default_options = "without_jdk=True"
    
    def source(self):
        base_url = "https://github.com/bazelbuild/bazel/releases/download/{0}".format(self.version)
        name_and_version = "bazel-{0}".format(self.version)
        
        if os_info.is_windows:
            os_segment = "windows"
            ext = "exe"
            final_bin_filename = "bazel.exe"
        if os_info.is_linux:
            os_segment = "installer-linux"
            ext = "sh"
            final_bin_filename = "bazel"
        if os_info.is_macos:
            os_segment = "installer-darwin"
            ext = "sh"
            final_bin_filename = "bazel"
        if self.options.without_jdk:
            jdk_choice="without-jdk"
        
        jdk_and_os = "{0}-{1}".format(jdk_choice, os_segment) if self.options.without_jdk else os_segment
        
        bin_filename = "{0}-{1}-x86_64.{2}".format(name_and_version, jdk_and_os, ext)
        sha_filename = bin_filename + ".sha256"
        
        bin_url = "{0}/{1}".format(base_url, bin_filename)
        sha_url = "{0}/{1}".format(base_url, sha_filename)
        
        self.output.info("Downloading : {0}".format(sha_url))
        tools.download(sha_url, sha_filename)
        
        self.output.info("Downloading : {0}".format(bin_url))
        tools.download(bin_url, final_bin_filename)
        
        sha_checksum = tools.load(sha_filename).split(" ")[0]
        tools.check_sha256(final_bin_filename, sha_checksum)
                
    def package(self):
        self.copy(pattern="bazel*", dst="bin", src=".")
        
    def package_info(self):
        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable with : {0}".format(bin_path))
        self.env_info.path.append(bin_path)

