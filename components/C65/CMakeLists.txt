cmake_minimum_required(VERSION 3.9 FATAL_ERROR)

project(C65C02Plugin VERSION 20.11.17 LANGUAGES C CXX)

find_package(Qt5 COMPONENTS Widgets REQUIRED)

set(C65C02_SOURCES
  C65.cc
  C65C02.cc  
  C65C22.cc  
  C74LS189.cc  
  CRAM.cc  
  CAT28C256.cc  
  CRPTR.cc  
  CRPTRNode.cc  
  CDTButton.cc
  CDTButtonNode.cc
  CRIED.cc
  C74LS163A.cc
  ByteToBools.cc
  BoolsToByte.cc
  CCLROM.cc
  Byte27SD.cc
  Byte27SDNode.cc
  Word64ToBytes.cc
  ConstWord64.cc
  ConstWord64Node.cc
  BytesToWord64.cc
  InfoWord64.cc
  InfoByte.cc
  InfoWord64Node.cc
  InfoByteNode.cc
  ConstByte.cc
  ConstByteNode.cc
#  cpu/fake6502.c
	IntVar.cc
	
  W64.cc
  W64RAM.cc	
  )
 
 

add_library(C65C02 MODULE ${C65C02_SOURCES})
target_include_directories(C65C02 PRIVATE ${PROJECT_ROOT})
target_include_directories(C65C02 SYSTEM PRIVATE
	$<BUILD_INTERFACE:/usr/include/SDL>
	$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>/include
	)
target_compile_definitions(C65C02
  PUBLIC SPAGHETTI_SHARED
  PRIVATE SPAGHETTI_EXPORTS ${SPAGHETTI_DEFINITIONS}
  PRIVATE $<$<CONFIG:Debug>:${SPAGHETTI_DEFINITIONS_DEBUG}>
  PRIVATE $<$<CONFIG:Release>:${SPAGHETTI_DEFINITIONS_RELEASE}>
  )
target_compile_options(C65C02
  PRIVATE ${SPAGHETTI_FLAGS}
  PRIVATE ${SPAGHETTI_FLAGS_C}
  PRIVATE ${SPAGHETTI_FLAGS_CXX}
  PRIVATE ${SPAGHETTI_FLAGS_LINKER}
  PRIVATE $<$<CONFIG:Debug>:${SPAGHETTI_FLAGS_DEBUG}>
  PRIVATE $<$<CONFIG:Debug>:${SPAGHETTI_WARNINGS}>
  PRIVATE $<$<CONFIG:Release>:${SPAGHETTI_FLAGS_RELEASE}>
  )
set_target_properties(C65C02 PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/plugins")
set_target_properties(C65C02 PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/plugins")

target_link_libraries(C65C02 Spaghetti)

SET(OBJS
#  ${VENDOR_ROOT}/x16-emulator/cpu/fake6502.o
#  ${VENDOR_ROOT}/x16-emulator/memory.o
)

target_link_libraries(C65C02 ${OBJS})

SET_SOURCE_FILES_PROPERTIES(
  ${OBJS}
  PROPERTIES
  EXTERNAL_OBJECT true
  GENERATED true
)

install(TARGETS C65C02
  COMPONENT C65C02Plugin
  EXPORT C65C02
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/spaghetti
  )

set(VENDOR_X16_HEADERS
  debugger.h
  	glue.h
  memory.h
  cpu/support.h 
  cpu/modes.h
  cpu/instructions.h
  cpu/65c02.h 
  cpu/tables.h
  cpu/fake6502.h	 
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
 
