#pragma once
#ifndef CHIPS_API_H
#define CHIPS_API_H

//extern "C" {

#include "common/common.h"
#ifndef CHIPSCPC_IMPL
#define CHIPS_IMPL
#endif
#include "extools/chips/chips/z80.h"
#include "extools/chips/chips/ay38910.h"
#include "extools/chips/chips/i8255.h"
#include "extools/chips/chips/mc6845.h"
//#include "extools/chips/chips/crt.h" not found ?/deleted?
#include "extools/chips/chips/clk.h"
#include "extools/chips/chips/kbd.h"
#include "extools/chips/chips/mem.h"

#include "extools/chips/chips/am40010.h"
#include "extools/chips/chips/upd765.h"
#include "extools/chips/chips/fdd.h"
#include "extools/chips/chips/fdd_cpc.h"

#include "extools/chips/systems/cpc.h"
#ifndef CHIPSCPC_IMPL
#include "roms/cpc_roms.h"
#endif
//}
//extern "C" {

//}
#endif // CHIPS_API_H
