cmake_minimum_required(VERSION 3.9 FATAL_ERROR)
 
project(makaronLab
  VERSION 20.12.07
  DESCRIPTION "Simulation experiments laboratory"
  LANGUAGES C CXX
)

find_package(Threads REQUIRED)
find_package(Qt5  COMPONENTS Widgets REQUIRED)

option(MLAB_BUILD_EDITOR "Build editor" ON)
option(MLAB_BUILD_C65 "Build c65 plugins" OFF)
option(BUILD_SHARED_LIBS "Build shared libs" ON)


set(EXTERNAL_TOOLS_ROOT ${PROJECT_SOURCE_DIR}/externalTools)


if (MLAB_BUILD_EDITOR)
  add_subdirectory(${EXTERNAL_TOOLS_ROOT}/spaghetti)
  add_subdirectory(libmakaron)
  add_subdirectory(editor) 
endif ()

if (MLAB_BUILD_C65)
#  add_subdirectory(C65)
endif ()

