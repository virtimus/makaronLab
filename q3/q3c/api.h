#pragma once
#ifndef CHIPS_API_H
#define CHIPS_API_H

//extern "C" {
#define AY38910_DATA(p) ((uint8_t)(p>>16))

//#ifndef CHIPSCPC_IMPL
//#define CHIPS_IMPL
//#endif
#undef CHIPS_IMPL
#define CHIPS_ASSERT
#define assert(ignore) ((void)0)
#include "extools/sokol/sokol_app.h"

#include "extools/sokol/sokol_args.h"
#include "extools/sokol/sokol_time.h"
#include "common/clock.h"
#include "common/fs.h"
#include "common/gfx.h"
#include "common/keybuf.h"
#include <ctype.h> /* isupper, islower, toupper, tolower */

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

#include "extools/chips/chips/m6502.h"
#include "extools/chips/chips/mc6847.h"
#include "extools/chips/chips/m6522.h"
#include "extools/chips/chips/beeper.h"


//c64
#include "extools/chips/chips/m6526.h"
#include "extools/chips/chips/m6569.h"
#include "extools/chips/chips/m6581.h"
#include "extools/chips/systems/c1541.h"
#include "extools/chips/systems/c1530.h"
#include "extools/chips/systems/c64.h"



//#endif
//}
//extern "C" {

//}
#endif // CHIPS_API_H
