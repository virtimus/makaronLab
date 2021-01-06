cmake_minimum_required(VERSION 3.9 FATAL_ERROR)

project(ChipsPlugin VERSION 20.12.29 LANGUAGES C CXX)

find_package(Qt5 COMPONENTS Widgets REQUIRED)

set(Chips_SOURCES
  Chips.cc
  cpc.c
  CPCPC.cc
  CPCPCNode.cc
  )
 
 

add_library(Chips MODULE ${Chips_SOURCES})
target_include_directories(Chips PRIVATE ${PROJECT_ROOT})
target_include_directories(Chips SYSTEM PRIVATE
	$<BUILD_INTERFACE:/usr/include/SDL>
	$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>/include
	)
target_compile_definitions(Chips
  PUBLIC SPAGHETTI_SHARED
  PRIVATE SPAGHETTI_EXPORTS ${SPAGHETTI_DEFINITIONS}
  PRIVATE $<$<CONFIG:Debug>:${SPAGHETTI_DEFINITIONS_DEBUG}>
  PRIVATE $<$<CONFIG:Release>:${SPAGHETTI_DEFINITIONS_RELEASE}>
  )
target_compile_options(Chips
  PRIVATE ${SPAGHETTI_FLAGS}
  PRIVATE ${SPAGHETTI_FLAGS_C}
  PRIVATE ${SPAGHETTI_FLAGS_CXX}
  PRIVATE ${SPAGHETTI_FLAGS_LINKER}
  PRIVATE $<$<CONFIG:Debug>:${SPAGHETTI_FLAGS_DEBUG}>
  PRIVATE $<$<CONFIG:Debug>:${SPAGHETTI_WARNINGS}>
  PRIVATE $<$<CONFIG:Release>:${SPAGHETTI_FLAGS_RELEASE}>
  )
set_target_properties(Chips PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/plugins")
set_target_properties(Chips PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/plugins")

target_link_libraries(Chips Makaron Spaghetti)

SET(OBJS
#  ${VENDOR_ROOT}/x16-emulator/cpu/fake6502.o
#  ${VENDOR_ROOT}/x16-emulator/memory.o
)

target_link_libraries(Chips ${OBJS})

SET_SOURCE_FILES_PROPERTIES(
  ${OBJS}
  PROPERTIES
  EXTERNAL_OBJECT true
  GENERATED true
)

install(TARGETS Chips
  COMPONENT ChipsPlugin
  EXPORT Chips
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/spaghetti
  )

 
set(VENDOR_CHIPS_HEADERS
  chips/m6502.h	 
  ) 
 
#foreach(HEADER ${VENDOR_X16_HEADERS})
#  configure_file(${VENDOR_ROOT}/x16-emulator/${HEADER} ${CMAKE_CURRENT_BINARY_DIR}/include/vendor/x16/${HEADER} COPYONLY)
#endforeach ()
#install(DIRECTORY ${VENDOR_ROOT}/x16-emulator
#  COMPONENT SDK
#  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/vendor) 
 
foreach(HEADER ${VENDOR_CHIPS_HEADERS})
  configure_file(${VENDOR_ROOT}/chips/${HEADER} ${CMAKE_CURRENT_BINARY_DIR}/include/vendor/chips/${HEADER} COPYONLY)
endforeach ()
install(DIRECTORY ${VENDOR_ROOT}/chips
  COMPONENT SDK
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/vendor)  
 
