cmake_minimum_required(VERSION 3.22)
project(OS4)

set(CMAKE_CXX_STANDARD 11)

add_executable(OS4
        PhysicalMemory.cpp
        VirtualMemory.cpp
        MemoryConstants.h
        PhysicalMemory.h
        VirtualMemory.h

        SimpleTest.cpp)
