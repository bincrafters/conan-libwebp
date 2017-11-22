#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools


class libwebpConan(ConanFile):
    name = "libwebp"
    version = "0.6.0"
    license = "BSD-3"
    description = "library to encode and decode images in WebP format"
    url = "http://github.com/bincrafters/conan-libwebp"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports_sources = ['CMakeLists.txt']
    generators = 'cmake'

    def source(self):
        base_url = "https://github.com/webmproject/libwebp"
        archive_name = "v" + self.version
        archive_path = "/archive/"
        archive_extension = ".zip"
        download_url = base_url + archive_path + archive_name + archive_extension
        tools.get(download_url)
        sources_dir_name = self.name + "-" + self.version
        os.rename(sources_dir_name, "sources")

    def configure(self):
        del self.settings.compiler.libcxx

    def build(self):
        cmake = CMake(self)
        if self.options.shared and self.settings.compiler == "Visual Studio":
            tools.replace_in_file(os.path.join('sources', 'src', 'webp', 'types.h'),
                                  '#ifndef WEBP_EXTERN',
                                  """#ifndef WEBP_EXTERN
  #ifdef _MSC_VER
    #ifdef WEBP_USE_DLL
      #define WEBP_EXTERN(type) __declspec(dllimport) type
    #else /* WEBP_USE_DLL */
      #define WEBP_EXTERN(type) __declspec(dllexport) type
    #endif /* WEBP_USE_DLL */
  #endif /* _MSC_VER */
#endif
#ifndef WEBP_EXTERN""")
        cmake.configure()
        cmake.build()

    def package(self):
        src_dir = os.path.join("sources", "src")
        self.copy("FindWEBP.cmake", ".", ".")
        self.copy("webp/types.h", dst="include", src=src_dir)
        self.copy("webp/decode.h", dst="include", src=src_dir)
        self.copy("webp/encode.h", dst="include", src=src_dir)
        self.copy("libwebp*.a", dst="lib", src="lib", keep_path=False)
        self.copy("webp*.lib", dst="lib", src="lib", keep_path=False)
        self.copy("webp*.lib", dst="lib", src="Release", keep_path=False)
        self.copy("*.so*", dst="lib", src='sources', keep_path=False)
        self.copy("*.dylib", dst="lib", src='sources', keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["webp"]
        if self.options.shared and self.settings.compiler == "Visual Studio":
            self.cpp_info.defines.append('WEBP_USE_DLL')
