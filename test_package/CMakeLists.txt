cmake_minimum_required(VERSION 2.8.11)
project(test_package)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(Threads REQUIRED)

add_executable(${PROJECT_NAME} test_package.c)
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS} ${CMAKE_THREAD_LIBS_INIT} -lm)
set_property(TARGET ${PROJECT_NAME} PROPERTY C_STANDARD 99)