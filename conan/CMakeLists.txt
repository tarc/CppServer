cmake_minimum_required(VERSION 3.13)
project(cmake_wrapper)

include(${CMAKE_CURRENT_BINARY_DIR}/../conanbuildinfo.cmake)
conan_basic_setup()

if(WIN32)
    add_definitions (-D_WIN32_WINNT=_WIN32_WINNT_WIN7)
    add_definitions (-D_WINSOCK_DEPRECATED_NO_WARNINGS)
    add_definitions (-D_SILENCE_CXX17_ALLOCATOR_VOID_DEPRECATION_WARNING)
endif()

enable_testing()

add_subdirectory("source_subfolder")

conan_target_link_libraries(cppserver)

target_compile_features(cppserver PUBLIC cxx_std_17)

install(DIRECTORY source_subfolder/include/
        DESTINATION include
        FILES_MATCHING
        PATTERN "*.h"
        PATTERN "*.inl")

if(WIN32)
    set_target_properties(cppserver PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
    target_link_libraries(cppserver rpcrt4 userenv)

    if(BUILD_SHARED_LIBS)
        set_target_properties(cppserver PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
    endif()
endif()
