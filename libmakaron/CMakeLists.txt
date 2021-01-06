cmake_minimum_required(VERSION 3.9 FATAL_ERROR)

project(libMakaron VERSION 20.12.29 LANGUAGES C CXX)

find_package(Qt5 COMPONENTS Widgets REQUIRED)
find_package(Threads REQUIRED)

set(LIBMAKARON_PUBLIC_HEADERS
  include/makaron/api.h
  include/roms/cpc_roms.h
  )

set(LIBMAKARON_SOURCES
  libmakaron.cc
  )
 
 

add_library(Makaron SHARED ${LIBMAKARON_SOURCES})

target_include_directories(Makaron PRIVATE ${PROJECT_ROOT})
target_include_directories(Makaron SYSTEM PRIVATE
	$<BUILD_INTERFACE:/usr/include/SDL>
	$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>/include
	)
target_include_directories(Makaron
  PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
  PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>
  PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../externalTools/spaghetti/libspaghetti/source>
  PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../externalTools/spaghetti/libspaghetti/source>
  )

#[[target_compile_definitions(Makaron
  PUBLIC SPAGHETTI_SHARED
  PRIVATE SPAGHETTI_EXPORTS ${SPAGHETTI_DEFINITIONS}
  PRIVATE $<$<CONFIG:Debug>:${SPAGHETTI_DEFINITIONS_DEBUG}>
  PRIVATE $<$<CONFIG:Release>:${SPAGHETTI_DEFINITIONS_RELEASE}>
  )
target_compile_options(Makaron
  PRIVATE ${SPAGHETTI_FLAGS}
  PRIVATE ${SPAGHETTI_FLAGS_C}
  PRIVATE ${SPAGHETTI_FLAGS_CXX}
  PRIVATE ${SPAGHETTI_FLAGS_LINKER}
  PRIVATE $<$<CONFIG:Debug>:${SPAGHETTI_FLAGS_DEBUG}>
  PRIVATE $<$<CONFIG:Debug>:${SPAGHETTI_WARNINGS}>
  PRIVATE $<$<CONFIG:Release>:${SPAGHETTI_FLAGS_RELEASE}>
  )
set_target_properties(Makaron PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")
set_target_properties(Makaron PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")
]]
target_link_libraries(Makaron Spaghetti X11 Xcursor Xi GL m dl asound)

SET(OBJS
#  ${VENDOR_ROOT}/x16-emulator/cpu/fake6502.o
#  ${VENDOR_ROOT}/x16-emulator/memory.o
)

target_link_libraries(Makaron ${OBJS})

SET_SOURCE_FILES_PROPERTIES(
  ${OBJS}
  PROPERTIES
  EXTERNAL_OBJECT true
  GENERATED true
)

install(TARGETS Makaron
  COMPONENT libMakaron
  EXPORT Makaron
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/makaron
  )

 
set(EXTOOLS_CHIPS_HEADERS
  chips/m6502.h	
  chips/z80.h 
  chips/ay38910.h
  chips/i8255.h
  chips/mc6845.h
#  chips/crt.h
	chips/clk.h
	chips/kbd.h
	chips/mem.h
	
	chips/am40010.h
	chips/upd765.h
	chips/fdd.h
	chips/fdd_cpc.h
	
	systems/cpc.h
  ) 
 
set(EXTOOLS_SOKOL_HEADERS
  sokol_app.h	
  sokol_audio.h 
  sokol_args.h
  sokol_time.h
  sokol_gfx.h
  sokol_glue.h
  )  
 
#foreach(HEADER ${VENDOR_X16_HEADERS})
#  configure_file(${VENDOR_ROOT}/x16-emulator/${HEADER} ${CMAKE_CURRENT_BINARY_DIR}/include/vendor/x16/${HEADER} COPYONLY)
#endforeach ()
#install(DIRECTORY ${VENDOR_ROOT}/x16-emulator
#  COMPONENT SDK
#  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/vendor) 
 
foreach(HEADER ${EXTOOLS_CHIPS_HEADERS})
  configure_file(${EXTERNAL_TOOLS_ROOT}/chips/${HEADER} ${CMAKE_CURRENT_BINARY_DIR}/include/extools/chips/${HEADER} COPYONLY)
endforeach ()
install(DIRECTORY ${EXTERNAL_TOOLS_ROOT}/chips
  COMPONENT SDK
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/extools)  

foreach(HEADER ${EXTOOLS_SOKOL_HEADERS})
  configure_file(${EXTERNAL_TOOLS_ROOT}/sokol/${HEADER} ${CMAKE_CURRENT_BINARY_DIR}/include/extools/sokol/${HEADER} COPYONLY)
endforeach ()
install(DIRECTORY ${EXTERNAL_TOOLS_ROOT}/sokol
  COMPONENT SDK
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/extools)  
 
 
