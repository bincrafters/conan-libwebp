#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, CMake, tools


class LibwebpConan(ConanFile):
    name = "libwebp"
    version = "1.0.0"
    description = "library to encode and decode images in WebP format"
    url = "http://github.com/bincrafters/conan-libwebp"
    homepage = "https://github.com/webmproject/libwebp"
    license = "BSD 3-Clause"
    exports = ["LICENSE.md"]
    exports_sources = ['CMakeLists.txt']
    generators = 'cmake'
    source_subfolder = "source_subfolder"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False],
                "with_simd": [True, False], "near_lossless": [True, False],
                "swap_16bit_csp": [True, False]}
    default_options = "shared=False", "fPIC=True", "with_simd=True", "near_lossless=True", \
                      "swap_16bit_csp=False"

    def source(self):
        source_url = "https://github.com/webmproject/libwebp"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        os.rename(extracted_dir, self.source_subfolder)
        os.rename(os.path.join(self.source_subfolder, "CMakeLists.txt"),
                  os.path.join(self.source_subfolder, "CMakeListsOriginal.txt"))
        shutil.copy("CMakeLists.txt",
                    os.path.join(self.source_subfolder, "CMakeLists.txt"))

    def configure(self):
        del self.settings.compiler.libcxx

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    @property
    def version_components(self):
        return [int(x) for x in self.version.split('.')]

    def build(self):
        # WEBP_EXTERN is not specified on Windows
        # Set it to dllexport for building (see CMakeLists.txt) and to dllimport otherwise
        if self.options.shared and self.settings.compiler == "Visual Studio":
            tools.replace_in_file(os.path.join(self.source_subfolder, 'src', 'webp', 'types.h'),
                                  '#ifndef WEBP_EXTERN',
                                  """#ifndef WEBP_EXTERN
#ifdef _MSC_VER
    #ifdef WEBP_DLL
        #define WEBP_EXTERN __declspec(dllexport)
    #else
        #define WEBP_EXTERN __declspec(dllimport)
    #endif
#endif /* _MSC_VER */
#endif

#ifndef WEBP_EXTERN""")

        # cmake misses dll (RUNTIME) copy
        tools.replace_in_file(os.path.join(self.source_subfolder, "CMakeListsOriginal.txt"),
                              "LIBRARY DESTINATION lib",
                              "RUNTIME DESTINATION bin\nLIBRARY DESTINATION lib")

        cmake = CMake(self)
        # should be an option but it doesn't work yet
        cmake.definitions["WEBP_ENABLE_SIMD"] = self.options.with_simd
        if self.version_components[0] >= 1:
            cmake.definitions["WEBP_ENABLE_NEAR_LOSSLESS"] = self.options.near_lossless
        else:
            cmake.definitions["WEBP_NEAR_LOSSLESS"] = self.options.near_lossless
        cmake.definitions['WEBP_ENABLE_SWAP_16BIT_CSP'] = self.options.swap_16bit_csp
        # avoid finding system libs
        cmake.definitions['CMAKE_DISABLE_FIND_PACKAGE_GIF'] = True
        cmake.definitions['CMAKE_DISABLE_FIND_PACKAGE_PNG'] = True
        cmake.definitions['CMAKE_DISABLE_FIND_PACKAGE_TIFF'] = True
        cmake.definitions['CMAKE_DISABLE_FIND_PACKAGE_JPEG'] = True

        cmake.configure(source_folder=self.source_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self.source_subfolder)
        self.copy("FindWEBP.cmake", dst=".", src=".")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.options.shared and self.settings.os == "Windows" and self.settings.compiler != 'Visual Studio':
            self.cpp_info.libs = [lib+'.dll' for lib in self.cpp_info.libs]
