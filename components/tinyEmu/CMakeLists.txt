cmake_minimum_required(VERSION 3.9 FATAL_ERROR)

project(tinyEmuPlugin VERSION 20.11.17 LANGUAGES C CXX)

find_package(Qt5 COMPONENTS Widgets REQUIRED)

set(TINYEMU_ROOT ${PROJECT_SOURCE_DIR}/../../../../tinyEMU)

set(CONFIG_VERSION 00)

list(APPEND SPAGHETTI_FLAGS_CXX -DCONFIG_VERSION="00" -DMAX_XLEN=64 -DCONFIG_RISCV_MAX_XLEN=64 -DCONFIG_SLIRP=y -DCONFIG_FS_NET=y)
list(APPEND SPAGHETTI_FLAGS_CXX -O2 -Wall -g -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -MMD -D_GNU_SOURCE)
#list(APPEND SPAGHETTI_FLAGS_LINKER -L"/usr/lib/x86_64-linux-gnu" -lcurl -lcrypto)
#


set(tinyEmu_SOURCES
#  ../../../../tinyEMU/temu.c
  ${TINYEMU_ROOT}/temu.c
  ${TINYEMU_ROOT}/machine.c
  ${TINYEMU_ROOT}/riscv_machine.c
  ${TINYEMU_ROOT}/virtio.c
  ${TINYEMU_ROOT}/json.c
  ${TINYEMU_ROOT}/riscv_cpu32.c
  ${TINYEMU_ROOT}/riscv_cpu64.c
  ${TINYEMU_ROOT}/riscv_cpu128.c
  ${TINYEMU_ROOT}/softfp.c
  ${TINYEMU_ROOT}/cutils.c
  ${TINYEMU_ROOT}/pci.c
  ${TINYEMU_ROOT}/iomem.c
  ${TINYEMU_ROOT}/simplefb.c
  ${TINYEMU_ROOT}/fs_disk.c
  ${TINYEMU_ROOT}/fs_net.c
  ${TINYEMU_ROOT}/fs_wget.c
  ${TINYEMU_ROOT}/fs_utils.c
  ${TINYEMU_ROOT}/block_net.c
  ${TINYEMU_ROOT}/fs.c
  ${TINYEMU_ROOT}/slirp/slirp.c
  ${TINYEMU_ROOT}/slirp/tcp_timer.c
  ${TINYEMU_ROOT}/slirp/socket.c
  ${TINYEMU_ROOT}/slirp/misc.c
  ${TINYEMU_ROOT}/slirp/tcp_subr.c
  ${TINYEMU_ROOT}/slirp/tcp_input.c
  ${TINYEMU_ROOT}/slirp/tcp_output.c
  ${TINYEMU_ROOT}/slirp/mbuf.c
  ${TINYEMU_ROOT}/slirp/udp.c
  ${TINYEMU_ROOT}/slirp/ip_input.c
  ${TINYEMU_ROOT}/slirp/ip_output.c
  ${TINYEMU_ROOT}/slirp/if.c
  ${TINYEMU_ROOT}/slirp/ip_icmp.c
  ${TINYEMU_ROOT}/slirp/cksum.c
  ${TINYEMU_ROOT}/slirp/sbuf.c
  ${TINYEMU_ROOT}/slirp/bootp.c 
  tinyEmu.cc
  )
 
set(tinyEmuRisc_SOURCES 
#  ${TINYEMU_ROOT}/riscv_cpu.c
  )
#add_library(tinyEmuRisc MODULE ${tinyEmuRisc_SOURCES}) 

add_library(tinyEmu MODULE ${tinyEmu_SOURCES})
target_include_directories(tinyEmu PRIVATE ${PROJECT_ROOT})
target_include_directories(tinyEmu SYSTEM PRIVATE
	$<BUILD_INTERFACE:/usr/include/SDL>
	$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>/include
	)
target_compile_definitions(tinyEmu
  PUBLIC SPAGHETTI_SHARED
  PRIVATE SPAGHETTI_EXPORTS ${SPAGHETTI_DEFINITIONS}
  PRIVATE $<$<CONFIG:Debug>:${SPAGHETTI_DEFINITIONS_DEBUG}>
  PRIVATE $<$<CONFIG:Release>:${SPAGHETTI_DEFINITIONS_RELEASE}>
  )
target_compile_options(tinyEmu
  PRIVATE ${SPAGHETTI_FLAGS}
  PRIVATE ${SPAGHETTI_FLAGS_C}
  PRIVATE ${SPAGHETTI_FLAGS_CXX}
  PRIVATE ${SPAGHETTI_FLAGS_LINKER}
  PRIVATE $<$<CONFIG:Debug>:${SPAGHETTI_FLAGS_DEBUG}>
  PRIVATE $<$<CONFIG:Debug>:${SPAGHETTI_WARNINGS}>
  PRIVATE $<$<CONFIG:Release>:${SPAGHETTI_FLAGS_RELEASE}>
  )
set_target_properties(tinyEmu PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/plugins")
set_target_properties(tinyEmu PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/plugins")

target_link_libraries(tinyEmu Spaghetti)

set(CURL_LIBRARY "-lcurl") 
find_package(CURL REQUIRED) 
include_directories(${CURL_INCLUDE_DIR})
target_link_libraries(tinyEmu ${CURL_LIBRARIES})

SET(OBJS
#  ${VENDOR_ROOT}/x16-emulator/cpu/fake6502.o
#  ${VENDOR_ROOT}/x16-emulator/memory.o
)

target_link_libraries(tinyEmu ${OBJS})

SET_SOURCE_FILES_PROPERTIES(
  ${OBJS}
  PROPERTIES
  EXTERNAL_OBJECT true
  GENERATED true
)

install(TARGETS tinyEmu
  COMPONENT tinyEmuPlugin
  EXPORT tinyEmu
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
 
