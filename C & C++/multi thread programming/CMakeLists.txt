cmake_minimum_required(VERSION 3.26)
project(ex3)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(ex3
        "Sample Client/SampleClient.cpp"
        MapReduceClient.cpp
        "Sample Client/MapReduceClient.h"
        MapReduceFramework.cpp
        "Sample Client/MapReduceFramework.h"
        Barrier/barrierdemo.cpp
        SampleClient.cpp
        SampleClient.cpp)
