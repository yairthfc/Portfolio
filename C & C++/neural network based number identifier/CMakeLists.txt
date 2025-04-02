cmake_minimum_required(VERSION 3.22)
project(ex4_yairthfc)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(ex4_yairthfc
        Activation.h
        Dense.h
        main.cpp
        Matrix.h
        MlpNetwork.h
        Matrix.cpp
        Activation.cpp
        Activation.cpp
        Dense.cpp
        Dense.cpp
        MlpNetwork.cpp
        MlpNetwork.cpp
        presubmit.cpp)
