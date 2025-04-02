cmake_minimum_required(VERSION 3.22)
project(ex3b_yairthfc C)

set(CMAKE_C_STANDARD 11)

include_directories(.)

add_executable(ex3b_yairthfc
        linked_list.c
        linked_list.h
        markov_chain.h
        snakes_and_ladders.c
        markov_chain.c
        tweets_generator.c)
