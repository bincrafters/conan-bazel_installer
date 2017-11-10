#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os 


class BazelInstallerConan(ConanFile):
    name = "bazel_installer"
    version = "0.7.0"
    url = "https://github.com/bincrafters/conan-bazel_installer"
    description = "The Bazel Build system from Google"
    license = "https://github.com/bazelbuild/bazel/blob/master/LICENSE"
    settings = "os", "arch"
    options = {"with_jdk": [True, False]}
    default_options = "with_jdk=True"

    def system_requirements(self):
        if self.settings.os == "Linux":
            if tools.os_info.linux_distro == "ubuntu":
                installer = tools.SystemPackageTool()
                installer.install("unzip")

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("msys2_installer/latest@%s/%s" % (self.user, self.channel))
        
    def requirements(self):
        if self.options.with_jdk:
            self.requires("java_installer/8.0.144@%s/%s" % (self.user, self.channel))

    def build(self):
        archive_name = "bazel-{0}-dist.zip".format(self.version)
        url = "https://github.com/bazelbuild/bazel/releases/download/{0}/{1}".format(self.version, archive_name)
        tools.download(url, archive_name, verify=True)
        tools.unzip(archive_name)
        os.unlink(archive_name)
        if self.settings.os == "Windows":
            raise Exception("implement MSYS build")
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

    def package_id(self):
        self.info.options.with_jdk = "any"
