/*
    cpc.c

    Amstrad CPC 464/6128 and KC Compact. No disc emulation.
*/
/*#include "common/common.h"
#define CHIPS_IMPL
#include "chips/z80.h"
#include "chips/ay38910.h"
#include "chips/i8255.h"
#include "chips/mc6845.h"
#include "chips/am40010.h"
#include "chips/upd765.h"
#include "chips/clk.h"
#include "chips/kbd.h"
#include "chips/mem.h"
#include "chips/fdd.h"
#include "chips/fdd_cpc.h"
#include "systems/cpc.h"
#include "cpc_roms.h"*/
//#include <GL/gl.h>
//#define CHIPSCPC_IMPL
//##define SOKOL_IMPL

#define Q3C_EXCL_AUDIO
#define Q3C_EXCL_GLFW


#include "api.h"
#define CHIPS_IMPL
#include "extools/chips/systems/cpc.h" 
#include "roms/cpc_roms.h"

/* imports from cpc-ui.cc */
#ifdef CHIPS_USE_UI
//##include "ui.h"
void cpcui_init(cpc_t* cpc);
void cpcui_discard(void);
void cpcui_draw(void);
void cpcui_exec(cpc_t* cpc, uint32_t frame_time_us);
static const int ui_extra_height = 16;
#else
static const int ui_extra_height = 0;
#endif



static cpc_t cpc;
//static cpc_t cpc;

/* sokol-app entry, configure application callbacks and window */
static void app_init(void);
static void app_frame(void);
static void app_input(const sapp_event*);
static void app_cleanup(void);

/*sapp_desc sokol_main(int argc, char* argv[]) {
    sargs_setup(&(sargs_desc){ .argc=argc, .argv=argv });
    return (sapp_desc) {
        .init_cb = app_init,
        .frame_cb = app_frame,
        .event_cb = app_input,
        .cleanup_cb = app_cleanup,
        .width = cpc_std_display_width(),
        .height = 2 * cpc_std_display_height() + ui_extra_height,
        .window_title = "CPC 6128",
        .ios_keyboard_resizes_canvas = true
    };
}*/

cpc_t* readCpcPtr(){
    return &cpc;
}

static unsigned int __wid = 0;

void setRootWid(unsigned int wid){
	__wid = wid;
} 

extern void triggerWidResize(unsigned int wid,unsigned int w,unsigned int h);

extern void triggerWindowClose(unsigned int wid);

uint64_t readCpc(){
	return cpc.cpu.pins;
	//return cpc;
}

unsigned int getRootWid(){
	return __wid;
}

//void cpcRun(){
	//cpc_run(1,__wid);
	//QFuture<void>  m_f1  = QtConcurrent::run(cpc_run,1,registry.wId());
//}

void cpc_run(int argc, unsigned int wid,const char * machineType){
    char * atom = "atom";
    printf("\ncpc_run machineType:%s:%s\n",machineType,atom);
    if (strcmp(machineType,"c64")==0){
        c64_run(argc,wid);
        return;
    } 
    if (strcmp(machineType,atom)==0){
        atom_run(argc,wid);
        return;
    }

//    return;
	sapp_desc desc = (sapp_desc) {
        .init_cb = app_init,
        .frame_cb = app_frame,
        .event_cb = app_input,
        .cleanup_cb = app_cleanup,
        .width = cpc_std_display_width(),
        .height = 2 * cpc_std_display_height() + ui_extra_height,
        .window_title = "CPC 6128",
        .ios_keyboard_resizes_canvas = true
    };

    sapp_run2(&desc, wid);
}

//sapp_width(), sapp_height() and sapp_dpi_scale()
/*
SOKOL_API_IMPL int sapp_width(void) {
	return 640;
}
 
SOKOL_API_IMPL int sapp_height(void) {
	return 480;
}

SOKOL_API_IMPL float sapp_dpi_scale(void) {
	return 1.0;
}*/
//sapp_width      ->
// sapp_height     ->
// sapp_dpi_scale  ->

/* audio-streaming callback */
static void push_audio(const float* samples, int num_samples, void* user_data) {
    (void)user_data;
#ifndef Q3C_EXCL_AUDIO
    saudio_push(samples, num_samples);
#endif
}

/* get cpc_desc_t struct based on model and joystick type */
cpc_desc_t cpc_desc(cpc_type_t type, cpc_joystick_type_t joy_type) {
    return (cpc_desc_t) {
        .type = type,
        .joystick_type = joy_type,
        .pixel_buffer = gfx_framebuffer(),
        .pixel_buffer_size = gfx_framebuffer_size(),
        .audio_cb = push_audio,
#ifndef Q3C_EXCL_AUDIO
        .audio_sample_rate = saudio_sample_rate(),
#endif
        .rom_464_os = dump_cpc464_os_bin,
        .rom_464_os_size = sizeof(dump_cpc464_os_bin),
        .rom_464_basic = dump_cpc464_basic_bin,
        .rom_464_basic_size = sizeof(dump_cpc464_basic_bin),
        .rom_6128_os = dump_cpc6128_os_bin,
        .rom_6128_os_size = sizeof(dump_cpc6128_os_bin),
        .rom_6128_basic = dump_cpc6128_basic_bin,
        .rom_6128_basic_size = sizeof(dump_cpc6128_basic_bin),
        .rom_6128_amsdos = dump_cpc6128_amsdos_bin,
        .rom_6128_amsdos_size = sizeof(dump_cpc6128_amsdos_bin),
        .rom_kcc_os = dump_kcc_os_bin,
        .rom_kcc_os_size = sizeof(dump_kcc_os_bin),
        .rom_kcc_basic = dump_kcc_bas_bin,
        .rom_kcc_basic_size = sizeof(dump_kcc_bas_bin)
    };
}

/* one-time application init */
void app_init(void) {
    gfx_init(&(gfx_desc_t){
        #ifdef CHIPS_USE_UI
        .draw_extra_cb = ui_draw,
        #endif
        .top_offset = ui_extra_height,
        .aspect_y = 2
    });
    keybuf_init(7);
    clock_init();
#ifndef Q3C_EXCL_AUDIO
    saudio_setup(&(saudio_desc){0});
#endif
    fs_init();
    bool delay_input = false;
 /*   if (sargs_exists("file")) {
        delay_input = true;
        if (!fs_load_file(sargs_value("file"))) {
            gfx_flash_error();
        }
    }*/
    cpc_type_t type = CPC_TYPE_6128;
  /*  if (sargs_exists("type")) {
        if (sargs_equals("type", "cpc464")) {
            type = CPC_TYPE_464;
        }
        else if (sargs_equals("type", "kccompact")) {
            type = CPC_TYPE_KCCOMPACT;
        }
    }*/
    cpc_joystick_type_t joy_type = CPC_JOYSTICK_NONE;
 /*   if (sargs_exists("joystick")) {
        joy_type = CPC_JOYSTICK_DIGITAL;
    }*/
    cpc_desc_t desc = cpc_desc(type, joy_type);
    cpc_init(&cpc, &desc);
    #ifdef CHIPS_USE_UI
    cpcui_init(&cpc);
    #endif

    /* keyboard input to send to emulator */
    if (!delay_input) {
     /*   if (sargs_exists("input")) {
            keybuf_put(sargs_value("input"));
        }*/
    }
}

/* per frame stuff, tick the emulator, handle input, decode and draw emulator display */
void app_frame(void) {
    const uint32_t frame_time = clock_frame_time();
    #if CHIPS_USE_UI
        cpcui_exec(&cpc, frame_time);
    #else
        cpc_exec(&cpc, frame_time);
    #endif
    gfx_draw(cpc_display_width(&cpc), cpc_display_height(&cpc));
    const uint32_t load_delay_frames = 120;
    if (fs_ptr() && ((clock_frame_count_60hz() > load_delay_frames) || fs_ext("sna"))) {
        bool load_success = false;
        if (fs_ext("txt") || fs_ext("bas")) {
            load_success = true;
            keybuf_put((const char*)fs_ptr());
        }
        else if (fs_ext("tap")) {
            load_success = cpc_insert_tape(&cpc, fs_ptr(), fs_size());
        }
        else if (fs_ext("dsk")) {
            load_success = cpc_insert_disc(&cpc, fs_ptr(), fs_size());
        }
        else if (fs_ext("sna") || fs_ext("bin")) {
            load_success = cpc_quickload(&cpc, fs_ptr(), fs_size());
        }
        if (load_success) {
            if (clock_frame_count_60hz() > (load_delay_frames + 10)) {
                gfx_flash_success();
            }
            if (sargs_exists("input")) {
                keybuf_put(sargs_value("input"));
            }
        }
        else {
            gfx_flash_error();
        }
        fs_free();
    }
    uint8_t key_code;
    if (0 != (key_code = keybuf_get(frame_time))) {
        cpc_key_down(&cpc, key_code);
        cpc_key_up(&cpc, key_code);
    }
}

/* keyboard input handling */
void app_input(const sapp_event* event) {
    #ifdef CHIPS_USE_UI
    if (ui_input(event)) {
        /* input was handled by UI */
        return;
    }
    #endif
    const bool shift = event->modifiers & SAPP_MODIFIER_SHIFT;
    switch (event->type) {
        int c;
        case SAPP_EVENTTYPE_CHAR:
            c = (int) event->char_code;
            if ((c > 0x20) && (c < 0x7F)) {
                cpc_key_down(&cpc, c);
                cpc_key_up(&cpc, c);
            }
            break;
        case SAPP_EVENTTYPE_KEY_DOWN:
        case SAPP_EVENTTYPE_KEY_UP:
            switch (event->key_code) {
                case SAPP_KEYCODE_SPACE:        c = 0x20; break;
                case SAPP_KEYCODE_LEFT:         c = 0x08; break;
                case SAPP_KEYCODE_RIGHT:        c = 0x09; break;
                case SAPP_KEYCODE_DOWN:         c = 0x0A; break;
                case SAPP_KEYCODE_UP:           c = 0x0B; break;
                case SAPP_KEYCODE_ENTER:        c = 0x0D; break;
                case SAPP_KEYCODE_LEFT_SHIFT:   c = 0x02; break;
                case SAPP_KEYCODE_BACKSPACE:    c = shift ? 0x0C : 0x01; break; // 0x0C: clear screen
                case SAPP_KEYCODE_ESCAPE:       c = shift ? 0x13 : 0x03; break; // 0x13: break
                case SAPP_KEYCODE_F1:           c = 0xF1; break;
                case SAPP_KEYCODE_F2:           c = 0xF2; break;
                case SAPP_KEYCODE_F3:           c = 0xF3; break;
                case SAPP_KEYCODE_F4:           c = 0xF4; break;
                case SAPP_KEYCODE_F5:           c = 0xF5; break;
                case SAPP_KEYCODE_F6:           c = 0xF6; break;
                case SAPP_KEYCODE_F7:           c = 0xF7; break;
                case SAPP_KEYCODE_F8:           c = 0xF8; break;
                case SAPP_KEYCODE_F9:           c = 0xF9; break;
                case SAPP_KEYCODE_F10:          c = 0xFA; break;
                case SAPP_KEYCODE_F11:          c = 0xFB; break;
                case SAPP_KEYCODE_F12:          c = 0xFC; break;
                default:                        c = 0; break;
            }
            if (c) {
                if (event->type == SAPP_EVENTTYPE_KEY_DOWN) {
                    cpc_key_down(&cpc, c);
                }
                else {
                    cpc_key_up(&cpc, c);
                }
            }
            break;
        case SAPP_EVENTTYPE_TOUCHES_BEGAN:
            sapp_show_keyboard(true);
            break;
        default:
            break;
    }
}

/* application cleanup callback */
void app_cleanup(void) {
    cpc_discard(&cpc);
    #ifdef CHIPS_USE_UI
    cpcui_discard();
    #endif
#ifndef Q3C_EXCL_AUDIO
    saudio_shutdown();
#endif
    gfx_shutdown();
    //sargs_shutdown();
}


#define CHIPS_IMPL
//#include "extools/chips/chips/m6502.h"
//#include "extools/chips/chips/mc6847.h"
//#include "extools/chips/chips/i8255.h"
//#include "extools/chips/chips/m6522.h"
//#include "extools/chips/chips/beeper.h"
//#include "extools/chips/chips/clk.h"
//#include "extools/chips/chips/kbd.h"
//#include "extools/chips/chips/mem.h"
#include "extools/chips/systems/atom.h"

#include "extools/chips-test/examples/roms/atom-roms.h"
static atom_t atom;

/* sokol-app entry, configure application callbacks and window */
static void atom_app_init(void);
static void atom_app_frame(void);
static void atom_app_input(const sapp_event*);
static void atom_app_cleanup(void);


void atom_run(int argc, unsigned int wid){

	sapp_desc desc = (sapp_desc) {
	        .init_cb = atom_app_init,
	        .frame_cb = atom_app_frame,
	        .event_cb = atom_app_input,
	        .cleanup_cb = atom_app_cleanup,
	        .width = 2 * atom_std_display_width(),
	        .height = 2 * atom_std_display_height() + ui_extra_height,
	        .window_title = "Acorn Atom",
	        .ios_keyboard_resizes_canvas = true
	    };

	sapp_run2(&desc, wid);

}

/* audio-streaming callback */
static void atom_push_audio(const float* samples, int num_samples, void* user_data) {
    (void)user_data;
#ifndef Q3C_EXCL_AUDIO
    saudio_push(samples, num_samples);
#endif
}

/* get atom_desc_t struct based on joystick type */
atom_desc_t atom_desc(atom_joystick_type_t joy_type) {
    return (atom_desc_t) {
        .joystick_type = joy_type,
        .audio_cb = push_audio,
#ifndef Q3C_EXCL_AUDIO
        .audio_sample_rate = saudio_sample_rate(),
#endif
        .pixel_buffer = gfx_framebuffer(),
        .pixel_buffer_size = gfx_framebuffer_size(),
        .rom_abasic = dump_abasic_ic20,
        .rom_abasic_size = sizeof(dump_abasic_ic20),
        .rom_afloat = dump_afloat_ic21,
        .rom_afloat_size = sizeof(dump_afloat_ic21),
        .rom_dosrom = dump_dosrom_u15,
        .rom_dosrom_size = sizeof(dump_dosrom_u15)
    };
}

/* one-time application init */
void atom_app_init(void) {
    gfx_init(&(gfx_desc_t) {
        #ifdef CHIPS_USE_UI
        .draw_extra_cb = ui_draw,
        #endif
        .top_offset = ui_extra_height
    });
    keybuf_init(10);
    clock_init();
    bool delay_input = false;
    fs_init();
    if (sargs_exists("file")) {
        delay_input = true;
        if (!fs_load_file(sargs_value("file"))) {
            gfx_flash_error();
        }
    }
#ifndef Q3C_EXCL_AUDIO
    saudio_setup(&(saudio_desc){0});
#endif
    atom_joystick_type_t joy_type = ATOM_JOYSTICKTYPE_NONE;
    if (sargs_exists("joystick")) {
        if (sargs_equals("joystick", "mmc") || sargs_equals("joystick", "yes")) {
            joy_type = ATOM_JOYSTICKTYPE_MMC;
        }
    }
    atom_desc_t desc = atom_desc(joy_type);
    atom_init(&atom, &desc);
    #ifdef CHIPS_USE_UI
    atomui_init(&atom);
    #endif
    /* keyboard input to send to emulator */
    if (!delay_input) {
        if (sargs_exists("input")) {
            keybuf_put(sargs_value("input"));
        }
    }
}

/* per frame stuff, tick the emulator, handle input, decode and draw emulator display */
void atom_app_frame() {
    const uint32_t frame_time = clock_frame_time();
    #if CHIPS_USE_UI
        atomui_exec(frame_time);
    #else
        atom_exec(&atom, frame_time);
    #endif
    gfx_draw(atom_display_width(&atom), atom_display_height(&atom));
    const uint32_t load_delay_frames = 48;
    if (fs_ptr() && clock_frame_count_60hz() > load_delay_frames) {
        bool load_success = false;
        if (fs_ext("txt") || fs_ext("bas")) {
            load_success = true;
            keybuf_put((const char*)fs_ptr());
        }
        if (fs_ext("tap")) {
            load_success = atom_insert_tape(&atom, fs_ptr(), fs_size());
        }
        if (load_success) {
            if (clock_frame_count_60hz() > (load_delay_frames + 10)) {
                gfx_flash_success();
            }
            if (sargs_exists("input")) {
                keybuf_put(sargs_value("input"));
            }
        }
        else {
            gfx_flash_error();
        }
        fs_free();
    }
    uint8_t key_code;
    if (0 != (key_code = keybuf_get(frame_time))) {
        atom_key_down(&atom, key_code);
        atom_key_up(&atom, key_code);
    }
}

/* keyboard input handling */
void atom_app_input(const sapp_event* event) {
    #ifdef CHIPS_USE_UI
    if (ui_input(event)) {
        /* input was handled by UI */
        return;
    }
    #endif
    int c = 0;
    switch (event->type) {
        case SAPP_EVENTTYPE_CHAR:
            c = (int) event->char_code;
            if ((c > 0x20) && (c < 0x7F)) {
                /* need to invert case (unshifted is upper caps, shifted is lower caps */
                if (isupper(c)) {
                    c = tolower(c);
                }
                else if (islower(c)) {
                    c = toupper(c);
                }
                atom_key_down(&atom, c);
                atom_key_up(&atom, c);
            }
            break;
        case SAPP_EVENTTYPE_KEY_UP:
        case SAPP_EVENTTYPE_KEY_DOWN:
            switch (event->key_code) {
                case SAPP_KEYCODE_SPACE:        c = 0x20; break;
                case SAPP_KEYCODE_RIGHT:        c = 0x09; break;
                case SAPP_KEYCODE_LEFT:         c = 0x08; break;
                case SAPP_KEYCODE_DOWN:         c = 0x0A; break;
                case SAPP_KEYCODE_UP:           c = 0x0B; break;
                case SAPP_KEYCODE_ENTER:        c = 0x0D; break;
                case SAPP_KEYCODE_INSERT:       c = 0x1A; break;
                case SAPP_KEYCODE_HOME:         c = 0x19; break;
                case SAPP_KEYCODE_BACKSPACE:    c = 0x01; break;
                case SAPP_KEYCODE_ESCAPE:       c = 0x1B; break;
                case SAPP_KEYCODE_F1:           c = 0x0C; break; /* mapped to Ctrl+L (clear screen) */
                default:                        c = 0;
            }
            if (c) {
                if (event->type == SAPP_EVENTTYPE_KEY_DOWN) {
                    atom_key_down(&atom, c);
                }
                else {
                    atom_key_up(&atom, c);
                }
            }
            break;
        case SAPP_EVENTTYPE_TOUCHES_BEGAN:
            sapp_show_keyboard(true);
            break;
        default:
            break;
    }
}

/* application cleanup callback */
void atom_app_cleanup(void) {
    atom_discard(&atom);
    #ifdef CHIPS_USE_UI
    atomui_discard();
    #endif
#ifndef Q3C_EXCL_AUDIO
    saudio_shutdown();
#endif
    gfx_shutdown();
    sargs_shutdown();
}



/*
    c64.c
*/
//#include "common.h"
#define CHIPS_IMPL
//#include "extools/chips/chips/m6502.h"
//#include "extools/chips/chips/m6526.h"
////#include "extools/chips/chips/m6569.h"
//#include "extools/chips/chips/m6581.h"
//#include "extools/chips/chips/kbd.h"
//#include "extools/chips/chips/clk.h"
//#include "extools/chips/chips/mem.h"
//#include "extools/chips/systems/c1530.h"
//#include "extools/chips/chips/m6522.h"
///#include "extools/chips/systems/c1541.h"
//#include "extools/chips/systems/c64.h"
//#define AY38910_DATA(p) ((uint8_t)(p>>16)) 
#include "extools/chips-test/examples/roms/c64-roms.h"
#include "extools/chips-test/examples/roms/c1541-roms.h"

/* imports from cpc-ui.cc */
#ifdef CHIPS_USE_UI
#include "ui.h"
void c64ui_init(c64_t* c64);
void c64ui_discard(void);
void c64ui_draw(void);
void c64ui_exec(uint32_t frame_time_us);
static const int ui_extra_height = 16;
#else
//static const int ui_extra_height = 0;
#endif

c64_t c64;

/* sokol-app entry, configure application callbacks and window */
void c64_app_init(void);
void c64_app_frame(void);
void c64_app_input(const sapp_event*);
void c64_app_cleanup(void);
  
void c64_run(int argc, unsigned int wid){

    sapp_desc desc = (sapp_desc) {
        .init_cb = c64_app_init,
        .frame_cb = c64_app_frame,
        .event_cb = c64_app_input,
        .cleanup_cb = c64_app_cleanup,
        .width =  c64_std_display_width(),
        .height =  c64_std_display_height() + ui_extra_height,
        .window_title = "C64",
        .ios_keyboard_resizes_canvas = true
    };

    sapp_run2(&desc, wid);
}

/* audio-streaming callback */
static void c64_push_audio(const float* samples, int num_samples, void* user_data) {
    (void)user_data;
#ifndef Q3C_EXCL_AUDIO
    saudio_push(samples, num_samples);
#endif
}

/* get c64_desc_t struct based on joystick type */
c64_desc_t c64_desc(c64_joystick_type_t joy_type, bool c1530_enabled, bool c1541_enabled) {
    return (c64_desc_t) {
        .c1530_enabled = c1530_enabled,
        .c1541_enabled = c1541_enabled,
        .joystick_type = joy_type,
        .pixel_buffer = gfx_framebuffer(),
        .pixel_buffer_size = gfx_framebuffer_size(),
        .audio_cb = push_audio,
#ifndef Q3C_EXCL_AUDIO
        .audio_sample_rate = saudio_sample_rate(),
#endif
        .rom_char = dump_c64_char_bin,
        .rom_char_size = sizeof(dump_c64_char_bin),
        .rom_basic = dump_c64_basic_bin,
        .rom_basic_size = sizeof(dump_c64_basic_bin),
        .rom_kernal = dump_c64_kernalv3_bin,
        .rom_kernal_size = sizeof(dump_c64_kernalv3_bin),
        .c1541_rom_c000_dfff = dump_1541_c000_325302_01_bin,
        .c1541_rom_c000_dfff_size = sizeof(dump_1541_c000_325302_01_bin),
        .c1541_rom_e000_ffff = dump_1541_e000_901229_06aa_bin,
        .c1541_rom_e000_ffff_size = sizeof(dump_1541_e000_901229_06aa_bin)
    };
}

/* one-time application init */
void c64_app_init(void) {
    gfx_init(&(gfx_desc_t){
        #ifdef CHIPS_USE_UI
        .draw_extra_cb = ui_draw,
        #endif
        .top_offset = ui_extra_height
    });
    keybuf_init(5);
    clock_init();
#ifndef Q3C_EXCL_AUDIO
    saudio_setup(&(saudio_desc){0});
#endif
    fs_init();
    bool delay_input = false;
    if (sargs_exists("file")) {
        delay_input = true;
        if (!fs_load_file(sargs_value("file"))) {
            gfx_flash_error();
        }
    }
    if (sargs_exists("prg")) {
        if (!fs_load_base64("url.prg", sargs_value("prg"))) {
            gfx_flash_error();
        }
    }
    c64_joystick_type_t joy_type = C64_JOYSTICKTYPE_NONE;
    if (sargs_exists("joystick")) {
        if (sargs_equals("joystick", "digital_1")) {
            joy_type = C64_JOYSTICKTYPE_DIGITAL_1;
        }
        else if (sargs_equals("joystick", "digital_2")) {
            joy_type = C64_JOYSTICKTYPE_DIGITAL_2;
        }
        else if (sargs_equals("joystick", "digital_12")) {
            joy_type = C64_JOYSTICKTYPE_DIGITAL_12;
        }
    }
    bool c1530_enabled = sargs_exists("c1530");
    bool c1541_enabled = sargs_exists("c1541");
    c64_desc_t desc = c64_desc(joy_type, c1530_enabled, c1541_enabled);
    c64_init(&c64, &desc);
    #ifdef CHIPS_USE_UI
    c64ui_init(&c64);
    #endif
    if (!delay_input) {
        if (sargs_exists("input")) {
            keybuf_put(sargs_value("input"));
        }
    }
}

/* per frame stuff, tick the emulator, handle input, decode and draw emulator display */
void c64_app_frame(void) {
    const uint32_t frame_time = clock_frame_time();
    #ifdef CHIPS_USE_UI
        c64ui_exec(frame_time);
    #else
        c64_exec(&c64, frame_time);
    #endif
    gfx_draw(c64_display_width(&c64), c64_display_height(&c64));
    const uint32_t load_delay_frames = 180;
    if (fs_ptr() && clock_frame_count_60hz() > load_delay_frames) {
        bool load_success = false;
        if (fs_ext("txt") || fs_ext("bas")) {
            load_success = true;
            keybuf_put((const char*)fs_ptr());
        }
        else if (fs_ext("tap")) {
            load_success = c64_insert_tape(&c64, fs_ptr(), fs_size());
        }
        else if (fs_ext("bin") || fs_ext("prg") || fs_ext("")) {
            load_success = c64_quickload(&c64, fs_ptr(), fs_size());
        }
        if (load_success) {
            if (clock_frame_count_60hz() > (load_delay_frames + 10)) {
                gfx_flash_success();
            }
            if (fs_ext("tap")) {
                c64_tape_play(&c64);
            }
            if (!sargs_exists("debug")) {
                if (sargs_exists("input")) {
                    keybuf_put(sargs_value("input"));
                }
                else if (fs_ext("tap")) {
                    keybuf_put("LOAD\n");
                }
                else if (fs_ext("prg")) {
                    keybuf_put("RUN\n");
                }
            }
        }
        else {
            gfx_flash_error();
        }
        fs_free();
    }
    uint8_t key_code;
    if (0 != (key_code = keybuf_get(frame_time))) {
        /* FIXME: this is ugly */
        c64_joystick_type_t joy_type = c64.joystick_type;
        c64.joystick_type = C64_JOYSTICKTYPE_NONE;
        c64_key_down(&c64, key_code);
        c64_key_up(&c64, key_code);
        c64.joystick_type = joy_type;
    }
}

/* keyboard input handling */
void c64_app_input(const sapp_event* event) {
    #ifdef CHIPS_USE_UI
    if (ui_input(event)) {
        /* input was handled by UI */
        return;
    }
    #endif
    const bool shift = event->modifiers & SAPP_MODIFIER_SHIFT;
    switch (event->type) {
        int c;
        case SAPP_EVENTTYPE_CHAR:
            c = (int) event->char_code;
            if ((c > 0x20) && (c < 0x7F)) {
                /* need to invert case (unshifted is upper caps, shifted is lower caps */
                if (isupper(c)) {
                    c = tolower(c);
                }
                else if (islower(c)) {
                    c = toupper(c);
                }
                c64_key_down(&c64, c);
                c64_key_up(&c64, c);
            }
            break;
        case SAPP_EVENTTYPE_KEY_DOWN:
        case SAPP_EVENTTYPE_KEY_UP:
            switch (event->key_code) {
                case SAPP_KEYCODE_SPACE:        c = 0x20; break;
                case SAPP_KEYCODE_LEFT:         c = 0x08; break;
                case SAPP_KEYCODE_RIGHT:        c = 0x09; break;
                case SAPP_KEYCODE_DOWN:         c = 0x0A; break;
                case SAPP_KEYCODE_UP:           c = 0x0B; break;
                case SAPP_KEYCODE_ENTER:        c = 0x0D; break;
                case SAPP_KEYCODE_BACKSPACE:    c = shift ? 0x0C : 0x01; break;
                case SAPP_KEYCODE_ESCAPE:       c = shift ? 0x13 : 0x03; break;
                case SAPP_KEYCODE_F1:           c = 0xF1; break;
                case SAPP_KEYCODE_F2:           c = 0xF2; break;
                case SAPP_KEYCODE_F3:           c = 0xF3; break;
                case SAPP_KEYCODE_F4:           c = 0xF4; break;
                case SAPP_KEYCODE_F5:           c = 0xF5; break;
                case SAPP_KEYCODE_F6:           c = 0xF6; break;
                case SAPP_KEYCODE_F7:           c = 0xF7; break;
                case SAPP_KEYCODE_F8:           c = 0xF8; break;
                default:                        c = 0; break;
            }
            if (c) {
                if (event->type == SAPP_EVENTTYPE_KEY_DOWN) {
                    c64_key_down(&c64, c);
                }
                else {
                    c64_key_up(&c64, c);
                }
            }
            break;
        case SAPP_EVENTTYPE_TOUCHES_BEGAN:
            sapp_show_keyboard(true);
            break;
        default:
            break;
    }
}

/* application cleanup callback */
void c64_app_cleanup(void) {
    #ifdef CHIPS_USE_UI
    c64ui_discard();
    #endif
    c64_discard(&c64);
#ifndef Q3C_EXCL_AUDIO
    saudio_shutdown();
#endif
    gfx_shutdown();
}
