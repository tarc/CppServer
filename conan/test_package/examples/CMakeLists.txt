project(examples)

file(GLOB EXAMPLE_HEADER_FILES "examples/*.h")
file(GLOB EXAMPLE_INLINE_FILES "examples/*.inl")
file(GLOB EXAMPLE_SOURCE_FILES RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}/examples" "examples/*.cpp")
foreach(EXAMPLE_SOURCE_FILE ${EXAMPLE_SOURCE_FILES})
    string(REGEX REPLACE "(.*)\\.cpp" "\\1" EXAMPLE_NAME ${EXAMPLE_SOURCE_FILE})
    set(EXAMPLE_TARGET "cppcommon-example-${EXAMPLE_NAME}")
    add_executable(${EXAMPLE_TARGET} ${EXAMPLE_HEADER_FILES} ${EXAMPLE_INLINE_FILES} "examples/${EXAMPLE_SOURCE_FILE}")
    add_dependencies(${EXAMPLE_TARGET} ${PLUGINS})
    set_target_properties(${EXAMPLE_TARGET} PROPERTIES COMPILE_FLAGS "${PEDANTIC_COMPILE_FLAGS}" FOLDER "examples")
    target_link_libraries(${EXAMPLE_TARGET} ${LINKLIBS})
    list(APPEND INSTALL_TARGETS ${EXAMPLE_TARGET})
    list(APPEND INSTALL_TARGETS_PDB ${EXAMPLE_TARGET})

    conan_target_link_libraries(${EXAMPLE_TARGET})
    target_compile_features(cppcommon PUBLIC cxx_std_17)

endforeach()
