## This repository holds a conan recipe for the Bazel Build system from Google.

[![Appveyor Status](https://ci.appveyor.com/api/projects/status/e860aeoe6bij7ccy/branch/testing%2F0.6.0?svg=true)](https://ci.appveyor.com/project/BinCrafters/conan-bazel-installer/testing%2F0.6.0)
[![Travis Status](https://travis-ci.org/bincrafters/conan-bazel_installer.svg?branch=testing%2F0.6.0)](https://travis-ci.org/bincrafters/conan-bazel_installer)

[Conan.io](https://conan.io) package for [Bazel](https://github.com/bazelbuild/bazel) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/bincrafters/public-conan/bazel_installer%3Abincrafters).

Bazel is an open-source build system released by Google which is written in Java, and effectively required to build all of their open-source C++ libraries.  While many C++ developers may want to utilize Google's C++ libraries, Bazel presents some challenges.  For example, most C++ developers outside of Google have never used Bazel.  Also, many C++ developers may not have a suitable Java version installed.  Thus, the overall proposition of Bazel is regarded as unreasonable by some, and in many cases passed over by those who were initially interested.  The "overall proposition of bazel" being the requirement of installing Java which is disagreeable to some, in order to install Bazel which they'll have to learn from scratch just to utilize a few Google projects. 

This Conan.io package aims to make it trivial for C++ developers to incorporate Googles C++ libraries in their projects, by removing the need for the developer to deal with anything related to Bazel. 

This package contains pre-built binaries of Bazel for Windows, Mac, and Linux, and includes an option to include an embedded JDK if the local machine does have a suitable version already.  It intended to serve as a building block for future packages which will contain Google's open-source C++ libraries.  These future Conan packages will reference this package as a `build_requirement`. This means that whenever one of these other Google libraries needs to be compiled, Bazel will be automatically downloaded and used to perform the build. This download will only occur once for the machine however, as Bazel will be cached in the local Conan cache for reuse. 

## For Users: Use this package

Because this package is intended to be used as a `build_requirement` in other package recipes, most users won't need to install this package directly.  However, most users should be aware of how to pass the the custom package option of `with_jdk` to Conan as described below. 

### Basic setup

    $ conan install bazel_installer/0.6.0@bincrafters/testing
	
### Custom Package Options

This package has the following custom package options: 

|Option Name	| Default Value   | Possible Value    
|-----------------|------------------|------------------
|with_jdk	        | False               | True/False         

`with_jdk` - The current default of true means that the package will download the Bazel binary which contains an embedded JDK. This can add significant convenience in many cases.  However, this adds approximately 60-70 MB to the size of the download, which is inefficient if you already have Java installed.  If this option is set to `False` Bazel must be able to find an appropriate version of the JDK pre-installed for Bazel to work, most likely via `JAVA_HOME` environment variable.  Conan options can be set in multiple places such as *conanfile.txt* and *conanfile.py*, or passed at the CLI when running `conan install ..` for example:  

    $ conan install bazel_installer/0.6.0@bincrafters/testing -o bazel_installer:with_jdk=False
	
Or, alternatively if running commands for a Google C++ library such as Abseil which references the `bazel_installer` package as a dependency, you can still pass the option for the `bazel_installer` the same way: 
	
    $ conan install Abseil/latest@bincrafters/testing -o bazel_installer:with_jdk=False

The complete list of Bazel binaries can be found here:  https://github.com/bazelbuild/bazel/releases

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    bazel_installer/0.6.0@bincrafters/testing

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..
	
Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git. 

## For Packagers: Publish this Package

The example below shows the commands used to publish to bincrafters conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly. 

## Build and package 

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from `build_requires` and `requires` , and then running the `build()` method. 

    $ conan create bincrafters/testing
	
## Add Remote

	$ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"

## Upload

    $ conan upload bazel_installer/0.6.0@bincrafters/testing --all -r bincrafters
