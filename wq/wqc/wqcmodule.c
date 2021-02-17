#include <Python.h>
#include <pthread.h>
#include "wqc.h"
#include "wq6502.h"


void* sum(void *argp){
    unsigned long *stepsFrom = (unsigned long *) argp;
    unsigned long *stepsTo = (unsigned long *) (argp + sizeof(unsigned long));
    unsigned long s, i;

    s = 0;
    for(i=*stepsFrom; i<*stepsTo; i++)
        s += (i+1);

    return (void *)s;
}


static int number = 0;

int incDecNumber(int n){
    number += n;
    return number;
}


static PyObject* method_sum(PyObject* self, PyObject* args) {
    unsigned long countOfNumbers;
    if(!PyArg_ParseTuple(args, "k", &countOfNumbers)){
        printf("# FAIL\n");
        return NULL;
    }

    int n = (int)countOfNumbers;
    int result = incDecNumber(n);

    return PyLong_FromLong((unsigned long)result);
}

static PyObject* method_c6502_initold(PyObject* self, PyObject* args) {
    /*unsigned long pinValues;
    if(!PyArg_ParseTuple(args, "k", &pinValues)){
        printf("# FAIL\n");
        return NULL;
    }*/

    //int n = (int)countOfNumbers;
    uint64_t result = 0;
    wq6502Info_t info;
    wq6502_init(&info);

    return PyLong_FromLong((unsigned long)result);
}

static PyObject* method_cpc_init(PyObject* self, PyObject* args) {
    PyObject* dict = NULL;
    dict = pyDictNew();//PyDict_New();
    return dict;
}


static PyObject* method_c6502_init(PyObject* self, PyObject* args) {

    PyObject* dict = NULL;
    PyObject* dictIn = NULL;
    //PyObject* temp_p = PyTuple_GetItem(args,0);
    Py_ssize_t TupleSize = PyTuple_Size(args);
    if (TupleSize){
        if (!PyArg_ParseTuple(args, "|O",  &dictIn)){//&PyDict_Type,
            goto except;
        }
    } else {
        dictIn = pyDictNew();
    }



    dict = pyDictNew();//PyDict_New();
    
    uint64_t result = 0;

    
    PyObject* signalMap = pyDictNew();//PyDict_New();

    pyDictSetSizet(signalMap,"@size",64);

    /**
     * Information from "Commodore Semiconductor Group, 6500 MICROPROCESSORS" document.
     * 
     * http://archive.6502.org/datasheets/mos_6500_mpu_nov_1985.pdf
     * 
     * */
#ifndef Q3C_CLASSIC_6502
    PyObject* vpbDict = pyDictNew();
    pyDictSetSizet(vpbDict,"from",0);
    pyDictSetObject(signalMap,"VPB",vpbDict);
#endif
    PyObject* rdyDict = pyDictNew();//PyDict_New();//PyLong_FromSize_t(1);
    pyDictSetSizet(rdyDict,"from",CPINS_RDY);
    pyDictSetString(rdyDict,"ioType","I");
    pyDictSetSizet(rdyDict,"size",1);
    pyDictSetString(rdyDict,"info","Ready signal (input, 1bit, high-active)");
    pyDictSetString(rdyDict,"doc","This  input signal allows the user to single cycle the microprocessor on all cycles except write cycles. A negative transition to the low state during or coincident with  phase one (0,) and  up to  100ns after phase two (02) will halt the microprocessor with  the output address lines  reflecting the current address  being fetched. This condition will  remain through a subsequent phase two (<2fJ  in which the  Ready signal  is  low. This feature allows microprocessor interfacing with  low speed  PROMS as well as fast (max. 2  cycle)  Direct  Memory Access (DMA).  If  Ready is low during a write cycle,  it is ignored until the following  read  operation");
    pyDictSetObject(signalMap,"RDY",rdyDict);
#ifndef Q3C_CLASSIC_6502
    //Clocks  (01,  02)The 651X requires a two phase non-overlapping clock that runs at the Vcc voltage level. The 650X clocks are supplied with an internal clock generator. The frequency of these clocks  is externally controlled.
    PyObject* phi1oDict = pyDictNew();
    pyDictSetSizet(phi1oDict,"from",2);
    pyDictSetString(phi1oDict,"ioType","O");
    pyDictSetObject(signalMap,"PHI1O",phi1oDict);
#endif
    PyObject* irqbDict = pyDictNew();
    pyDictSetSizet(irqbDict,"from",CPINS_IRQB);
    pyDictSetSizet(irqbDict,"size",1);
    pyDictSetString(irqbDict,"info","Interrupt  Request (IRQ)");
    pyDictSetString(irqbDict,"doc","This TTL level  input requests that an  interrupt sequence begin within  the microprocessor. The microprocessor will complete the current instruction  being executed before recognizing  the request. At that time, the interrupt mask bit in the Status Code  Register will be examined.  If the  interrupt mask flag is not set. the microprocessor will  begin an  interrupt sequence. The  Program Counter and  Processor Status  Register are stored in the stack.The  microprocessor will then  set the  interrupt mask  flag  high so that no further interrupts may occur. At the end of this cycle, the program counter low will be loaded from address  FFFE. and program counter high  from  location  FFFF. therefore transferring program control to the memory vector located  at these addresses. The  RDY signal must be in  the high  state for any interrupt to  be recognized. A 3K  external  resistor should be used for proper wire-OR operation.");
    pyDictSetObject(signalMap,"IRQB",irqbDict);
#ifndef Q3C_CLASSIC_6502
    PyObject* nc0Dict = pyDictNew();
    pyDictSetSizet(nc0Dict,"from",4);
    pyDictSetObject(signalMap,"NC0",nc0Dict); 
#endif
    PyObject* nmibDict = pyDictNew();
    pyDictSetSizet(nmibDict,"from",CPINS_NMIB);
    pyDictSetSizet(nmibDict,"size",1);
    pyDictSetString(nmibDict,"info","Non-Maskable  Interrupt (NM I)");
    pyDictSetString(nmibDict,"doc","A negative going edge on this  input requests that a  non-maskable interrupt sequence be generated within the microprocessor. NMiT is an  unconditional  interrupt.  Following completion of the current instruction, the sequence of operations defined  for IRQ will be performed, regardless of the interrupt mask flag status. The vector address  loaded into the program  counter,  low and high, are locations FFFA and FFFB  respectively, thereby transferring program control to the memory vector located  at these addresses. The instructions loaded  at these locations  cause the microprocessor to branch to a non-maskable interrupt routine in memory.NMI  also requires an external 3K  register to Vcc for proper wire- OR operations.Inputs  IRQ and  NMI  are hardware interrupt lines that are sampled during’0 , (phase 2)  and will  begin the appropriate interrupt routine on the 0.  (phase  1) following the completion of the current instruction.");
    pyDictSetObject(signalMap,"NMIB",nmibDict); 

    PyObject* syncDict = pyDictNew();
    pyDictSetSizet(syncDict,"from",CPINS_SYNC);
    pyDictSetSizet(syncDict,"size",1);
    pyDictSetString(syncDict,"ioType","O");
    pyDictSetString(syncDict,"info","SYNC");
    pyDictSetString(syncDict,"doc","This output line is provided to identify those cycles  in which the microprocessor is doing an OP CODE fetch. The SYNC  line goes high during  0,  of an OP CODE  fetch  and stays  high for the remainder of that cycle.  If the  RDY line is  pulled  low during the 0, clock  pulse in which  SYNC went high, the processor will stop in its current state and will  remain  in the state until the RDY  line goes high.  In this  manner, the SYNC signal  can  be used to control  RDY to cause single instruction execution.");
    pyDictSetObject(signalMap,"SYNC",syncDict);
#ifndef Q3C_CLASSIC_6502
    PyObject* vccDict = pyDictNew();
    pyDictSetSizet(vccDict,"from",7);
    pyDictSetObject(signalMap,"VCC",vccDict);
#endif
    PyObject* adrDict = pyDictNew();
    pyDictSetSizet(adrDict,"from",CPINS_A0);
    pyDictSetSizet(adrDict,"size",16);
    pyDictSetString(adrDict,"ioType","O");
    pyDictSetString(adrDict,"info","Address  Bus (A0-A15)");
    pyDictSetString(adrDict,"doc","These outputs are TTL compatible, capable of driving one standard TTL load and  130  pf.");
    pyDictSetObject(signalMap,"ADR",adrDict);

    PyObject* resbDict = pyDictNew();
    pyDictSetSizet(resbDict,"from",CPINS_RESB);
    pyDictSetSizet(resbDict,"size",1);
    pyDictSetString(resbDict,"info","Reset");
    pyDictSetString(resbDict,"doc","This input is  used to reset or start the microprocessor from a power down condition.  During the time that this  line is  held  low, writing to or from the microprocessor is  inhibited. When a positive edge is detected on  the  input, the microprocessor will  immediately begin the reset sequence.After a  system  initialization time of six clock cycles, the  mask interrupt flag will be set and the microprocessor will  load  the program counter from the memory vector locations FFFC and FFFD. This is the start location for program control. After Vcc reaches 4.75 volts in a  power up routine, reset must be held low for at least two clock cycles. At this time the R/W and (SYNC) signal will become valid.When  the reset signal  goes high following these two clock cycles, the microprocessor will  proceed with the normal  reset procedure detailed above");
    pyDictSetObject(signalMap,"RESB",resbDict);
#ifndef Q3C_CLASSIC_6502
    //Clocks  (01,  02)
    PyObject* phi2oDict = pyDictNew();
    pyDictSetSizet(phi2oDict,"from",33);
    pyDictSetString(phi2oDict,"ioType","O");
    pyDictSetObject(signalMap,"PHI2O",phi2oDict);

    PyObject* sobDict = pyDictNew();
    pyDictSetSizet(sobDict,"from",34);
    pyDictSetString(sobDict,"info","Set  Overflow  Flag  (S.O.)");
    pyDictSetString(sobDict,"doc","A  NEGATIVE going edge on this input sets the overflow bit in the Status Code  Register. This signal  is sampled on  the trailing edgeo f0");
    pyDictSetObject(signalMap,"SOB",sobDict);
#endif    
    //Clocks - input
    PyObject* phioiDict = pyDictNew();
    pyDictSetSizet(phioiDict,"from",CPINS_PHI2);
    pyDictSetSizet(phioiDict,"size",1);
    pyDictSetObject(signalMap,"PHI0I",phioiDict);
#ifndef Q3C_CLASSIC_6502
    //NC
    PyObject* nc1Dict = pyDictNew();
    pyDictSetSizet(nc1Dict,"from",36);
    pyDictSetObject(signalMap,"NC1",nc1Dict);

    PyObject* nc2Dict = pyDictNew();
    pyDictSetSizet(nc2Dict,"from",37);
    pyDictSetObject(signalMap,"NC2",nc2Dict);
#endif
    PyObject* rwbDict = pyDictNew();
    pyDictSetSizet(rwbDict,"from",CPINS_RWB);
    pyDictSetSizet(rwbDict,"size",1);
    pyDictSetString(rwbDict,"info","Data  Bus  Enable(DBE)");
    pyDictSetString(rwbDict,"doc","This TTL compatible input allows external control of the tri-state data output buffers and will enabel the microprocessor bus driver when  in the high state. In normal operation  DBE would be driven by the phase two (02) clock, thus allowing data  output from microprocessor only during 0;. During the  read cycle, the data bus drivers are internally disabled, becoming  essentially an open circuit. To disable data bus drivers externally, DBE should be held low");
    pyDictSetObject(signalMap,"RWB",rwbDict);

    PyObject* dtaDict = pyDictNew();
    pyDictSetSizet(dtaDict,"from",CPINS_D0);
    pyDictSetSizet(dtaDict,"size",8);
    pyDictSetString(dtaDict,"ioType","D");
    pyDictSetString(dtaDict,"info","Data  Bus (D0-D7)");
    pyDictSetString(dtaDict,"doc","Eight pins are used for the data bus. This is a bi-directional  bus. transferring data to and from the device and  peripherals. The outputs are tri-state buffers capable of driving one standard  TTL load and  130  pf.");
    pyDictSetObject(signalMap,"DTA",dtaDict);
#ifndef Q3C_CLASSIC_6502
    PyObject* npDict = pyDictNew();
    pyDictSetSizet(npDict,"from",55);
    pyDictSetObject(signalMap,"NP",npDict);

    PyObject* vssDict = pyDictNew();
    pyDictSetSizet(vssDict,"from",63);
    pyDictSetObject(signalMap,"VSS",vssDict);
#endif
    PyObject* endDict = pyDictNew();
    pyDictSetSizet(endDict,"from",64);
    pyDictSetObject(signalMap,"@end",endDict);

    //PyDict_SetItemString(dict, "signalMap", signalMap);
    pyDictSetObject(dict,"signalMap",signalMap);
    pyDictSetObject(dict,"dictIn",dictIn);

    return dict;
    assert(! PyErr_Occurred());
    assert(dict);
    goto finally;
except:
    PyErr_Print();
    //printf("Exception");
    Py_XDECREF(dict);  
    dict = NULL;
finally:
    return dict;
}

extern  int cpc_run(int argc, unsigned int wid);
extern  void setRootWid(unsigned int wid);
extern  void triggerWidResize(unsigned int wid,unsigned int w,unsigned int h);
extern  unsigned int getRootWid();

#include <pthread.h> 

void *myThreadFun(void *vargp) 
{ 
    cpc_run(1,getRootWid());
    sleep(1); 
    printf("Printing GeeksQuiz from Thread \n"); 
    return NULL; 
} 

static PyObject* method_cpc_insp(PyObject* self, PyObject* args) {

    PyObject* dictIn = NULL;

    Py_ssize_t TupleSize = PyTuple_Size(args);
    if (TupleSize){
        if (!PyArg_ParseTuple(args, "|O",  &dictIn)){//&PyDict_Type,
            goto except;
        }
    } else {
        dictIn = pyDictNew();
    }

    PyObject * pOb = pyDictGetItem(dictIn,"winId");
    long hwnd = PyLong_AsLong(pOb);
    PyObject * pObW = pyDictGetItem(dictIn,"width");
    PyObject * pObH = pyDictGetItem(dictIn,"height");
    long w = PyLong_AsLong(pObW);
    long h = PyLong_AsLong(pObH);
    //HWND hwnd = (HWND)PyCObject_AsVoidPtr(pOb)
    //PyObject * pOb2 = pyDictGetItem(dictIn,"command");
    triggerWidResize(hwnd,w,h);

    //pthread_t thread_id; 
    //printf("Before Thread\n"); 
   // pthread_create(&thread_id, NULL, myThreadFun, NULL); 

    
 

    PyObject* dict = pyDictNew();

    return dict;
    assert(! PyErr_Occurred());
    assert(dict);
    goto finally;
except:
    PyErr_Print();
    //printf("Exception");
    Py_XDECREF(dict);  
    dict = NULL;
finally:
    return dict;
}

static PyObject* method_cpc_open(PyObject* self, PyObject* args) {

    PyObject* dictIn = NULL;

    Py_ssize_t TupleSize = PyTuple_Size(args);
    if (TupleSize){
        if (!PyArg_ParseTuple(args, "|O",  &dictIn)){//&PyDict_Type,
            goto except;
        }
    } else {
        dictIn = pyDictNew();
    }

    PyObject * pOb = pyDictGetItem(dictIn,"winId");
    long hwnd = PyLong_AsLong(pOb);
    //HWND hwnd = (HWND)PyCObject_AsVoidPtr(pOb)
    setRootWid(hwnd);

    pthread_t thread_id; 
    //printf("Before Thread\n"); 
    pthread_create(&thread_id, NULL, myThreadFun, NULL); 

    
 

    PyObject* dict = pyDictNew();

    return dict;
    assert(! PyErr_Occurred());
    assert(dict);
    goto finally;
except:
    PyErr_Print();
    //printf("Exception");
    Py_XDECREF(dict);  
    dict = NULL;
finally:
    return dict;
}

static PyObject* method_c6502_open(PyObject* self, PyObject* args) {

    PyObject* dictIn = NULL;

    Py_ssize_t TupleSize = PyTuple_Size(args);
    if (TupleSize){
        if (!PyArg_ParseTuple(args, "|O",  &dictIn)){//&PyDict_Type,
            goto except;
        }
    } else {
        dictIn = pyDictNew();
    }

    PyObject* dict = pyDictNew();

    wq6502Info_t info;
    wq6502_init(&info);

    pyDictSetSizet(dict,"iv",info.iv);

    pyDictSetUint64(dict,"pins",info.pins);

    goto finally;
except:
    PyErr_Print();
    //printf("Exception");
    Py_XDECREF(dict);  
    dict = NULL;
finally:
    return dict;
}

static PyObject* method_c6502_insp(PyObject* self, PyObject* args) {

    PyObject* result = PyList_New(0);
    int i;

    for (i = 0; i < 100; ++i)
    {
        PyList_Append(result, PyLong_FromLong(i));
    }

    return result;
}

static PyObject* method_cpc_calc(PyObject* self, PyObject* args) {
    PyObject* dict = pyDictNew();
    return dict;
}

static PyObject* method_c6502_calc(PyObject* self, PyObject* args) {
    unsigned long pinValues;
    size_t iv;
    if(!PyArg_ParseTuple(args, "nk", &iv, &pinValues)){
        printf("# FAIL\n");
        return NULL;
    }

    //int n = (int)countOfNumbers;
    uint64_t result = wq6502_calc(iv,pinValues);

    return PyLong_FromLong((unsigned long)result);
}

static PyMethodDef WqcMethods[] = {
    {"sum", method_sum, METH_VARARGS, "Calculate sum of n numbers."},
    {"c6502_init2", method_c6502_initold, METH_VARARGS, "Init 6502 CPU"},
    {"c6502_init", method_c6502_init, METH_VARARGS, "Init 6502 CPU Infra"},
    {"c6502_open", method_c6502_open, METH_VARARGS, "Open 6502 CPU (newObj)."},
    {"c6502_calc", method_c6502_calc, METH_VARARGS, "Calc 6502 CPU (tick)."},
    {"c6502_insp", method_c6502_insp, METH_VARARGS, "Inspect 6502 CPU."},
    {"cpc_init", method_cpc_init, METH_VARARGS, "Init CPC System Infra"},
    {"cpc_open", method_cpc_open, METH_VARARGS, "Open CPC (newObj)."},
    {"cpc_insp", method_cpc_insp, METH_VARARGS, "Insp CPC."},
    {"cpc_calc", method_cpc_calc, METH_VARARGS, "Calc CPC (tick)."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef wqcmodule = {
    PyModuleDef_HEAD_INIT,
    "wqChips",
    "Different chips simulation.",
    -1,
    WqcMethods
};

PyMODINIT_FUNC PyInit_wqc() {
    return PyModule_Create(&wqcmodule);
}
