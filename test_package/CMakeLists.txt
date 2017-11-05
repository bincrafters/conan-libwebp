project(PackageTest C)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(Threads REQUIRED)


add_executable(example example.c)
target_link_libraries(example ${CONAN_LIBS} ${CMAKE_THREAD_LIBS_INIT} -lm)
