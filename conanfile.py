#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools


class libwebpConan(ConanFile):
    name = "libwebp"
    version = "0.6.0"
    license = "AGPL"
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
        cmake.configure()
        cmake.build()

    def package(self):
        src_dir = os.path.join("sources", "src")
        self.copy("FindWEBP.cmake", ".", ".")
        self.copy("webp/types.h", dst="include", src=src_dir)
        self.copy("webp/decode.h", dst="include", src=src_dir)
        self.copy("webp/encode.h", dst="include", src=src_dir)
        self.copy("libwebp*.a", dst="lib", src="lib")
        self.copy("webp*.lib", dst="lib", src="lib")
        self.copy("webp*.lib", dst="lib", src="Release")
        self.copy("libwebp*.so*", dst="lib")
        self.copy("libwebp*dylib", dst="lib")
        self.copy("*.dll", dst="bin")

    def package_info(self):
        self.cpp_info.libs = ["webp"]
