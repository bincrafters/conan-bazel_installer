from conans import ConanFile, tools
from conans.errors import ConanException
from conans.errors import ConanInvalidConfiguration
import os 
import platform


class BazelInstallerConan(ConanFile):
    name = "bazel_installer"
    version = "0.27.1"
    description = "The Bazel Build system from Google"
    website = "https://github.com/bazelbuild/bazel"
    url = "https://github.com/bincrafters/conan-bazel_installer"
    license = "Apache-2.0"
    topics = ("conan", "bazel", "build", "bzl")
    homepage = "https://www.bazel.build/"
    settings = "os", "arch"
    short_paths = True

    def config_options(self):
        # Checking against self.settings.* would prevent cross-building profiles from working
        if tools.detected_architecture() not in ["x86", "x86_64"]:
            raise ConanInvalidConfiguration("Unsupported Architecture.  This package currently only supports x86 and x86_64.")
        if platform.system() not in ["Windows", "Darwin", "Linux"]:
            raise ConanInvalidConfiguration("Unsupported System. This package currently only support Linux/Darwin/Windows")
    
    def system_requirements(self):
        if tools.os_info.is_linux:
            if tools.os_info.with_apt or tools.os_info.with_yum:
                installer = tools.SystemPackageTool()
                installer.install("unzip")

    def build(self):
        if self.settings.os == "Windows":
            bash = tools.which("bash.exe")
            if bash:
                self.output.info("using bash.exe from: " + bash)
            else:
                raise ConanException("No instance of bash.exe could be found on %PATH%")

        archive_name = "bazel-{0}-dist.zip".format(self.version)
        url = "{0}/releases/download/{1}/{2}".format(self.website, self.version, archive_name)
        tools.get(url, sha256="8051d77da4ec338acd91770f853e4c25f4407115ed86fd35a6de25921673e779")

        if self.settings.os == "Windows":
            bash = tools.which("bash.exe")
            with tools.environment_append({'BAZEL_SH': bash}):
                self.run('"{bash}" -l -c "pacman -S coreutils git curl zip unzip --needed --noconfirm"'.format(bash=bash))
                self.run('"{bash}" -c "./compile.sh"'.format(bash=bash))
        else:
            # fix executable permissions
            for root, _, files in os.walk('.'):
                for filename in files:
                    if filename.endswith('.sh') or filename.endswith('.tpl'):
                        filepath = os.path.join(root, filename)
                        os.chmod(filepath, os.stat(filepath).st_mode | 0o111)

            self.run('./compile.sh')
               
    def package(self):
        if self.settings.os == "Windows":
            self.copy(pattern="bazel.exe", dst="bin", src="output")
        else:
            self.copy(pattern="bazel", dst="bin", src="output")
            
    def package_info(self):
        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable with : {0}".format(bin_path))
        self.env_info.path.append(bin_path)
