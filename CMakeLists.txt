cmake_minimum_required(VERSION 3.0)

project(buffer)

add_library(buffer
    ${CMAKE_CURRENT_SOURCE_DIR}/src/buffer.c)

add_executable(serializer-test
    ${CMAKE_CURRENT_SOURCE_DIR}/src/main.c)

target_link_libraries(serializer-test buffer)