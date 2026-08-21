cmake_minimum_required(VERSION 3.16)
project(ppreproc_pfb_reader VERSION 1.0.0 LANGUAGES CXX)

include(GNUInstallDirs)
include(CTest)

add_library(ppreproc_pfb INTERFACE)
target_include_directories(
  ppreproc_pfb
  INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)
target_compile_features(ppreproc_pfb INTERFACE cxx_std_17)

add_executable(read_pfb examples/read_pfb.cpp)
target_link_libraries(read_pfb PRIVATE ppreproc_pfb)

if(BUILD_TESTING)
  add_test(
    NAME read_pfb_fixture
    COMMAND read_pfb
            ${CMAKE_CURRENT_SOURCE_DIR}/../tests/fixtures/minimal.pfb)
  set_tests_properties(
    read_pfb_fixture
    PROPERTIES PASS_REGULAR_EXPRESSION "parent_scan=101")
endif()

install(TARGETS ppreproc_pfb EXPORT ppreproc_pfb_targets)
install(TARGETS read_pfb RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(
  EXPORT ppreproc_pfb_targets
  FILE ppreproc_pfb_targets.cmake
  NAMESPACE ppreproc::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/ppreproc_pfb)
