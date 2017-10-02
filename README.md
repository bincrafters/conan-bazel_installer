## This repository holds a conan recipe for Bazel.

[Conan.io](https://conan.io) package for [Bazel](https://github.com/bazelbuild/bazel) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/bincrafters/public-conan/bazel_installer%3Abincrafters).

## For Users: Use this package

### Basic setup

    $ conan install bazel_installer/0.6.0@bincrafters/testing
	
### Custom Package Options

This package has the following custom package options: 

|Package        |Option Name		| Default Value   | Possible Value    
|----------------|--------------------|-------------------|------------------
|All				|with_jdk	        | False                | True/False         

`with_jdk` - If set to `True`, the package will download the Bazel binary containing an embedded JDK.  While more convenient if you do not have Java installed, this adds approximately 60-70 MB to it's size which is inefficient if you already have Java installed.  The current default is `False` which means you must have an appropriate version of the JDK pre-installed for Bazel to work.  Conan options can be set in multiple places such as *conanfile.txt* and *conanfile.py*, or passed at the CLI when running `conan install ..`, for example:  

    $ conan install bazel_installer/0.6.0@bincrafters/testing -o bazel_installer:with_jdk=True

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

    $ conan create bincrafters/stable
	
## Add Remote

	$ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"

## Upload

    $ conan upload bazel_installer/0.6.0@bincrafters/testing --all -r bincrafters
