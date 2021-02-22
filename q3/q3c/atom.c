 
 /*
    atom.c

    The Acorn Atom was a very simple 6502-based home computer
    (just a MOS 6502 CPU, Motorola MC6847 video
    display generator, and Intel i8255 I/O chip).

    Note: Ctrl+L (clear screen) is mapped to F1.

    NOT EMULATED:
        - REPT key (and some other special keys)
*/

#include "api.h"

#define CHIPS_IMPL

//#include "extools/chips/chips/clk.h"
//#include "extools/chips/chips/kbd.h"
//#include "extools/chips/chips/mem.h"
#include "extools/chips/systems/atom.h"
#include "extools/chips-test/examples/roms/atom-roms.h"
//#define AY38910_DATA(p) ((uint8_t)(p>>16))
/* imports from cpc-ui.cc */
#ifdef CHIPS_USE_UI
#include "extools/chips-test/examples/common/ui.h"
void atomui_init(atom_t* atom);
void atomui_discard(void);
void atomui_draw(void);
void atomui_exec(uint32_t frame_time_us);
static const int ui_extra_height = 16;
#else
static const int ui_extra_height = 0;
#endif

static atom_t atom;

/* sokol-app entry, configure application callbacks and window */
void app_init(void);
void app_frame(void);
void app_input(const sapp_event*);
void app_cleanup(void);

/*sapp_desc sokol_main(int argc, char* argv[]) {
    sargs_setup(&(sargs_desc){ .argc=argc, .argv=argv });
    return (sapp_desc) {
        .init_cb = app_init,
        .frame_cb = app_frame,
        .event_cb = app_input,
        .cleanup_cb = app_cleanup,
        .width = 2 * atom_std_display_width(),
        .height = 2 * atom_std_display_height() + ui_extra_height,
        .window_title = "Acorn Atom",
        .ios_keyboard_resizes_canvas = true
    };
}*/



