#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <limits.h>
#define TRUE 1
#define FALSE 0
typedef unsigned char uint8_t;
typedef short int16_t;
#define ARRAY_CREATE(array, init_capacity, init_size) {\
    array = malloc(sizeof(*array)); \
    array->data = malloc((init_capacity) * sizeof(*array->data)); \
    assert(array->data != NULL); \
    array->capacity = init_capacity; \
    array->size = init_size; \
}
#define ARRAY_PUSH(array, item) {\
    if (array->size == array->capacity) {  \
        array->capacity *= 2;  \
        array->data = realloc(array->data, array->capacity * sizeof(*array->data)); \
        assert(array->data != NULL); \
    }  \
    array->data[array->size++] = item; \
}
#define STR_INT16_T_BUFLEN ((CHAR_BIT * sizeof(int16_t) - 1) / 3 + 2)
void str_int16_t_cat(char *str, int16_t num) {
    char numstr[STR_INT16_T_BUFLEN];
    sprintf(numstr, "%d", num);
    strcat(str, numstr);
}
enum js_var_type {JS_VAR_NULL, JS_VAR_UNDEFINED, JS_VAR_NAN, JS_VAR_BOOL, JS_VAR_INT16, JS_VAR_STRING, JS_VAR_ARRAY, JS_VAR_DICT};
struct js_var {
    enum js_var_type type;
    int16_t number;
    void *data;
};
struct js_var js_var_from(enum js_var_type type) {
    struct js_var v;
    v.type = type;
    v.data = NULL;
    return v;
}
static ARRAY(void *) gc_main;

struct array_number_t {
    int16_t size;
    int16_t capacity;
    int16_t* data;
};
struct array_pointer_t {
    int16_t size;
    int16_t capacity;
    void ** data;
};
struct array_array_array_number_t {
    int16_t size;
    int16_t capacity;
    struct array_array_number_t ** data;
};

static ARRAY(ARRAY(void *)) gc_main_arrays;
static uint8_t debug;
static int16_t A_reg;
static int16_t C_flag;
static int16_t T_flag;
static int16_t PC_stack[4];
static int16_t sp;
static struct array_number_t * R_regs;
static int16_t cmram;
static int16_t ramaddr;
static int16_t ph;
static int16_t pm;
static int16_t pl;
static int16_t cmrom;
static int16_t romport;
static struct array_pointer_t * prom;
static struct array_array_array_number_t * ramdata;
static struct array_array_array_number_t * ramstatus;
static struct array_number_t * ramout;
static struct array_pointer_t * breakpoints;
static int16_t temp;
static uint8_t testFlag;
static uint8_t animFlag;
static uint8_t runFlag;
static uint8_t stepFlag;
static void (*codes)()[256];
static int16_t cycles[256] = { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 };
static int16_t cpuCycles;
static ARRAY(void *) gc_22810;

void cpuLoop(int16_t cycleLimit);

void incPC()
{
    PC_stack[0]++;
    PC_stack[0] &= 0xfff;
    if (testFlag)
        PC_stack[0] &= 0xff;

}
int16_t nextCode()
{
    incPC();
    return js_var_from(JS_VAR_NAN) & 0xff;

}
int16_t activeCode()
{
    return js_var_from(JS_VAR_NAN) & 0xff;

}
void setRpar(int16_t rpar, int16_t pset)
{
    R_regs->data[2 * rpar + 1] = pset & 0xf;
    R_regs->data[2 * rpar] = (pset >> 4) & 0xf;

}
int16_t getRpar(int16_t rpar)
{
    return ((R_regs->data[2 * rpar] << 4) & 0xf0 | R_regs->data[2 * rpar + 1] & 0xf);

}
void ramAdrDecoder()
{
    switch (cmram) {
        case 1:
            ph = ramaddr >> 6;
            break;
        case 2:
            ph = 0x4 | ramaddr >> 6;
            break;
        case 4:
            ph = 0x8 | ramaddr >> 6;
            break;
        case 8:
            ph = 0xC | ramaddr >> 6;
            break;
    }
    if (testFlag)
        ph &= 0x1;
    pm = (ramaddr & 0x30) >> 4;
    pl = ramaddr & 0xf;

}
void opJCN(int16_t cond)
{
    int16_t invert;
    invert = 0;
    if (cond & 0x8)
        invert = 1;
    temp = PC_stack[0] & 0xf00;
    temp |= nextCode();
    incPC();
    if (cond & 0x4)
        if (/* unsupported expression (!A_reg)^invert */)
        PC_stack[0] = temp;
    if (cond & 0x2)
        if (/* unsupported expression (C_flag)^invert */)
        PC_stack[0] = temp;
    if (cond & 0x1)
        if (/* unsupported expression (T_flag)^invert */)
        PC_stack[0] = temp;

}
void opFIM(int16_t rpar)
{
    setRpar(rpar, nextCode());
    incPC();

}
void opSRC(int16_t rpar)
{
    ramaddr = getRpar(rpar);
    incPC();

}
void opFIN(int16_t rpar)
{
    setRpar(rpar, prom->data[(PC_stack[0] & 0xf00) | getRpar(0)]);
    incPC();

}
void opJIN(int16_t rpar)
{
    PC_stack[0] = (PC_stack[0] & 0xf00) | getRpar(rpar);
    if (testFlag)
        PC_stack[0] &= 0xff;

}
void opJUN(int16_t addr)
{
    PC_stack[0] = addr | nextCode();
    if (testFlag)
        PC_stack[0] &= 0xff;

}
void opJMS(int16_t addr)
{
    temp = addr | nextCode();
    if (sp < 3)
    {
        sp++;
        for (i = sp;js_var_from(JS_VAR_NAN) > 0;/* expression is not yet supported i-- */)
            PC_stack[i] = PC_stack[js_var_from(JS_VAR_NAN) - 1];
        PC_stack[0] = temp;
        if (testFlag)
            PC_stack[0] &= 0xff;
    }
    else
    {
        incPC();
        if (debug)
            /* Unsupported function call: alert('Stack overflow') */;
    }

}
void opINC(int16_t reg)
{
    R_regs->data[reg]++;
    if (R_regs->data[reg] & 0xf0)
        R_regs->data[reg] = 0;
    incPC();

}
void opISZ(int16_t reg)
{
    temp = nextCode();
    R_regs->data[reg] = (R_regs->data[reg] + 1) & 0xf;
    if (R_regs->data[reg])
        PC_stack[0] = (PC_stack[0] & 0xf00) | temp;
    else
        incPC();

}
void opADD(int16_t reg)
{
    A_reg = A_reg + R_regs->data[reg] + C_flag;
    C_flag = 0;
    if (A_reg & 0xf0)
    {
        A_reg &= 0xf;
        C_flag = 1;
    }
    incPC();

}
void opSUB(int16_t reg)
{
    A_reg = A_reg + (~R_regs->data[reg] & 0xf) + (~C_flag & 1);
    C_flag = 0;
    if (A_reg & 0xf0)
    {
        A_reg &= 0xf;
        C_flag = 1;
    }
    incPC();

}
void opLD(int16_t reg)
{
    A_reg = R_regs->data[reg];
    incPC();

}
void opXCH(int16_t reg)
{
    temp = A_reg;
    A_reg = R_regs->data[reg];
    R_regs->data[reg] = temp;
    incPC();

}
void opBBL(int16_t data)
{
    char * null = NULL;
    if (sp > 0)
    {
        for (i = 0;js_var_from(JS_VAR_NAN) < sp;/* expression is not yet supported i++ */)
        {
            null = malloc(15 + STR_INT16_T_BUFLEN + 1);
            assert(null != NULL);
            null[0] = '\0';
            strcat(null, "[object Object]");
            str_int16_t_cat(null, 1);
            PC_stack[i] = PC_stack[null];
        }
        PC_stack[sp] = 0;
        sp--;
        A_reg = data;
    }
    else
        if (debug)
        /* Unsupported function call: alert('Stack error') */;
    incPC();

}
void opLDM(int16_t data)
{
    A_reg = data;
    incPC();

}
void opWRM()
{
    ramAdrDecoder();
    ramdata->data[ph]->data[pm]->data[pl] = A_reg;
    incPC();

}
void opWMP()
{
    ramAdrDecoder();
    ramout->data[ph] = A_reg;
    if (testFlag)
        T_flag = ramout->data[0] & 0x1;
    incPC();

}
void opWRR()
{
    romport = A_reg;
    incPC();

}
void opWR(int16_t status)
{
    ramAdrDecoder();
    ramstatus->data[ph]->data[pm]->data[status] = A_reg;
    incPC();

}
void opSBM()
{
    ramAdrDecoder();
    A_reg = A_reg + ((~ramdata->data[ph]->data[pm]->data[pl]) & 0xf) + (~C_flag & 1);
    C_flag = 0;
    if (A_reg & 0xf0)
    {
        A_reg &= 0xf;
        C_flag = 1;
    }
    incPC();

}
void opRDM()
{
    ramAdrDecoder();
    A_reg = ramdata->data[ph]->data[pm]->data[pl];
    incPC();

}
void opRDR()
{
    if (testFlag)
        romport = ramout->data[1];
    A_reg = romport;
    incPC();

}
void opADM()
{
    ramAdrDecoder();
    A_reg = A_reg + ramdata->data[ph]->data[pm]->data[pl] + C_flag;
    C_flag = 0;
    if (A_reg & 0xf0)
    {
        A_reg &= 0xf;
        C_flag = 1;
    }
    incPC();

}
void opRD(int16_t status)
{
    ramAdrDecoder();
    A_reg = ramstatus->data[ph]->data[pm]->data[status];
    incPC();

}
void opCLB()
{
    A_reg = 0;
    C_flag = 0;
    incPC();

}
void opCLC()
{
    C_flag = 0;
    incPC();

}
void opIAC()
{
    A_reg++;
    C_flag = 0;
    if (A_reg & 0xf0)
    {
        A_reg &= 0xf;
        C_flag = 1;
    }
    incPC();

}
void opCMC()
{
    C_flag = (C_flag == 1) ? 0 : 1;
    incPC();

}
void opCMA()
{
    A_reg = (~A_reg) & 0xf;
    incPC();

}
void opRAL()
{
    A_reg = (A_reg << 1) | C_flag;
    C_flag = 0;
    if (A_reg & 0xf0)
    {
        A_reg &= 0xf;
        C_flag = 1;
    }
    incPC();

}
void opRAR()
{
    temp = A_reg & 1;
    A_reg = (A_reg >> 1) | (C_flag << 3);
    C_flag = temp;
    incPC();

}
void opTCC()
{
    A_reg = C_flag;
    C_flag = 0;
    incPC();

}
void opDAC()
{
    (A_reg = A_reg + 0xf);
    C_flag = 0;
    if (A_reg & 0xf0)
    {
        A_reg &= 0xf;
        C_flag = 1;
    }
    incPC();

}
void opTCS()
{
    A_reg = 9 + C_flag;
    C_flag = 0;
    incPC();

}
void opSTC()
{
    C_flag = 1;
    incPC();

}
void opDAA()
{
    if (A_reg > 9 || C_flag == 1)
        (A_reg = A_reg + 6);
    if (A_reg & 0xf0)
    {
        A_reg &= 0xf;
        C_flag = 1;
    }
    incPC();

}
void opKBP()
{
    switch (A_reg) {
        case 0:
            A_reg = 0;
            break;
        case 1:
            A_reg = 1;
            break;
        case 2:
            A_reg = 2;
            break;
        case 4:
            A_reg = 3;
            break;
        case 8:
            A_reg = 4;
            break;
        default:
            A_reg = 15;
            break;
    }
    incPC();

}
void opDCL()
{
    switch (A_reg & 0x7) {
        case 0:
            cmram = 1;
            break;
        case 1:
            cmram = 2;
            break;
        case 2:
            cmram = 4;
            break;
        case 3:
            cmram = 3;
            break;
        case 4:
            cmram = 8;
            break;
        case 5:
            cmram = 10;
            break;
        case 6:
            cmram = 12;
            break;
        case 7:
            cmram = 14;
            break;
    }
    incPC();

}
void i00()
{
    incPC();

}
void i10()
{
    opJCN(0);

}
void i11()
{
    opJCN(1);

}
void i12()
{
    opJCN(2);

}
void i13()
{
    opJCN(3);

}
void i14()
{
    opJCN(4);

}
void i15()
{
    opJCN(5);

}
void i16()
{
    opJCN(6);

}
void i17()
{
    opJCN(7);

}
void i18()
{
    opJCN(8);

}
void i19()
{
    opJCN(9);

}
void i1a()
{
    opJCN(10);

}
void i1b()
{
    opJCN(11);

}
void i1c()
{
    opJCN(12);

}
void i1d()
{
    opJCN(13);

}
void i1e()
{
    opJCN(14);

}
void i1f()
{
    opJCN(15);

}
void i20()
{
    opFIM(0);

}
void i21()
{
    opSRC(0);

}
void i22()
{
    opFIM(1);

}
void i23()
{
    opSRC(1);

}
void i24()
{
    opFIM(2);

}
void i25()
{
    opSRC(2);

}
void i26()
{
    opFIM(3);

}
void i27()
{
    opSRC(3);

}
void i28()
{
    opFIM(4);

}
void i29()
{
    opSRC(4);

}
void i2a()
{
    opFIM(5);

}
void i2b()
{
    opSRC(5);

}
void i2c()
{
    opFIM(6);

}
void i2d()
{
    opSRC(6);

}
void i2e()
{
    opFIM(7);

}
void i2f()
{
    opSRC(7);

}
void i30()
{
    opFIN(0);

}
void i31()
{
    opJIN(0);

}
void i32()
{
    opFIN(1);

}
void i33()
{
    opJIN(1);

}
void i34()
{
    opFIN(2);

}
void i35()
{
    opJIN(2);

}
void i36()
{
    opFIN(3);

}
void i37()
{
    opJIN(3);

}
void i38()
{
    opFIN(4);

}
void i39()
{
    opJIN(4);

}
void i3a()
{
    opFIN(5);

}
void i3b()
{
    opJIN(5);

}
void i3c()
{
    opFIN(6);

}
void i3d()
{
    opJIN(6);

}
void i3e()
{
    opFIN(7);

}
void i3f()
{
    opJIN(7);

}
void i40()
{
    opJUN(0x000);

}
void i41()
{
    opJUN(0x100);

}
void i42()
{
    opJUN(0x200);

}
void i43()
{
    opJUN(0x300);

}
void i44()
{
    opJUN(0x400);

}
void i45()
{
    opJUN(0x500);

}
void i46()
{
    opJUN(0x600);

}
void i47()
{
    opJUN(0x700);

}
void i48()
{
    opJUN(0x800);

}
void i49()
{
    opJUN(0x900);

}
void i4a()
{
    opJUN(0xa00);

}
void i4b()
{
    opJUN(0xb00);

}
void i4c()
{
    opJUN(0xc00);

}
void i4d()
{
    opJUN(0xd00);

}
void i4e()
{
    opJUN(0xe00);

}
void i4f()
{
    opJUN(0xf00);

}
void i50()
{
    opJMS(0x000);

}
void i51()
{
    opJMS(0x100);

}
void i52()
{
    opJMS(0x200);

}
void i53()
{
    opJMS(0x300);

}
void i54()
{
    opJMS(0x400);

}
void i55()
{
    opJMS(0x500);

}
void i56()
{
    opJMS(0x600);

}
void i57()
{
    opJMS(0x700);

}
void i58()
{
    opJMS(0x800);

}
void i59()
{
    opJMS(0x900);

}
void i5a()
{
    opJMS(0xa00);

}
void i5b()
{
    opJMS(0xb00);

}
void i5c()
{
    opJMS(0xc00);

}
void i5d()
{
    opJMS(0xd00);

}
void i5e()
{
    opJMS(0xe00);

}
void i5f()
{
    opJMS(0xf00);

}
void i60()
{
    opINC(0);

}
void i61()
{
    opINC(1);

}
void i62()
{
    opINC(2);

}
void i63()
{
    opINC(3);

}
void i64()
{
    opINC(4);

}
void i65()
{
    opINC(5);

}
void i66()
{
    opINC(6);

}
void i67()
{
    opINC(7);

}
void i68()
{
    opINC(8);

}
void i69()
{
    opINC(9);

}
void i6a()
{
    opINC(10);

}
void i6b()
{
    opINC(11);

}
void i6c()
{
    opINC(12);

}
void i6d()
{
    opINC(13);

}
void i6e()
{
    opINC(14);

}
void i6f()
{
    opINC(15);

}
void i70()
{
    opISZ(0);

}
void i71()
{
    opISZ(1);

}
void i72()
{
    opISZ(2);

}
void i73()
{
    opISZ(3);

}
void i74()
{
    opISZ(4);

}
void i75()
{
    opISZ(5);

}
void i76()
{
    opISZ(6);

}
void i77()
{
    opISZ(7);

}
void i78()
{
    opISZ(8);

}
void i79()
{
    opISZ(9);

}
void i7a()
{
    opISZ(10);

}
void i7b()
{
    opISZ(11);

}
void i7c()
{
    opISZ(12);

}
void i7d()
{
    opISZ(13);

}
void i7e()
{
    opISZ(14);

}
void i7f()
{
    opISZ(15);

}
void i80()
{
    opADD(0);

}
void i81()
{
    opADD(1);

}
void i82()
{
    opADD(2);

}
void i83()
{
    opADD(3);

}
void i84()
{
    opADD(4);

}
void i85()
{
    opADD(5);

}
void i86()
{
    opADD(6);

}
void i87()
{
    opADD(7);

}
void i88()
{
    opADD(8);

}
void i89()
{
    opADD(9);

}
void i8a()
{
    opADD(10);

}
void i8b()
{
    opADD(11);

}
void i8c()
{
    opADD(12);

}
void i8d()
{
    opADD(13);

}
void i8e()
{
    opADD(14);

}
void i8f()
{
    opADD(15);

}
void i90()
{
    opSUB(0);

}
void i91()
{
    opSUB(1);

}
void i92()
{
    opSUB(2);

}
void i93()
{
    opSUB(3);

}
void i94()
{
    opSUB(4);

}
void i95()
{
    opSUB(5);

}
void i96()
{
    opSUB(6);

}
void i97()
{
    opSUB(7);

}
void i98()
{
    opSUB(8);

}
void i99()
{
    opSUB(9);

}
void i9a()
{
    opSUB(10);

}
void i9b()
{
    opSUB(11);

}
void i9c()
{
    opSUB(12);

}
void i9d()
{
    opSUB(13);

}
void i9e()
{
    opSUB(14);

}
void i9f()
{
    opSUB(15);

}
void ia0()
{
    opLD(0);

}
void ia1()
{
    opLD(1);

}
void ia2()
{
    opLD(2);

}
void ia3()
{
    opLD(3);

}
void ia4()
{
    opLD(4);

}
void ia5()
{
    opLD(5);

}
void ia6()
{
    opLD(6);

}
void ia7()
{
    opLD(7);

}
void ia8()
{
    opLD(8);

}
void ia9()
{
    opLD(9);

}
void iaa()
{
    opLD(10);

}
void iab()
{
    opLD(11);

}
void iac()
{
    opLD(12);

}
void iad()
{
    opLD(13);

}
void iae()
{
    opLD(14);

}
void iaf()
{
    opLD(15);

}
void ib0()
{
    opXCH(0);

}
void ib1()
{
    opXCH(1);

}
void ib2()
{
    opXCH(2);

}
void ib3()
{
    opXCH(3);

}
void ib4()
{
    opXCH(4);

}
void ib5()
{
    opXCH(5);

}
void ib6()
{
    opXCH(6);

}
void ib7()
{
    opXCH(7);

}
void ib8()
{
    opXCH(8);

}
void ib9()
{
    opXCH(9);

}
void iba()
{
    opXCH(10);

}
void ibb()
{
    opXCH(11);

}
void ibc()
{
    opXCH(12);

}
void ibd()
{
    opXCH(13);

}
void ibe()
{
    opXCH(14);

}
void ibf()
{
    opXCH(15);

}
void ic0()
{
    opBBL(0);

}
void ic1()
{
    opBBL(1);

}
void ic2()
{
    opBBL(2);

}
void ic3()
{
    opBBL(3);

}
void ic4()
{
    opBBL(4);

}
void ic5()
{
    opBBL(5);

}
void ic6()
{
    opBBL(6);

}
void ic7()
{
    opBBL(7);

}
void ic8()
{
    opBBL(8);

}
void ic9()
{
    opBBL(9);

}
void ica()
{
    opBBL(10);

}
void icb()
{
    opBBL(11);

}
void icc()
{
    opBBL(12);

}
void icd()
{
    opBBL(13);

}
void ice()
{
    opBBL(14);

}
void icf()
{
    opBBL(15);

}
void id0()
{
    opLDM(0);

}
void id1()
{
    opLDM(1);

}
void id2()
{
    opLDM(2);

}
void id3()
{
    opLDM(3);

}
void id4()
{
    opLDM(4);

}
void id5()
{
    opLDM(5);

}
void id6()
{
    opLDM(6);

}
void id7()
{
    opLDM(7);

}
void id8()
{
    opLDM(8);

}
void id9()
{
    opLDM(9);

}
void ida()
{
    opLDM(10);

}
void idb()
{
    opLDM(11);

}
void idc()
{
    opLDM(12);

}
void idd()
{
    opLDM(13);

}
void ide()
{
    opLDM(14);

}
void idf()
{
    opLDM(15);

}
void ie0()
{
    opWRM();

}
void ie1()
{
    opWMP();

}
void ie2()
{
    opWRR();

}
void ie4()
{
    opWR(0);

}
void ie5()
{
    opWR(1);

}
void ie6()
{
    opWR(2);

}
void ie7()
{
    opWR(3);

}
void ie8()
{
    opSBM();

}
void ie9()
{
    opRDM();

}
void iea()
{
    opRDR();

}
void ieb()
{
    opADM();

}
void iec()
{
    opRD(0);

}
void ied()
{
    opRD(1);

}
void iee()
{
    opRD(2);

}
void ief()
{
    opRD(3);

}
void if0()
{
    opCLB();

}
void if1()
{
    opCLC();

}
void if2()
{
    opIAC();

}
void if3()
{
    opCMC();

}
void if4()
{
    opCMA();

}
void if5()
{
    opRAL();

}
void if6()
{
    opRAR();

}
void if7()
{
    opTCC();

}
void if8()
{
    opDAC();

}
void if9()
{
    opTCS();

}
void ifa()
{
    opSTC();

}
void ifb()
{
    opDAA();

}
void ifc()
{
    opKBP();

}
void ifd()
{
    opDCL();

}
void ini()
{
    if (debug)
        /* Unsupported function call: alert('Not implemented') */;
    incPC();

}
void mainLoop()
{
    if (stepFlag)
    {
        cpuLoop(1);
        stepFlag = FALSE;
    }
    if (animFlag)
        cpuLoop(1);
    if (runFlag)
        cpuLoop(12500);
    /* Unsupported function call: setTimeout("mainLoop()",0) */;

}
void cpuLoop(int16_t cycleLimit)
{
    int16_t code;

    ARRAY_CREATE(gc_22810, 2, 0);

    (cycleLimit = cycleLimit + cpuCycles);
    while (cpuCycles < cycleLimit)
    {
        int16_t arr_pos;
        int16_t i;
        code = activeCode();
        /* Unsupported function call: codes[code]() */;
        (cpuCycles = cpuCycles + cycles[code]);
        arr_pos = -1;
        for (i = 0; i < breakpoints->size; i++) {
            if (/* unsupported equality expression (synthesized node) */) {
                arr_pos = i;
                break;
            }
        }
        if ((arr_pos != -1) && !stepFlag)
        {
            /* Unsupported function call: alert("Stop at: "+getHexAddr(PC_stack[0])+" (breakpoint)") */;
            animFlag = FALSE;
            runFlag = FALSE;
            break;
        }
    }
    /* Unsupported function call: changeAll() */;
    for (gc_i = 0; gc_i < gc_22810->size; gc_i++)
        free(gc_22810->data[gc_i]);
    free(gc_22810->data);
    free(gc_22810);

}
void resetCPU()
{
    A_reg = C_flag = T_flag = 0;
    PC_stack[0] = 0;
    PC_stack[1] = 0;
    PC_stack[2] = 0;
    PC_stack[3] = 0;
    sp = 0;
    for (i = 0;js_var_from(JS_VAR_NAN) < 16;/* expression is not yet supported i++ */)
        R_regs->data[i] = 0;
    cmram = 1;
    ramaddr = 0;
    cmrom = 0;
    animFlag = FALSE;
    runFlag = FALSE;
    stepFlag = FALSE;
    cpuCycles = 0;

}
void clearRAM()
{
    int16_t i;
    int16_t j;
    int16_t k;
    for (i = 0;i < 16;i++)
        for (j = 0;j < 4;j++)
        for (k = 0;k < 16;k++)
        ramdata->data[i]->data[j]->data[k] = 0;
    for (i = 0;i < 16;i++)
        for (j = 0;j < 4;j++)
        for (k = 0;k < 4;k++)
        ramstatus->data[i]->data[j]->data[k] = 0;
    for (i = 0;i < 16;i++)
        ramout->data[i] = 0;

}
void clearROM()
{
    for (i = 0;js_var_from(JS_VAR_NAN) <= 0xfff;(js_var_from(JS_VAR_NAN) = js_var_from(JS_VAR_NAN) + 1))
        prom->data[i] = 0;
    romport = 0;

}
void reset()
{
    resetCPU();
    clearRAM();
    clearROM();
    /* Unsupported function call: changeAll() */;

}

int main(void) {
    ARRAY_CREATE(gc_main, 2, 0);
    ARRAY_CREATE(gc_main_arrays, 2, 0);

    debug = FALSE;
    /* Unsupported 'new' expression new Array(4) */;
    sp = 0;
    /* Unsupported 'new' expression new Array(16) */;
    /* Unsupported 'new' expression new Array(4096) */;
    /* Unsupported 'new' expression new Array(16) */;
    for (i = 0;js_var_from(JS_VAR_NAN) < 16;/* expression is not yet supported i++ */)
    {
        /* Unsupported 'new' expression new Array(4) */;
        for (j = 0;js_var_from(JS_VAR_NAN) < 4;/* expression is not yet supported j++ */)
            /* Unsupported 'new' expression new Array(16) */;
    }
    /* Unsupported 'new' expression new Array(16) */;
    for (i = 0;js_var_from(JS_VAR_NAN) < 16;/* expression is not yet supported i++ */)
    {
        /* Unsupported 'new' expression new Array(4) */;
        for (j = 0;js_var_from(JS_VAR_NAN) < 4;/* expression is not yet supported j++ */)
            /* Unsupported 'new' expression new Array(4) */;
    }
    /* Unsupported 'new' expression new Array(16) */;
    ARRAY_CREATE(breakpoints, 2, 0);
    testFlag = FALSE;
    animFlag = FALSE;
    runFlag = FALSE;
    stepFlag = FALSE;
    codes[0] = i00;
    codes[1] = ini;
    codes[2] = ini;
    codes[3] = ini;
    codes[4] = ini;
    codes[5] = ini;
    codes[6] = ini;
    codes[7] = ini;
    codes[8] = ini;
    codes[9] = ini;
    codes[10] = ini;
    codes[11] = ini;
    codes[12] = ini;
    codes[13] = ini;
    codes[14] = ini;
    codes[15] = ini;
    codes[16] = i10;
    codes[17] = i11;
    codes[18] = i12;
    codes[19] = i13;
    codes[20] = i14;
    codes[21] = i15;
    codes[22] = i16;
    codes[23] = i17;
    codes[24] = i18;
    codes[25] = i19;
    codes[26] = i1a;
    codes[27] = i1b;
    codes[28] = i1c;
    codes[29] = i1d;
    codes[30] = i1e;
    codes[31] = i1f;
    codes[32] = i20;
    codes[33] = i21;
    codes[34] = i22;
    codes[35] = i23;
    codes[36] = i24;
    codes[37] = i25;
    codes[38] = i26;
    codes[39] = i27;
    codes[40] = i28;
    codes[41] = i29;
    codes[42] = i2a;
    codes[43] = i2b;
    codes[44] = i2c;
    codes[45] = i2d;
    codes[46] = i2e;
    codes[47] = i2f;
    codes[48] = i30;
    codes[49] = i31;
    codes[50] = i32;
    codes[51] = i33;
    codes[52] = i34;
    codes[53] = i35;
    codes[54] = i36;
    codes[55] = i37;
    codes[56] = i38;
    codes[57] = i39;
    codes[58] = i3a;
    codes[59] = i3b;
    codes[60] = i3c;
    codes[61] = i3d;
    codes[62] = i3e;
    codes[63] = i3f;
    codes[64] = i40;
    codes[65] = i41;
    codes[66] = i42;
    codes[67] = i43;
    codes[68] = i44;
    codes[69] = i45;
    codes[70] = i46;
    codes[71] = i47;
    codes[72] = i48;
    codes[73] = i49;
    codes[74] = i4a;
    codes[75] = i4b;
    codes[76] = i4c;
    codes[77] = i4d;
    codes[78] = i4e;
    codes[79] = i4f;
    codes[80] = i50;
    codes[81] = i51;
    codes[82] = i52;
    codes[83] = i53;
    codes[84] = i54;
    codes[85] = i55;
    codes[86] = i56;
    codes[87] = i57;
    codes[88] = i58;
    codes[89] = i59;
    codes[90] = i5a;
    codes[91] = i5b;
    codes[92] = i5c;
    codes[93] = i5d;
    codes[94] = i5e;
    codes[95] = i5f;
    codes[96] = i60;
    codes[97] = i61;
    codes[98] = i62;
    codes[99] = i63;
    codes[100] = i64;
    codes[101] = i65;
    codes[102] = i66;
    codes[103] = i67;
    codes[104] = i68;
    codes[105] = i69;
    codes[106] = i6a;
    codes[107] = i6b;
    codes[108] = i6c;
    codes[109] = i6d;
    codes[110] = i6e;
    codes[111] = i6f;
    codes[112] = i70;
    codes[113] = i71;
    codes[114] = i72;
    codes[115] = i73;
    codes[116] = i74;
    codes[117] = i75;
    codes[118] = i76;
    codes[119] = i77;
    codes[120] = i78;
    codes[121] = i79;
    codes[122] = i7a;
    codes[123] = i7b;
    codes[124] = i7c;
    codes[125] = i7d;
    codes[126] = i7e;
    codes[127] = i7f;
    codes[128] = i80;
    codes[129] = i81;
    codes[130] = i82;
    codes[131] = i83;
    codes[132] = i84;
    codes[133] = i85;
    codes[134] = i86;
    codes[135] = i87;
    codes[136] = i88;
    codes[137] = i89;
    codes[138] = i8a;
    codes[139] = i8b;
    codes[140] = i8c;
    codes[141] = i8d;
    codes[142] = i8e;
    codes[143] = i8f;
    codes[144] = i90;
    codes[145] = i91;
    codes[146] = i92;
    codes[147] = i93;
    codes[148] = i94;
    codes[149] = i95;
    codes[150] = i96;
    codes[151] = i97;
    codes[152] = i98;
    codes[153] = i99;
    codes[154] = i9a;
    codes[155] = i9b;
    codes[156] = i9c;
    codes[157] = i9d;
    codes[158] = i9e;
    codes[159] = i9f;
    codes[160] = ia0;
    codes[161] = ia1;
    codes[162] = ia2;
    codes[163] = ia3;
    codes[164] = ia4;
    codes[165] = ia5;
    codes[166] = ia6;
    codes[167] = ia7;
    codes[168] = ia8;
    codes[169] = ia9;
    codes[170] = iaa;
    codes[171] = iab;
    codes[172] = iac;
    codes[173] = iad;
    codes[174] = iae;
    codes[175] = iaf;
    codes[176] = ib0;
    codes[177] = ib1;
    codes[178] = ib2;
    codes[179] = ib3;
    codes[180] = ib4;
    codes[181] = ib5;
    codes[182] = ib6;
    codes[183] = ib7;
    codes[184] = ib8;
    codes[185] = ib9;
    codes[186] = iba;
    codes[187] = ibb;
    codes[188] = ibc;
    codes[189] = ibd;
    codes[190] = ibe;
    codes[191] = ibf;
    codes[192] = ic0;
    codes[193] = ic1;
    codes[194] = ic2;
    codes[195] = ic3;
    codes[196] = ic4;
    codes[197] = ic5;
    codes[198] = ic6;
    codes[199] = ic7;
    codes[200] = ic8;
    codes[201] = ic9;
    codes[202] = ica;
    codes[203] = icb;
    codes[204] = icc;
    codes[205] = icd;
    codes[206] = ice;
    codes[207] = icf;
    codes[208] = id0;
    codes[209] = id1;
    codes[210] = id2;
    codes[211] = id3;
    codes[212] = id4;
    codes[213] = id5;
    codes[214] = id6;
    codes[215] = id7;
    codes[216] = id8;
    codes[217] = id9;
    codes[218] = ida;
    codes[219] = idb;
    codes[220] = idc;
    codes[221] = idd;
    codes[222] = ide;
    codes[223] = idf;
    codes[224] = ie0;
    codes[225] = ie1;
    codes[226] = ie2;
    codes[227] = ini;
    codes[228] = ie4;
    codes[229] = ie5;
    codes[230] = ie6;
    codes[231] = ie7;
    codes[232] = ie8;
    codes[233] = ie9;
    codes[234] = iea;
    codes[235] = ieb;
    codes[236] = iec;
    codes[237] = ied;
    codes[238] = iee;
    codes[239] = ief;
    codes[240] = if0;
    codes[241] = if1;
    codes[242] = if2;
    codes[243] = if3;
    codes[244] = if4;
    codes[245] = if5;
    codes[246] = if6;
    codes[247] = if7;
    codes[248] = if8;
    codes[249] = if9;
    codes[250] = ifa;
    codes[251] = ifb;
    codes[252] = ifc;
    codes[253] = ifd;
    codes[254] = ini;
    codes[255] = ini;
    free(R_regs->data);
    free(R_regs);
    free(prom->data);
    free(prom);
    free(ramdata->data);
    free(ramdata);
    free(ramstatus->data);
    free(ramstatus);
    free(ramout->data);
    free(ramout);
    free(breakpoints->data);
    free(breakpoints);
    for (gc_i = 0; gc_i < gc_main_arrays->size; gc_i++) {
        free(gc_main_arrays->data[gc_i]->data);
        free(gc_main_arrays->data[gc_i]);
    }
    free(gc_main_arrays->data);
    free(gc_main_arrays);
    for (gc_i = 0; gc_i < gc_main->size; gc_i++)
        free(gc_main->data[gc_i]);
    free(gc_main->data);
    free(gc_main);

    return 0;
}
