import os
import platform

from conans import ConanFile, CMake, tools

class libwebpConan(ConanFile):
    name = 'libwebp'
    version = '0.6.0'
    license = 'AGPL'
    description = 'library to encode and decode images in WebP format'
    url = 'http://github.com/ZaMaZaN4iK/conan-libwebp'
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {
        'shared': [True, False]
    }
    default_options = 'shared=False'
    generators = 'cmake'

    def source(self):
        base_url = "https://github.com/webmproject/libwebp/archive"
        zip_name = "v%s.zip" % self.version
        tools.download("%s/%s" % (base_url, zip_name), zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)
        tools.replace_in_file('libwebp-0.6.0/CMakeLists.txt', 'project(libwebp C)', '''project(libwebp C)
            include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
            conan_basic_setup()''')

    def configure(self):
        del self.settings.compiler.libcxx

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir='libwebp-0.6.0', build_dir='./')
        cmake.build()

    def package(self):
        self.copy("FindWEBP.cmake", ".", ".")
        self.copy('webp/types.h', dst='include', src='libwebp-0.6.0/src')
        self.copy('webp/decode.h', dst='include', src='libwebp-0.6.0/src')
        self.copy('webp/encode.h', dst='include', src='libwebp-0.6.0/src')
        self.copy('libwebp*.a', dst='lib', src='lib')
        self.copy('webp*.lib', dst='lib', src='lib')
        self.copy('libwebp*.so*', dst='lib')
        self.copy('libwebp*dylib', dst='lib')
        self.copy('*.dll', dst='bin')

    def package_info(self):
        self.cpp_info.libs = ['webp']
