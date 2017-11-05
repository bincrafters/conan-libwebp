from conans import ConanFile, CMake
import os

channel = os.getenv('CONAN_CHANNEL', 'stable')
username = os.getenv('CONAN_USERNAME', 'zamazan4ik')

class RestbedTestConan(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    requires = 'libwebp/0.6.0@%s/%s' % (username, channel)
    generators = 'cmake'

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self.conanfile_directory, build_dir='./')
        cmake.build()

    def imports(self):
        self.copy('*.dll', 'bin', 'bin')
        self.copy('*.dylib', 'bin', 'lib')

    def test(self):
        os.chdir('bin')
        self.run('.%sexample' % os.sep)
