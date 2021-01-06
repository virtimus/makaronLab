#pragma once
#define GLFW_INCLUDE_NONE
#include "GLFW/glfw3.h"
//''#include "flextgl/flextGL.h"
#ifndef CHIPSCPC_IMPL
#define COMMON_IMPL
#define SOKOL_NO_ENTRY
#define SOKOL_GFX_IMPL
#define SOKOL_GLCORE33
//SOKOL_GLCORE33, SOKOL_GLES2, SOKOL_GLES3, SOKOL_D3D11, SOKOL_METAL, SOKOL_WGPU or
//#define SOKOL_DUMMY_BACKEND
#define SOKOL_APP_IMPL
#define SOKOL_ARGS_IMPL
#define SOKOL_TIME_IMPL
#define SOKOL_AUDIO_IMPL
#define SOKOL_GLUE_IMPL
#endif

#include "extools/sokol/sokol_app.h"
#include "extools/sokol/sokol_audio.h"
#include "extools/sokol/sokol_args.h"
#include "extools/sokol/sokol_time.h"
#include "clock.h"
#include "fs.h"
#include "gfx.h"
#include "keybuf.h"
#include <ctype.h> /* isupper, islower, toupper, tolower */
