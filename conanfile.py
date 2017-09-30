from conans import ConanFile, tools, os


class BoostAtomicConan(ConanFile):
    name = "Abseil"
    version = "1.65.1"
    generators = "boost"
    settings = "os", "arch", "compiler", "build_type"
    short_paths = True
    url = "https://github.com/bincrafters/conan-boost-atomic"
    description = "Please visit http://www.boost.org/doc/libs/1_65_1/libs/libraries.htm"
    license = "www.boost.org/users/license.html"
    lib_short_names = ["atomic"]
    default_options = "shared=False"
    options = {"shared": [True, False]}
    build_requires = "Boost.Generator/1.65.1@bincrafters/testing" 
    requires = "Boost.Config/1.65.1@bincrafters/testing", \
        "Boost.Assert/1.65.1@bincrafters/testing", \
        "Boost.Type_Traits/1.65.1@bincrafters/testing"
 
    def source(self):
        boostorg_github = "https://github.com/boostorg"
        archive_name = "boost-" + self.version  
        for lib_short_name in self.lib_short_names:
            tools.get("{0}/{1}/archive/{2}.tar.gz"
                .format(boostorg_github, lib_short_name, archive_name))
            os.rename(lib_short_name + "-" + archive_name, lib_short_name)

    def build(self):
        self.run(self.deps_user_info['Boost.Generator'].b2_command)
        
    def package(self):
        self.copy(pattern="*", dst="lib", src="stage/lib")
        for lib_short_name in self.lib_short_names:
            include_dir = os.path.join(lib_short_name, "include")
            self.copy(pattern="*", dst="include", src=include_dir)

    def package_info(self):
        self.user_info.lib_short_names = ",".join(self.lib_short_names)
        self.cpp_info.libs = self.collect_libs()
        self.cpp_info.defines.append("BOOST_ALL_NO_LIB=1")
