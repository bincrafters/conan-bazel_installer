## This repository holds a conan recipe for Abseil.

[Conan.io](https://conan.io) package for [Abseil](https://github.com/abseil/abseil-cpp) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/bincrafters/public-conan/Abseil%3Abincrafters).

## For Users: Use this package

## Conan "latest" version convention

Abseil has a unique versioning philosophy, so this package offers a unique versioning option on the packages by using a "conan alias" named "latest". 

["Conan Alias feature Explained"](http://conanio.readthedocs.io/en/latest/reference/commands/alias.html?highlight=conan%20alias)

In summary, if users want to follow the Abseil philosophy of "Live At Head" as closely as possible while getting the benefits of using Conan, they can reference the version of "latest" in their requirements as shown in the example below.  "latest" is just an alias which redirects to an actual version of an Abseil package. Bincrafters will compile, create and upload binaries for the package on some recurring basis, and "latest" will regularly be updated to point to the most recent one.  Of note, because Abseil does not use semantic versioning, a datestamp will be used as the version number on the actual Bincrafters packages and the `source()` method of each version of the recipe will point to the most recent commit of Abseil available at the time that package version was created.  Currently, there is only a "master" branch for Abseil. 

The result of using "latest" is that whenever Bincrafters uploads a new version of the recipe and updates the alias, your next call to "conan install" will download (or build if necessary), and the immediately begin using the latest version of Abseil. 

If users want to use Abseil, perhaps staying up to date but with slightly more control over when the updates happen, they can choose to point to the concrete packages. Pointing to concrete packages by date has many other uses, such as going back to a specific point in time for troubleshooting. 

### Basic setup

    $ conan install Abseil/latest@bincrafters/testing

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    Abseil/latest@bincrafters/testing

    [generators]
    txt

Complete the installation of requirements for your project running:</small></span>

    $ mkdir build && cd build && conan install ..
	
Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they shoudl not be added to the root of the project, nor committed to git. 

## For Packagers: Publish this Package

The example below shows the commands used to publish to bincrafters conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly. 

## Build  

This is a header only library, so nothing needs to be built.

## Package 

    $ conan create bincrafters/testing
	
## Add Remote

	$ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"

## Upload

To upload a package with an alias involved, it's a three-step process. 

The first step is standard, upload the concrete package you've recently built:

    $ conan upload Abseil/09292017@bincrafters/testing --all -r bincrafters

The second step is to update the "alias package": 

	$ conan alias Abseil/latest@bincrafters/testing Abseil/09292017@bincrafters/testing

The third step is to upload the alias package:

	$conan upload Abseil/latest@bincrafters/testing -r bincrafters
	
	
### License
[Apache License 2.0](LICENSE)
