cmake_minimum_required(VERSION 3.5)
project(openrpg_engine_server)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS)

link_libraries(boost_system pthread)

set(SOURCE_FILES main.cpp server_http.hpp imageServer.cpp imageServer.hpp)
add_executable(openrpg_engine_server ${SOURCE_FILES})
