[![Download](https://api.bintray.com/packages/nunojpg/conan-repo/libwebp%3Anunojpg/images/download.svg)](https://bintray.com/nunojpg/conan-repo/libwebp%3Anunojpg/_latestVersion)
[![Build Status](https://travis-ci.org/nunojpg/conan-libwebp.svg?branch=master)](https://travis-ci.org/nunojpg/conan-libwebp)
[![Build status](https://ci.appveyor.com/api/projects/status/id8h0aq9myiqjt7o/branch/master?svg=true)](https://ci.appveyor.com/project/nunojpg/conan-libwebp/branch/master)

# conan-libwebp

## Reuse the packages

### Basic setup

    $ conan install libwebp/0.6.0@zamazan4ik/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    libwebp/0.6.0@zamazan4ik/stable

    [options]
    #libwebp:shared=true # default is false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install .

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
