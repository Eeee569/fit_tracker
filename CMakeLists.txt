cmake_minimum_required(VERSION 3.21)
project(fit_tracker)

set(CMAKE_CXX_STANDARD 14)

message( "$ENV{BUILD_TYPE}" )
if(DEFINED ENV{BUILD_TYPE})


    if("$ENV{BUILD_TYPE}" STREQUAL "server")

        file(GLOB db
                src/db/*.h
                src/db/*.cpp
                )
        add_executable(yourProj ${db})

        add_executable(fit_tracker src/server/server.cpp)

    else()

        message( FATAL_ERROR "unknown BUILD_TYPE value" )
    endif()

else()

    message( FATAL_ERROR "need to set BUILD_TYPE env variable" )

endif()


