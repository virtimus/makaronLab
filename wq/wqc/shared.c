
#define CHIPS_IMPL
#define CHIPS_ASSERT 
//#include <assert.h>
#include "common/common.h"
#define CHIPS_IMPL
#include "extools/chips/chips/z80.h"
#define CHIPS_IMPL
#include "extools/chips/chips/ay38910.h"
//#define AY38910_DATA(p) ((uint8_t)(p>>16))
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
//atom,wqc
#include "extools/chips/chips/m6502.h"
#include "extools/chips/chips/mc6847.h"
//#include "extools/chips/chips/i8255.h"
#include "extools/chips/chips/m6522.h"
#include "extools/chips/chips/beeper.h"


//c64
#include "extools/chips/chips/m6526.h"
#include "extools/chips/chips/m6569.h"
#include "extools/chips/chips/m6581.h"
#include "extools/chips/systems/c1541.h"
#include "extools/chips/systems/c1530.h"
#include "extools/chips/systems/c64.h"

//#include "extools/chips/systems/cpc.h"
//#ifndef CHIPSCPC_IMPL 
//#include "roms/cpc_roms.h"
void triggerWindowClose(unsigned int wid){
    sapp_request_quit();
    while (_sapp.x11.colormap>0 || _sapp.x11.window>0){
        sleep(1);
        printf("[triggerWindowClose] Waiting for close %d %d...\n",_sapp.x11.colormap,_sapp.x11.window);
    }
}

void triggerWidResize(unsigned int wid,unsigned int w,unsigned int h){
    //windowDidResize(NULL);
    //_sapp_x11_app_event(SAPP_EVENTTYPE_RESIZED);
    //XSendEvent(SAPP_EVENTTYPE_RESIZED);

   /* XEvent event;
    memset(&event, 0, sizeof(event));

    event.type = ClientMessage;
    event.xclient.window = _sapp.x11.window;
    event.xclient.format = 32;
    event.xclient.message_type = ConfigureNotify;
    event.xclient.data.l[0] = 0;
    event.xclient.data.l[1] = 0;
    event.xclient.data.l[2] = 0;
    event.xclient.data.l[3] = 0;
    event.xclient.data.l[4] = 0;
    event.xconfigure.width=400;
    event.xconfigure.height=400;


    XSendEvent(_sapp.x11.display, _sapp.x11.root,
               False,
               SubstructureNotifyMask | SubstructureRedirectMask,
               &event);*/

    XWindowChanges wc;//CWX|CWY|
    wc.x=0;
    wc.y=0;
    wc.width = w;
    wc.height = h;
    wc.border_width = 1;
    XConfigureWindow(_sapp.x11.display, _sapp.x11.window, CWWidth|CWHeight|CWBorderWidth, &wc);
    XSync(_sapp.x11.display, False);

}


