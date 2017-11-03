from conans import ConanFile, tools
from conans.tools import os_info, SystemPackageTool
import os 


class BazelInstallerConan(ConanFile):
    name = "bazel_installer"
    version = "0.6.0"
    url = "https://github.com/bincrafters/conan-bazel_installer"
    description = "The Bazel Build system from Google"
    license = "https://github.com/bazelbuild/bazel/blob/master/LICENSE"
    settings = "os", "arch"
    options = {"with_jdk": [True, False]}
    default_options = "with_jdk=True"

    def config_options(self):    
        if self.settings.arch != "x86_64":
            raise Exception("Unsupported Architecture.  This package currently only supports x86_64.")
            #TODO: add compile from source for other architectures.

    def configure(self):    
        if not self.options.with_jdk and os.getenv("JAVA_HOME","") == "":
            raise Exception("JAVA_HOME variable not found. This package requires a valid JAVA_HOME variable.")
           
    def system_requirements(self):
        if os_info.linux_distro == "ubuntu":
            installer = SystemPackageTool()
            installer.install("unzip")
        
    def build_requirements(self):
        if self.options.with_jdk:
            self.build_requires("java_installer/8.0.144@bincrafters/stable")
            
    def build(self):
        name_and_version = "bazel-{0}".format(self.version)
        base_url = "https://github.com/bazelbuild/bazel/releases/download/{0}".format(self.version)
        
        bin_filename = name_and_version
           
        bin_filename += "-" 
        
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
        
        # Below we always use the without-jdk binaries because we use java_installer 
        # conan package as a build requires when user chooses with_jdk. 
        bin_filename += "without-jdk-{0}-{1}.{2}".format(os_segment, arch_segment, ext)
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
    
        if not os_info.is_windows:
            # This downloads a prebuilt installer and extracts, does not build from scratch
            self.run("chmod +x bazel.sh")
            self.run("./bazel.sh --prefix={0} --bin=%prefix%/bin --base=%prefix%/lib/bazel".format(os.getcwd()))
        
        #TODO: add compile from source for other architectures. 
        
    def package(self):
        if os_info.is_windows:
            self.copy(pattern="bazel*", dst="bin", src=".")
        else:
            self.copy(pattern="bazel*", dst="bin", src="lib/bazel/bin")
            
    def package_info(self):
        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable with : {0}".format(bin_path))
        self.env_info.path.append(bin_path)

    def package_id(self):
        self.info.options.with_jdk = "any" 